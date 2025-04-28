import os
import json
from datetime import datetime

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

def update_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_today_string():
    return datetime.now().strftime("%Y%m%d")
