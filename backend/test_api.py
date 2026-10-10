import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.main import app, build_context, generate_narrative, load_fixture, select_window, mock_narrative

client=TestClient(app)


@pytest.fixture(autouse=True)
def isolate_provider(monkeypatch):
    # Never spend real API quota during tests, even with a configured .env.
    monkeypatch.setenv('LLM_PROVIDER','mock')

def test_five_overs_includes_wide_and_reconciles_score():
    r=client.get('/api/matches/ind-aus/catch-up')
    assert r.status_code==200
    c=r.json()
    assert len(c['commentary'])==31
    assert sum(b['legal'] for b in c['commentary'])==30
    assert c['window_runs']==49 and c['window_wickets']==2
    assert c['score']==132 and c['wickets']==3
    assert c['runs_needed']==55 and c['balls_remaining']==30
    assert c['required_rate']==11
    assert sum(o['runs'] for o in c['overs'])==49
    assert c['mode']=='mock'

def test_three_over_window_uses_boundaries_not_thirty_records():
    c=client.get('/api/matches/ind-aus/catch-up?window=3').json()
    assert {b['over'] for b in c['commentary']}=={13,14,15}
    assert c['window_runs']==38
    assert len(c['commentary'])==18

def test_window_excludes_future_partial_over():
    f=load_fixture()
    future={**f['commentary'][-1],'over':16,'ball':1}
    assert future not in select_window(f['commentary']+[future],15,5)

def test_empty_error_and_validation():
    c=client.get('/api/matches/ind-aus/catch-up?scenario=empty').json()
    assert c['players']==[] and c['commentary']==[]
    assert client.get('/api/matches/ind-aus/catch-up?scenario=error').status_code==503
    assert client.get('/api/matches/no-match/catch-up').status_code==404
    assert client.get('/api/matches/ind-aus/catch-up?window=6').status_code==422

