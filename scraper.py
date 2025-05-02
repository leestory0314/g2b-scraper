# version: 3.0.2
# changelog:
# - v3.0.0: 기본 구조 설정, 모듈 분리
# - v3.0.1: 팝업 제거 및 로딩 대기 강화
# - v3.0.2: run_scraper 함수에 last_run_time 인자 추가 처리

import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from utils.popup_handler import wait_and_remove_popups
from utils.keyword_loader import load_keywords
from utils.search import search_bids
from utils.excel_handler import save_to_excel
from utils.logger import DualLogger
from utils.config_handler import load_config, save_config, get_log_path, get_result_path

def run_scraper(last_run_time=None):
    now = datetime.now()
    log_path = get_log_path(now)
    sys.stdout = DualLogger(log_path)
    print(f"🗓️ 검색 시작일: {now.strftime('%Y-%m-%d')}\n")

    # 브라우저 초기화
    chrome_driver_path = "./chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.g2b.go.kr")
        print("🌐 사이트 접속 완료")

        wait_and_remove_popups(driver, wait)

        config = load_config()
        keywords = load_keywords()
        all_results, new_last_run = search_bids(driver, wait, keywords, last_run_time)

        result_dir, result_file = get_result_path(now)
        save_to_excel(all_results, result_dir, result_file)

        config["last_run_time"] = new_last_run
        save_config(config)
        return new_last_run

    finally:
        driver.quit()
        print("✅ 브라우저 종료 완료")
