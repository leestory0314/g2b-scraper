from scraper import run_scraper
from utils.config_handler import load_config, save_config

if __name__ == "__main__":
    config = load_config()
    last_run_time = config.get("last_run_time", None)

    new_last_run_time = run_scraper(last_run_time)
    config["last_run_time"] = new_last_run_time
    save_config(config)
