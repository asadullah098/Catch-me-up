"""Two fictional stories with the same score. Every cricket figure is fixture-derived."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = [
 dict(id='arjun',name='Arjun Mehta',initials='AM',team='IND',role='Batter',number=18,experience=12,debut_year=2014,style='Top-order anchor',strength='Rotates strike and builds a platform before accelerating.',caution='Dismissed in this snapshot; his batting opportunity is over.',recent_runs=[44,38,52],recent_balls=[35,30,39]),
 dict(id='sahil',name='Sahil Desai',initials='SD',team='IND',role='Batter',number=45,experience=7,debut_year=2019,style='Opening aggressor',strength='Takes on pace early and uses the field restrictions.',caution='Dismissed in this snapshot.',recent_runs=[12,31,8],recent_balls=[10,23,9]),
 dict(id='nikhil',name='Nikhil Rao',initials='NR',team='IND',role='Batter',number=33,experience=4,debut_year=2022,style='Middle-order stabiliser',strength='Keeps the innings moving with singles while a partner attacks.',caution='A supporting role can mean fewer boundary opportunities.',recent_runs=[28,34,22],recent_balls=[24,27,19]),
 dict(id='rehan',name='Rehan Malik',initials='RM',team='IND',role='Batter',number=63,experience=1,debut_year=2025,style='New-generation finisher',strength='Attacks full pace bowling with a strong leg-side hitting range.',caution='Only three recent innings are supplied; this small sample is not a reliable prediction.',recent_runs=[35,28,41],recent_balls=[20,16,23]),
 dict(id='hart',name='Miles Hart',initials='MH',team='AUS',role='Bowler',number=88,experience=8,debut_year=2018,style='Leg-spin disruptor',strength='Uses a slower leg-break and googly to interrupt middle-over partnerships.',caution='Past wickets do not guarantee another; an aggressive partner may change the matchup.',recent_wickets=[2,1,3],recent_conceded=[24,29,22],recent_legal_balls=[24,24,24]),
 dict(id='cole',name='Ethan Cole',initials='EC',team='AUS',role='Bowler',number=56,experience=5,debut_year=2021,style='Left-arm pace',strength='Looks for fuller lengths and wickets at the back end.',caution='Missed yorkers can become boundary opportunities.',recent_wickets=[1,2,0],recent_conceded=[38,26,41],recent_legal_balls=[24,24,24])
]

def generate(kind):
    comeback=kind=='comeback'
    plans = [(11,'cole',[1,0,4,1,0,1]),(12,'hart',[0,1,0,0,1,1]),(13,'hart',[0,0,0,1,1,2]),(14,'cole',[1,4,0,1,4,2]),(15,'cole',[4,6,4,1,1,6])] if comeback else [(11,'cole',[1,0,4,1,0,3]),(12,'hart',[0,1,0,4,1,1]),(13,'hart',[0,0,1,1,4,0]),(14,'cole',[0,1,0,1,1,2]),(15,'hart',[0,1,0,1,0,2])]
    names={p['id']:p['name'] for p in PROFILES}
    striker,nonstriker='arjun','sahil'
    incoming=iter(['nikhil','rehan'])
    balls=[]
    for over,bowler,runs in plans:
        for ball,run in enumerate(runs,1):
            if over==11 and ball==3:
                balls.append(dict(id='11-wide',over=11,ball=3,label='10.3 wd',legal=False,runs=1,bat_runs=0,wicket=False,batter=striker,bowler=bowler,bowling_type='pace',text='Cole drifts outside off. Wide: a free run, but no legal ball used.'))
            wicket=(over,ball) in [(12,3),(13,2)]
            action='finds four through the gap' if run==4 else 'hits six over the rope' if run==6 else 'takes two' if run==2 else 'runs three' if run==3 else 'rotates the strike' if run==1 else 'cannot beat the field'
            text=f'{names[striker]} {action}.'
            if bowler=='hart' and run==0:
                text=f'Hart slows it down; {names[striker]} cannot get the leg-break away. Dot ball.'
            if wicket:
                text=f'Wicket! Hart draws {names[striker]} into a lofted shot with a slower leg-break. Caught at long-on.'
            if comeback and over==15 and run>=4:
                text=f'Cole misses the yorker. {names[striker]} hits {"six over midwicket" if run==6 else "four through the leg side"}; the new finisher is taking on pace.'
            balls.append(dict(id=f'{over}-{ball}',over=over,ball=ball,label=f'{over-1}.{ball}',legal=True,runs=run,bat_runs=run,wicket=wicket,batter=striker,bowler=bowler,bowling_type='spin' if bowler=='hart' else 'pace',text=text))
            if wicket:striker=next(incoming)
            elif run%2:striker,nonstriker=nonstriker,striker
        striker,nonstriker=nonstriker,striker
    total=sum(b['runs'] for b in balls)
    return dict(id='ind-aus' if comeback else 'spin-trap',title='India vs Australia',story='The comeback' if comeback else 'The spin squeeze',competition='T20 International · Fictional demo',venue='Wankhede Stadium, Mumbai',batting_team='IND',bowling_team='AUS',target=187,opponent_score='186/7',total_overs=20,completed_overs=15,score_before=132-total,wickets_before=1,snapshot_at='2026-10-10T14:30:00+05:30',commentary=balls,profiles=PROFILES,active_batters=[striker,nonstriker],active_bowler='hart',bowler_status='Bowling next',source='All players, career records, recent form and match events are fictional demo data.')

def main():
    ROOT.joinpath('data').mkdir(exist_ok=True)
    for filename,kind in [('match.json','comeback'),('spin-trap.json','squeeze')]:
        fixture=generate(kind)
        ROOT.joinpath('data',filename).write_text(json.dumps(fixture,indent=2),encoding='utf8')
        print(f"{fixture['story']}: 132/3, {sum(b['runs'] for b in fixture['commentary'])} window runs; current batters {fixture['active_batters']}")

if __name__=='__main__':main()
