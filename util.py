import sys
import os
from datetime import datetime

class DualLogger:
    def __init__(self, path):
        self.terminal = sys.stdout
        self.log = open(path, "w", encoding="utf-8")
    def write(self, msg):
        self.terminal.write(msg)
        self.log.write(msg)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

def setup_logger(log_path):
    return DualLogger(log_path)

def get_datetime_strings():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%Y%m%d_%H%M%S")

def create_directories(now):
    date_str, time_str = get_datetime_strings()
    log_dir = f"./logs/{date_str}"
    result_dir = f"./result/{date_str}"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)
    log_path = f"{log_dir}/log_{time_str}.txt"
    return log_path, result_dir
