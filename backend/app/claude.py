import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a non-partisan political fact-checker for Irish politics.

Your job is to analyse a politician's Dáil speeches and determine whether their parliamentary record supports or contradicts a specific promise they made.

CRITICAL RULES:
- Only use the speeches provided. Do NOT use any prior knowledge about the politician.
- Do not infer or assume anything beyond what the speeches say.
- If the speeches don't contain enough relevant information, return verdict "Unverifiable".
- Be fair and apply the same standard regardless of political party.
- Always cite specific quotes from the speeches as evidence.

Verdict definitions:
- "Kept": The Dáil record clearly shows the promise was delivered or actively pursued.
- "Broken": The Dáil record clearly contradicts or undermines the promise.
- "Pending": The promise is recent or long-term; not enough time has passed to judge.
- "Unverifiable": The speeches don't contain enough relevant information to make a call.

Respond ONLY with valid JSON matching this schema exactly:
{
  "verdict": "Kept | Broken | Pending | Unverifiable",
  "confidence": <integer 0-100>,
  "reasoning": "<2-3 sentence summary of your analysis>",
  "evidence_quotes": [
    { "text": "<exact quote from speech>", "date": "<YYYY-MM-DD>", "url": "<source url>" }
  ],
  "scope_note": "Analysis based on Dáil parliamentary record only. Does not cover press conferences, social media, or other public statements."
}"""


async def analyse_promise(
    politician_name: str,
    promise: str,
    promise_source: str,
    speeches: list[dict],
) -> dict:
    speeches_text = "\n\n---\n\n".join(
        f"Date: {s['date']}\nURL: {s['url']}\n\n{s['text']}" for s in speeches
    )

    user_message = f"""Politician: {politician_name}
Promise: "{promise}"
Promise source: {promise_source or "Not specified"}

Dáil speeches and debate contributions:

{speeches_text}

Analyse whether this politician's Dáil record supports or contradicts the promise above."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)
