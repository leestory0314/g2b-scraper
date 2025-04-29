# scraper.py
import os
import sys
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.popup_handler import force_remove_popups
from utils.keyword_loader import load_keywords
from utils.excel_handler import save_to_excel
from utils.config_handler import load_config, save_config

# 로그 이중 출력
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

def run_scraper():
    now = datetime.now()

    # 🔵 config.json 로드
    config = load_config()
    last_run_time = config.get("last_run_time")

    # 🔵 로그 디렉토리 세팅
    log_dir = f"./logs/{now.strftime('%Y-%m-%d')}"
    os.makedirs(log_dir, exist_ok=True)
    log_path = f"{log_dir}/log_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    sys.stdout = DualLogger(log_path)

    print(f"🗓️ 검색 시작일: {now.strftime('%Y-%m-%d')}\n")

    # 🔵 크롬 드라이버 세팅
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    wait = WebDriverWait(driver, 20)

    # 🔵 키워드 로딩
    keywords = load_keywords()

    try:
        driver.get("https://www.g2b.go.kr")
        print("🌐 사이트 접속 완료")

        time.sleep(8)
        force_remove_popups(driver)

        # 입찰공고목록 클릭
        menus = driver.find_elements(By.XPATH, "//span[text()='입찰공고목록']")
        if menus:
            driver.execute_script("arguments[0].click();", menus[0])
            print("✅ 입찰공고목록 클릭 완료")
        else:
            print("❗ 입찰공고목록 클릭 실패")

        time.sleep(5)

        # 🔵 검색 결과 개수 설정
        try:
            select_box = wait.until(EC.presence_of_element_located((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_sbxRecordCountPerPage1")))
            driver.execute_script("arguments[0].value = '100'; arguments[0].dispatchEvent(new Event('change'));", select_box)
            print("✅ 검색 결과 표시 개수를 100개로 설정 완료")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ 검색 개수 설정 실패: {e}")

        # 🔵 검색 UI 구성
        input_box = wait.until(EC.presence_of_element_located((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")))
        search_btn = wait.until(EC.element_to_be_clickable((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")))

        # 🔵 검색 및 데이터 수집
        all_results = []
        for keyword in keywords:
            print(f"\n🔍 검색어 입력: {keyword}")
            input_box.clear()
            input_box.send_keys(keyword)
            search_btn.click()
            time.sleep(3)

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
            print(f"🧾 검색 결과: {len(rows)}건")

            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    # 데이터 추출
                    title = cells[6].text.strip()
                    post_info = cells[9].text.strip()
                    posted, deadline = post_info.split("\n") if "\n" in post_info else (post_info, "")

                    # 배정예산 등 요약정보 툴팁 추출
                    tooltip_div = row.find_element(By.CSS_SELECTOR, "td[col_id='summary'] div")
                    tooltip_text = tooltip_div.text
                    tooltip_data = extract_tooltip_data(tooltip_text)

                    all_results.append({
                        "키워드": keyword,
                        "공고명": title,
                        "공고번호": cells[5].text.strip(),
                        "용역구분": cells[1].text.strip(),
                        "공고기관": cells[7].text.strip(),
                        "수요기관": cells[8].text.strip(),
                        "게시일시": posted.strip(),
                        "입찰마감일시": deadline.replace("(", "").replace(")", "").strip(),
                        **tooltip_data,
                    })
                except Exception as e:
                    print(f"⚠️ 행 파싱 실패: {e}")
                    continue

    finally:
        driver.quit()
        print("✅ 브라우저 종료 완료")

    # 🔵 결과 저장
    save_dir = f"./result/{now.strftime('%Y-%m-%d')}"
    save_filename = f"입찰공고검색_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    save_to_excel(all_results, save_dir, save_filename)

    # 🔵 마지막 실행시간 업데이트
    config["last_run_time"] = now.strftime("%Y-%m-%dT%H:%M:%S")
    save_config(config)

    return now.strftime("%Y-%m-%dT%H:%M:%S")


def extract_tooltip_data(text):
    result = {
        "배정예산": "",
        "추정가격": "",
        "낙찰방법": "",
        "재입찰": "",
        "국내/국제 입찰사유": "",
        "예가방법": "",
        "추첨번호공개여부": ""
    }
    if not text:
        return result

    for line in text.split("\n"):
        if "배정예산" in line:
            result["배정예산"] = line.split(":")[-1].strip().replace("원", "")
        elif "추정가격" in line:
            result["추정가격"] = line.split(":")[-1].strip().replace("원", "")
        elif "낙찰방법" in line:
            result["낙찰방법"] = line.split(":")[-1].strip()
        elif "재입찰" in line:
            result["재입찰"] = line.split(":")[-1].strip()
        elif "국내/국제" in line:
            result["국내/국제 입찰사유"] = line.split(":")[-1].strip()
        elif "예가방법" in line:
            result["예가방법"] = line.split(":")[-1].strip()
        elif "추첨번호공개여부" in line:
            result["추첨번호공개여부"] = line.split(":")[-1].strip()

    return result
