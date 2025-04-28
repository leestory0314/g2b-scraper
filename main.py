from scraper import run_scraper
from utils.config_handler import load_config, save_config
from datetime import datetime

config = load_config()
last_run_time = config.get("last_run_time")

new_last_run = run_scraper(last_run_time)

# 실행 완료 후 최신 시간 갱신
config["last_run_time"] = new_last_run
save_config(config)