def test_absent_credentials_fall_back(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','openai')
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    r=client.get('/api/matches/ind-aus/catch-up?ai=true').json()
    assert r['mode']=='fallback' and r['notice']
    assert len(r['narrative']['fantasy'])==len(r['players'])

def test_provider_failure_is_safe(monkeypatch):
    import langchain_openai
    monkeypatch.setenv('LLM_PROVIDER','openai')
    monkeypatch.setenv('OPENAI_API_KEY','fake-test-key')
    def fail(**kwargs): raise RuntimeError('sensitive-provider-details')
    monkeypatch.setattr(langchain_openai,'ChatOpenAI',fail)
    narrative,mode,notice=asyncio.run(generate_narrative(build_context(load_fixture())))
    assert mode=='fallback' and 'sensitive' not in notice
    assert narrative.headline


def test_langchain_structured_response_and_player_validation(monkeypatch):
    import langchain_openai
    from langchain_core.runnables import RunnableLambda
    context=build_context(load_fixture())
    expected=mock_narrative(context)
    monkeypatch.setenv('LLM_PROVIDER','openai')
    monkeypatch.setenv('OPENAI_API_KEY','fake-test-key')
    class FakeModel:
        def __init__(self,**kwargs): pass
        def with_structured_output(self,schema):
            assert schema.__name__=='Narrative'
            return RunnableLambda(lambda prompt: expected)
    monkeypatch.setattr(langchain_openai,'ChatOpenAI',FakeModel)
    result,mode,notice=asyncio.run(generate_narrative(context))
    assert mode=='openai' and result==expected and notice is None
    expected.fantasy[0].player_id='invented-player'
    result,mode,notice=asyncio.run(generate_narrative(context))
    assert mode=='fallback' and notice
    assert all(p.player_id!='invented-player' for p in result.fantasy)
    expected=mock_narrative(context)
    expected.bullets[0].evidence_ids=['unknown-delivery']
    result,mode,notice=asyncio.run(generate_narrative(context))
    assert mode=='fallback' and notice
    assert all('unknown-delivery' not in b.evidence_ids for b in result.bullets)


def test_langchain_timeout_falls_back(monkeypatch):
    import langchain_openai
    from langchain_core.runnables import RunnableLambda
    monkeypatch.setenv('LLM_PROVIDER','openai')
    monkeypatch.setenv('OPENAI_API_KEY','fake-test-key')
    monkeypatch.setenv('LLM_TIMEOUT_SECONDS','0.01')
    async def slow(prompt):
        await asyncio.sleep(1)
        return mock_narrative(build_context(load_fixture()))
    class FakeModel:
        def __init__(self,**kwargs): pass
        def with_structured_output(self,schema): return RunnableLambda(slow)
    monkeypatch.setattr(langchain_openai,'ChatOpenAI',FakeModel)
    result,mode,notice=asyncio.run(generate_narrative(build_context(load_fixture())))
    assert mode=='fallback' and notice and result.headline


def test_gemini_structured_response_and_cors(monkeypatch):
    import langchain_google_genai
    from langchain_core.runnables import RunnableLambda
    monkeypatch.setenv('LLM_PROVIDER','gemini')
    monkeypatch.setenv('GEMINI_API_KEY','fake-test-key')
    class FakeModel:
        def __init__(self,**kwargs): assert kwargs['google_api_key']=='fake-test-key'
        def with_structured_output(self,schema):
            return RunnableLambda(lambda prompt:mock_narrative(build_context(load_fixture())))
    monkeypatch.setattr(langchain_google_genai,'ChatGoogleGenerativeAI',FakeModel)
    response=client.get('/api/matches/ind-aus/catch-up?ai=true',headers={'Origin':'http://127.0.0.1:5180'})
    assert response.json()['mode']=='gemini'
    assert response.headers['access-control-allow-origin']=='http://127.0.0.1:5180'


def test_same_score_has_different_context_and_exactly_active_players():
    comeback=client.get('/api/matches/ind-aus/catch-up').json()
    squeeze=client.get('/api/matches/spin-trap/catch-up').json()
    assert comeback['score']==squeeze['score']==132
    assert comeback['wickets']==squeeze['wickets']==3
    assert comeback['window_runs']==49 and squeeze['window_runs']==32
    assert comeback['overs'][-1]['runs']==22 and squeeze['overs'][-1]['runs']==4
    for c in [comeback,squeeze]:
        assert {p['id'] for p in c['players']}=={'nikhil','rehan','hart'}
        assert len(c['narrative']['bullets'])==3
        assert all(not p['dismissed'] for p in c['players'])
        delivery_ids={b['id'] for b in c['commentary']}
        assert all(set(b['evidence_ids']).issubset(delivery_ids) for b in c['narrative']['bullets'])
    assert comeback['narrative']['headline']!=squeeze['narrative']['headline']


def test_profiles_have_computed_recent_form_and_history():
    c=client.get('/api/matches/ind-aus/catch-up').json()
    p=next(p for p in c['players'] if p['id']=='rehan')
    assert p['experience']==1 and p['debut_year']==2025
    assert p['form_value']==f'{104/59*100:.0f}'
    p=next(p for p in c['players'] if p['id']=='hart')
    assert p['form_value']=='6' and '6.25' in p['form_detail']


def test_hindi_translates_context_and_preserves_numeric_facts():
    en=client.get('/api/matches/ind-aus/catch-up').json()
    hi=client.get('/api/matches/ind-aus/catch-up?language=hi').json()
    assert hi['language']=='hi'
    assert hi['score']==en['score'] and hi['window_runs']==en['window_runs']
    assert 'रेहान' in hi['narrative']['bullets'][1]['text']
    assert hi['players'][0]['name']=='निखिल राव'
    assert all(any('\u0900'<=char<='\u097f' for char in b['text']) for b in hi['commentary'])
    assert all(any('\u0900'<=char<='\u097f' for char in p['forte']) for p in hi['players'])
    assert client.get('/api/matches/ind-aus/catch-up?language=fr').status_code==422


def test_match_listing_exposes_both_demo_ids():
    assert {m['id'] for m in client.get('/api/matches').json()}=={'ind-aus','spin-trap'}


def test_production_frontend_serves_on_api_origin():
    from backend.main import ROOT
    if not (ROOT/'dist/index.html').is_file():
        assert client.get('/').status_code==503
        return
    r=client.get('/')
    assert r.status_code==200 and 'text/html' in r.headers['content-type']
    import re
    asset=re.search(r'src="(/assets/[^\"]+)"',r.text).group(1)
    assert client.get(asset).status_code==200
