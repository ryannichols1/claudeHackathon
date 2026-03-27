# Promise Tracker — Claude Code Context

Built for the Claude Builders Society Hackathon (2026-03-28, 24hrs).
Track: Governance & Collaboration.

## What This Is

A civic accountability tool for Irish politics. User enters a politician's name and a promise — the app pulls their actual Dáil speeches from KildareStreet.com and passes them to Claude to analyse whether their parliamentary record supports or contradicts the promise. Every claim is cited back to the real Dáil debate record.

**Key differentiator:** Claude only uses the provided speeches — no prior knowledge, no hallucination beyond source material.

## Architecture

```
frontend/   React + TypeScript (port 3000)
backend/    Python + FastAPI (port 8000)
  app/
    main.py           — FastAPI app + CORS
    routes.py         — POST /check, GET /promises
    kildarestreet.py  — KildareStreet API integration
    claude.py         — Claude API call + structured output
    promises.py       — Load curated promises from JSON
  data/
    promises.json     — Curated politician promises (add more here)
```

## Verdict Schema (Claude output)

```json
{
  "verdict": "Kept | Broken | Pending | Unverifiable",
  "confidence": 0-100,
  "reasoning": "...",
  "evidence_quotes": [{ "text": "...", "date": "YYYY-MM-DD", "url": "..." }],
  "scope_note": "Based on Dáil parliamentary record only."
}
```

## Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in your API keys
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Environment Variables (backend/.env)
```
ANTHROPIC_API_KEY=       # get from console.anthropic.com
KILDARESTREET_API_KEY=   # request from kildarestreet.com/api
```

## Rules for Claude

- **Backend is Python only** — no switching to JS/TS for backend logic
- **Claude must be source-grounded** — never remove the "only use provided speeches" constraint from the system prompt in `claude.py`
- **Scope disclaimer must always be visible** in the UI — it's core to the ethics argument for judging
- **No auth, no user accounts** — out of scope for this hackathon
- **promises.json is the only promise store** — no database needed for the demo

## Judging Criteria (what matters)

1. **Ethics** — transparent sourcing, non-partisan, CC-licensed data, methodology shown
2. **Potential Risks** — hallucination mitigated by source-grounding, scope disclaimer always visible, same methodology for every TD
3. **Tech Functionality** — live KildareStreet API + Claude structured output, clickable citations
4. **Idea** — civic accountability for Irish politics, post-2024 election, no equivalent tool exists
5. **Presentation** — pick a well-known housing promise for the live demo, nail the pitch

---

## Checklist

### Setup (do first)
- [ ] Add all team members as collaborators on GitHub
- [ ] Everyone copies `.env.example` → `.env` and fills in keys
- [ ] Request KildareStreet API key at kildarestreet.com/api (may take time — do this NOW)
- [ ] Test `GET /promises` returns the curated list
- [ ] Test `POST /check` with a real politician name end-to-end

### Data
- [ ] Download Programme for Government 2025 PDF
- [ ] Extract 10–15 clean, specific promises → add to `backend/data/promises.json`
- [ ] Pick the demo promise (housing-related, well-documented in Dáil debates)

### Backend
- [ ] Verify KildareStreet `getMP()` resolves politician names correctly
- [ ] Verify `getDebates()` returns usable speech text
- [ ] Handle edge case: politician not found → clean 404 error
- [ ] Handle edge case: no speeches found → clean 404 error
- [ ] Test Claude output parses correctly as JSON (add try/except around json.loads)

### Frontend
- [ ] Promise list loads from `/promises` endpoint
- [ ] Check button hits `/check` and renders result card
- [ ] Verdict colours display correctly for all 4 verdicts
- [ ] Evidence quotes link back to KildareStreet source URLs
- [ ] Scope disclaimer always visible below results
- [ ] Error states handled gracefully

### Demo Prep
- [ ] Full end-to-end test with the chosen demo promise
- [ ] Pitch narrative written (problem → solution → demo → ethics → impact, ~2 mins)
- [ ] Slides or one-pager if needed

### Stretch (only if time)
- [ ] Side-by-side politician comparison
- [ ] Filter promises by category
- [ ] Party-level aggregation view

---

## Data Sources

- **KildareStreet.com** — Dáil debate transcripts, politician profiles. Free API, CC Attribution-ShareAlike 2.5. Cite as source.
- **Programme for Government 2025** — https://www.gov.ie/en/publication/5b1ff-programme-for-government-2025/
- **Party manifestos 2024** — available on FF, FG, SF official sites
