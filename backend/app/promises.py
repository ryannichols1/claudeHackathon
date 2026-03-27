import json
import os

PROMISES_FILE = os.path.join(os.path.dirname(__file__), "../data/promises.json")


def get_all_promises() -> list[dict]:
    if not os.path.exists(PROMISES_FILE):
        return []
    with open(PROMISES_FILE) as f:
        return json.load(f)
