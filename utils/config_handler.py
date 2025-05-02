# utils/config_handler.py
# version: 1.1.0
# changelog:
# - v1.0.0: config.json load/save
# - v1.1.0: get_log_path(), get_result_path() 추가

import os
import json
from datetime import datetime

def load_config(config_path="./config.json"):
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config_path, config):
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def get_log_path(now: datetime):
    log_dir = f"./logs/{now.strftime('%Y-%m-%d')}"
    os.makedirs(log_dir, exist_ok=True)
    return f"{log_dir}/log_{now.strftime('%Y%m%d_%H%M%S')}.txt"

def get_result_path(now: datetime):
    result_dir = f"./result/{now.strftime('%Y-%m-%d')}"
    os.makedirs(result_dir, exist_ok=True)
    filename = f"입찰공고검색_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    return result_dir, filename
