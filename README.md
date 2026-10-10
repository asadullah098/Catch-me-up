# Catch-Me-Up

**Every score has a story.**

Catch-Me-Up is a cricket companion for fans who join a match late. It explains the last five overs in three short takeaways and gives a quick introduction to the players shaping the next over. The whole experience is available in English and Hindi.

Built for the Dream11 Forward Deployed Engineer Intern assignment.

![Catch-Me-Up match story interface](docs/images/match-story.png)

## Why I built it

If I open a match at 132/3, I know the score—but I still don't know what I've missed. Has the batting side recovered from a collapse? Is a particular bowler controlling the chase? Who is the new player at the crease?

I wanted a late-arriving fan to understand those things in about 20 seconds, without reading every ball or searching for player stats separately.

## Same score, different game

The demo has two fictional match scenarios. In both, India is **132/3 after 15 overs, chasing 187**.

| Story | What happened |
| --- | --- |
| **The comeback** | Two wickets put the chase under pressure, then a newcomer leads a 22-run over. |
| **The spin squeeze** | The score looks identical, but a four-run over and pressure against spin tell a different story. |

That comparison is the core of the project: a scorecard gives the numbers; Catch-Me-Up explains how the game got there.

## What fans get

- **A three-point match story**, covering the momentum shift, the current pressure, and what to watch next.
- **Commentary behind each takeaway**, so fans can open the deliveries that support it.
- **Impact Players**, limited to the two current batters and the bowler scheduled next. Each card explains experience, strengths, recent form, and Fantasy Forte.
- **English and Hindi**, including the commentary and AI-generated player context.
- **A player shortlist**, role filters, and expandable backgrounds.
- **Three- or five-over windows**, with an over-by-over scoring view and spin-versus-pace context.

![Impact Player cards](docs/images/impact-players.png)

## How it works

FastAPI selects the commentary window and calculates the match statistics. LangChain sends that context and the relevant player profiles to Gemini, which returns the takeaways and player summaries in a structured format. The backend checks the response schema, player IDs, and commentary references before returning it to React.

```text
Commentary + player profiles
            ↓
Over selection and calculated statistics
            ↓
LangChain + Gemini
            ↓
Structured response and reference validation
            ↓
Match story + Impact Players
```

Extras stay with their correct over, rather than selecting a fixed number of commentary entries. Recent player form is calculated from the supplied appearances.

AI generation runs when a match loads or the language or over window changes. The **Catch me up** button generates a fresh summary. If the provider is unavailable, the app shows a prepared summary with its fallback status.

## A few deliberate choices

**Keep the data repeatable.** The two snapshots, player histories, and form records are fictional. That makes the same-score comparison easy to demonstrate. Gemini generates the analysis from those inputs; the app isn't connected to a live sports feed. Player portraits are also generated images of fictional characters.

**Keep player context focused.** A full squad adds noise for someone joining late. The three featured players are the ones relevant to the immediate situation.

**Show the source.** Takeaways link back to commentary. The backend validates those references, although a valid reference alone cannot guarantee that every generated sentence is accurate.

**Make Hindi part of the experience.** The language switch covers the full flow and persists across reloads.

The interface uses a light palette, glass cards, soft shadows, and subtle entrance animations. It supports narrow screens, keyboard navigation, and reduced motion.

## Tech stack

| Part | Tools |
| --- | --- |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Framer Motion |
| Backend | Python, FastAPI, Pydantic |
| AI | Gemini through LangChain; optional OpenAI integration |
| Tests | pytest, Playwright, axe-core |
| Packaging | Docker; frontend and API served together by FastAPI |

## Local development

Requires Node.js 22+ and Python 3.12+. These commands use PowerShell.

```powershell
git clone https://github.com/asadullah098/Catch-me-up.git
cd Catch-me-up
npm.cmd ci
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.lock.txt
Copy-Item backend/.env.example backend/.env
```

Provider configuration in `backend/.env`:

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
LLM_TIMEOUT_SECONDS=12
```

`GEMINI_MODEL` is configurable. `LLM_PROVIDER=mock` runs the prepared demo without an API key. Keys remain on the backend and environment files are excluded from Git.

Backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8012
```

Frontend, in another terminal:

```powershell
npm.cmd run dev
```

App: http://127.0.0.1:5180 · API docs: http://127.0.0.1:8012/docs

The demo match IDs are `ind-aus` and `spin-trap`.

## Docker

```powershell
docker build -t catch-me-up .
docker run --env-file backend/.env -p 8080:8080 catch-me-up
```

The container serves the frontend and API on the `PORT` environment variable, defaulting to 8080 locally. The health endpoint is `/api/health`. Provider configuration comes from runtime environment variables.

## Tests

```powershell
npm.cmd run build
.\.venv\Scripts\python.exe -m pytest backend/test_api.py -q
npx.cmd playwright install chromium
# Browser checks require both development servers.
npm.cmd run test:ui
node scripts/verify-artwork.mjs
```

The checks cover API behavior, evidence links, filters, shortlist persistence, Hindi, recovery states, keyboard access, reduced motion, and responsive layout. Browser tests use deterministic responses to avoid consuming API quota. Live Gemini generation has been checked separately in English and Hindi.

## AI tools used

Gemini and LangChain generate the match and player summaries. Codex assisted with implementation and UI iteration, and image generation was used for the fictional portraits.

This is an independent assignment prototype, not an official Dream11 product.
