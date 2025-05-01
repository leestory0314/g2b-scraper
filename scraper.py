import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from utils.popup_handler import force_remove_popups
from utils.search import search_bids
from utils.excel_handler import save_to_excel
from utils.config_handler import load_config, save_config
from utils.keyword_loader import load_keywords

def run_scraper():
    now = datetime.now()
    log_dir = f"./logs/{now.strftime('%Y-%m-%d')}"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"log_{now.strftime('%Y%m%d_%H%M%S')}.txt")

    # 로그 이중 출력 설정
    class DualLogger:
        def __init__(self, path):
            self.terminal = sys.stdout
            self.log = open(path, "w", encoding="utf-8")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            self.terminal.flush()
            self.log.flush()

    sys.stdout = DualLogger(log_path)

    print(f"🗓️ 검색 시작일: {now.strftime('%Y-%m-%d')}\n")

    config_path = "./config.json"
    keywords_path = "./keywords.txt"

    # ✅ 수정 포인트: 인자 명시
    config = load_config(config_path)
    keywords = load_keywords(keywords_path)
    last_run_time = config.get("last_run_time")

    chrome_driver_path = "./chromedriver.exe"
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.g2b.go.kr")
        print("🌐 사이트 접속 완료")

        force_remove_popups(driver)

        all_results, new_last_run = search_bids(driver, wait, keywords, last_run_time)

        save_dir = f"./result/{now.strftime('%Y-%m-%d')}"
        save_filename = f"입찰공고검색_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
        save_to_excel(all_results, save_dir, save_filename)

        config["last_run_time"] = new_last_run
        save_config(config, config_path)

    finally:
        driver.quit()
        print("✅ 브라우저 종료 완료")
