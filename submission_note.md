# Submission note

Fans joining a cricket match late can see the score but miss the story: why momentum shifted, which bowling matchup is causing trouble, and who an unfamiliar player actually is.

Catch-Me-Up turns the last five overs of commentary into three short takeaways, each linked to its supporting deliveries. Two fictional scenarios show the same 132/3 score with very different contexts: a rookie-led comeback and a chase squeezed by spin. The player layer focuses on the two current batters and the next bowler, explaining their experience, strengths, and recent form. Fans can switch the complete experience between English and Hindi.

I used Codex to assist implementation and UI iteration. Gemini, connected through LangChain, generates the three takeaways and player summaries in English or Hindi from the supplied commentary and profiles. Responses use a validated schema and commentary evidence references. The match data is clearly labelled fictional; prepared summaries remain a fallback if the provider is unavailable. React and FastAPI deliver the interactive experience.
