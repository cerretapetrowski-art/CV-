import json
import uuid
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))

HISTORY_FILE = DATA_DIR / "history.json"

def ensure_history_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("{}")

def get_user_id(request):
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

def add_record(user_id: str, image_name: str, results: list):
    ensure_history_file()
    data = json.loads(HISTORY_FILE.read_text())

    record = {
        "id": str(uuid.uuid4()),
        "image_name": image_name,
        "results": results,
        "time": datetime.now().isoformat()
    }

    if user_id not in data:
        data[user_id] = []
    data[user_id].insert(0, record)

    if len(data[user_id]) > 50:
        data[user_id] = data[user_id][:50]

    HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return record

def get_history(user_id: str, limit: int = 20):
    ensure_history_file()
    data = json.loads(HISTORY_FILE.read_text())
    records = data.get(user_id, [])[:limit]
    return records

def get_all_records():
    ensure_history_file()
    data = json.loads(HISTORY_FILE.read_text())
    return data
