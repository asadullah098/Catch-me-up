# Catch-Me-Up — Project Context

## Product and goals
Catch-Me-Up is a high-fidelity working prototype for Dream11's Forward Deployed Engineer Intern assignment. The email allows five days from receipt; the internal build target is four days. It helps fans joining a cricket match late understand the last five overs quickly, and helps casual fantasy fans assess unfamiliar players.

The core experience combines a snappy match “vibe check” with an Impact Players module containing concise “Fantasy Forte” summaries. Ground summaries in supplied commentary and player profiles; distinguish observations from inference and avoid invented statistics or guaranteed fantasy outcomes.

## Target audience
- Fans tuning in late who need the score, momentum, turning points, and current match context.
- Casual fantasy sports fans who need understandable player roles, strengths, recent impact, and relevant limitations.

## Prototype scope
Use two stable mock JSON scenarios with the same score (132/3) and different tactical stories for a dependable, rate-limit-free demo. Return exactly three evidence-linked vibe-check bullets. Profiles focus on the two batters at the crease and the bowler scheduled next, including experience, strengths, and computed recent form. Support persistent English/Hindi switching across summaries, controls, profiles, and evidence commentary. Support optional LangChain-powered generation through OpenAI or Gemini, with a deterministic mock response path when credentials or services are unavailable. Clearly label every match, player, and history as fictional. Live data integration is a future extension; public hosting and a real provider key are submission-readiness requirements.

## UI/UX mandate: Antigravity Design
Use a premium, spatial, weightless visual language rather than a generic dark AI terminal.
- Glassmorphism: subtle translucent surfaces, backdrop-filter blur, and semi-transparent borders; retain readable contrast and an opaque fallback.
- Weightlessness and depth: floating cards, layered soft diffused shadows, restrained elevation, and Z-axis layering.
- Motion and flow: staggered entrance animations, gentle transitions, and restrained hover lift; respect prefers-reduced-motion.
- Responsive layouts, visible keyboard focus, accessible controls, and legible typography are mandatory.
- Invoke and follow the UI/UX Pro Max skill before design-system generation. Define colors, typography, spacing, radii, shadows, glass surfaces, and motion tokens in Step 3.

## Proposed stack
- Frontend: React with Vite, Tailwind CSS, and Framer Motion. Next.js or GSAP may replace these if justified before setup.
- Backend: Python with FastAPI, LangChain, and an optional OpenAI or Gemini provider.
- Data: local mock JSON for match commentary, player profiles, and stable demo responses.
- Security/configuration: server-side provider keys via environment variables; commit only a placeholder environment example.

## Acceptance criteria
Users can open a demo match, catch up on its last five overs, and inspect Impact Players and Fantasy Forte summaries. Backend and frontend use a consistent response contract. The demo works without provider credentials, handles loading/empty/error states, and presents a polished responsive glass interface with staggered motion.

## Current state and authorization
Implementation authorized by the user on 10 October 2026: “now start the implementation and dont stop until external input is required.” Proceed through integration and polish. The implementation board is the source of truth for subsequent work.
