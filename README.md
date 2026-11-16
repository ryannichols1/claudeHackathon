# Promise Tracker

A civic accountability tool for Irish politics, built in 24 hours for the **Claude Builders Society Hackathon** (28 March 2026, Governance & Collaboration track).

Enter a politician and a promise they made. The app pulls their actual Dáil speeches from [KildareStreet.com](https://www.kildarestreet.com), passes them to Claude, and returns a verdict on whether their parliamentary record supports or contradicts the promise. Every claim links back to the real debate record.

## Design choices

- **Source-grounded:** Claude is only allowed to use the speeches it's given, with no prior knowledge, so it can't invent evidence.
- **Cited:** each verdict includes dated evidence quotes with links to the original debate.
- **Honest about scope:** every result carries a note that it's based on the Dáil record only.
- **Same method for everyone:** every politician goes through the same pipeline.

Verdicts are structured JSON: `Kept | Broken | Pending | Unverifiable`, a confidence score, reasoning, and evidence quotes with dates and URLs.

## Stack

| | |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React + TypeScript |
| AI | Anthropic API (structured output) |
| Data | KildareStreet API; curated promises in `backend/data/promises.json` |

## Running it

```bash
# Backend (http://localhost:8000)
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # add ANTHROPIC_API_KEY and KILDARESTREET_API_KEY
uvicorn app.main:app --reload

# Frontend (http://localhost:3000)
cd frontend
npm install
npm start
```

API: `GET /promises` lists the curated promises; `POST /check` analyses a politician and promise.

See [DESIGN.md](DESIGN.md) for the UI design and [CLAUDE.md](CLAUDE.md) for the project brief.
