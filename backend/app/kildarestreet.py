import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KILDARESTREET_API_KEY")
BASE_URL = "https://www.kildarestreet.com/api/"
MAX_SPEECHES = 20


async def get_politician_id(name: str) -> str | None:
    params = {"key": API_KEY, "output": "json", "search": name}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL + "getMP", params=params)
        resp.raise_for_status()
        data = resp.json()

    # KildareStreet returns a list of matches
    if not data:
        return None
    return data[0].get("person_id") or data[0].get("id")


async def get_debates(politician_id: str) -> list[dict]:
    params = {"key": API_KEY, "output": "json", "id": politician_id, "num": MAX_SPEECHES}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL + "getDebates", params=params)
        resp.raise_for_status()
        data = resp.json()

    speeches = []
    for item in data:
        text = item.get("body") or item.get("text") or ""
        if text:
            speeches.append({
                "text": text,
                "date": item.get("hdate", ""),
                "url": item.get("url", ""),
            })
    return speeches
