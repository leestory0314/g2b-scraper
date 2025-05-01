import os
import json
from datetime import datetime

def load_config(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "last_run_time": (datetime.now().replace(day=1)).strftime("%Y-%m-%dT%H:%M:%S")
        }

def save_config(config, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
