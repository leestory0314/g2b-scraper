import json
import os
from datetime import datetime

CONFIG_PATH = "./config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")

def parse_last_run_time(raw_time: str):
    try:
        return datetime.strptime(raw_time, "%Y%m%d%H%M%S")
    except ValueError:
        try:
            return datetime.fromisoformat(raw_time)
        except Exception:
            return None
