import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import setup_logger, create_directories, get_datetime_strings
from keywords import load_keywords
from tooltip import hover_and_parse_tooltip
from excel_writer import save_results_to_excel

def run_scraper(last_run_time: str = ""):
    now = datetime.now()
    log_path, result_path = create_directories(now)
    sys.stdout = setup_logger(log_path)

    driver = webdriver.Chrome(service=Service("./chromedriver.exe"))
    wait = WebDriverWait(driver, 20)

    keywords = load_keywords()

    driver.get("https://www.g2b.go.kr")
    time.sleep(10)

    try:
        driver.find_element(By.XPATH, "//span[text()='입찰공고목록']").click()
        time.sleep(3)

        input_box = wait.until(EC.presence_of_element_located((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")))
        search_btn = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")

        results = {}

        for keyword in keywords:
            input_box.clear()
            input_box.send_keys(keyword)
            search_btn.click()
            time.sleep(2)

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
            keyword_result = []

            for row in rows:
                try:
                    tds = row.find_elements(By.TAG_NAME, "td")
                    tooltip_elem = tds[-1]
                    tooltip_data = hover_and_parse_tooltip(driver, tooltip_elem, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_gridView1_tooltip")

                    keyword_result.append({
                        "키워드": keyword,
                        "공고명": tds[6].text.strip(),
                        "공고번호": tds[5].text.strip(),
                        "용역구분": tds[1].text.strip(),
                        "공고기관": tds[7].text.strip(),
                        "수요기관": tds[8].text.strip(),
                        "게시일시": tds[9].text.split("\n")[0].strip(),
                        "입찰마감일시": tds[9].text.split("\n")[1].replace("(", "").replace(")", "").strip(),
                        "배정예산": tooltip_data.get("배정예산", ""),
                        "추정가격": tooltip_data.get("추정가격", ""),
                        "낙찰방법": tooltip_data.get("낙찰방법", ""),
                        "재입찰": tooltip_data.get("재입찰", ""),
                        "국내/국제 입찰사유": tooltip_data.get("국내/국제 입찰사유", ""),
                        "예가방법": tooltip_data.get("예가방법", ""),
                        "추첨번호공개여부": tooltip_data.get("추첨번호공개여부", "")
                    })
                except Exception as e:
                    print(f"⚠️ 행 파싱 오류: {e}")
                    continue

            results[keyword] = keyword_result

        save_results_to_excel(results, result_path)

        return now.strftime("%Y%m%d%H%M%S")

    finally:
        driver.quit()
        print("✅ 브라우저 종료 완료")
