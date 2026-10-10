# Dream11 assignment alignment

## Completed in the prototype
| Requirement / idea | Implementation |
| --- | --- |
| Solve a fan problem | Late joiners get tactical and emotional context beyond the current score. |
| Last five overs | Cricket-aware grouping with legal-ball handling, plus a three-over option. |
| Snappy three-bullet vibe check | Hidden squeeze, momentum shift, and what to watch next. |
| Show why a scorecard is insufficient | Same 132/3 scoreboard, but one scenario ends in a 22-run rookie-led over and another in a four-run spin over. |
| Explain rather than invent | Each takeaway links to specific commentary delivery IDs. |
| Contextual player filtering | Exactly the two batters at the crease and the bowler scheduled next. |
| Player background | Fictional debut year, experience, strengths, caution, and last-three-match form. |
| Fantasy Forte | Concise profile sentence grounded in supplied player data. |
| Match input | Match-ID entry and two selectable demo scenarios; unknown IDs get clear recovery. |
| Hindi fans | Persistent English/Hindi switch with translated commentary, takeaways, profiles, and controls. |
| High-fidelity UI | Light spatial hero, floating glass cards, cricket visual, over-by-over contrast, motion and accessible responsive layouts. |
| AI integration | LangChain structured output with OpenAI/Gemini, evidence-ID validation, timeouts and fallback. Both chains are tested with mocks. |
| Short note | submission_note.md contains a draft under 200 words with honest runtime status. |

## Required external setup before submission
- [x] Publish the source code, evaluator README, screenshots, and repository description to https://github.com/asadullah098/Catch-me-up. This is the source repository, not the deployed artifact URL.
- [x] Configure Gemini in backend/.env and verify successful English/Hindi generation: both live responses returned mode=gemini, three evidence-linked takeaways, and three player profiles. AI is requested by default. Repeat this verification after deploying.
- [ ] Publish frontend/backend with a working public HTTPS artifact link. Localhost is not a shareable submission link. A tested production page/API serving path and Dockerfile are prepared for one origin. If deploying frontend and backend separately, configure VITE_API_BASE and add the frontend origin to backend CORS.
- [ ] Replace the artifact URL in submission_note.md and describe the provider actually enabled.
- [ ] Submit the public URL and the note in the supplied Dream11 form after checking from another device. No submission has been made.

## Optional extension, not necessary for the focused demo
Connect a reliable live-commentary provider and verified player-history source. Arbitrary real match IDs are not supported today. The two scenarios and all player records are intentionally fictional, with visible labels. A licensed data adapter is preferable to relying on brittle page scraping.

## Demo sequence
Show 132/3 → read the rookie-led comeback → open its evidence → switch to the spin squeeze while the score stays the same → open Rehan's profile → switch to Hindi. This demonstrates the fan problem and the solution in about one minute.


