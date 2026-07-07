import json
from pathlib import Path

import requests

REPO = "infiniflow/ragflow"
OUT = Path("badges/docker-pulls.json")
CACHE_FILE = Path("badges/docker-pulls-count.txt")

def fetch_pull_count(repo: str) -> int:
    url = f"https://hub.docker.com/v2/repositories/{repo}/"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    return int(data.get("pull_count", 0))

def load_previous_count() -> int:
    if CACHE_FILE.exists():
        try:
            return int(CACHE_FILE.read_text().strip())
        except Exception:
            return 0
    return 0

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    previous = load_previous_count()
    try:
        pulls = fetch_pull_count(REPO)
    except Exception:
        pulls = previous

    CACHE_FILE.write_text(str(pulls), encoding="utf-8")

    payload = {
        "schemaVersion": 1,
        "label": "docker pulls",
        "message": f"{pulls:,}",
        "color": "blue",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
