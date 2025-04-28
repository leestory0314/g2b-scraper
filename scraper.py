import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import setup_logger
from utils.popup_handler import force_remove_popups
from utils.keyword_loader import load_keywords
from utils.config_handler import load_config, save_config, parse_last_run_time
from utils.result_writer import save_to_excel

def run_scraper(last_run_time: str):
    now = datetime.now()

    # 💡 날짜 파싱
    parsed_dt = parse_last_run_time(last_run_time)
    from_date = parsed_dt if parsed_dt else now.replace(day=1)

    log_path = setup_logger(now)
    print(f"[시작 시간] {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 🔍 키워드 불러오기
    keywords = load_keywords()
    print(f"[키워드 로딩 완료] 총 {len(keywords)}개")

    # 🔧 셀레니움 세팅
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    wait = WebDriverWait(driver, 20)

    all_results = {}

    try:
        driver.get("https://www.g2b.go.kr")
        time.sleep(8)
        force_remove_popups(driver)

        # 입찰공고목록 진입
        menus = driver.find_elements(By.XPATH, "//span[text()='입찰공고목록']")
        if menus:
            driver.execute_script("arguments[0].click();", menus[0])
            time.sleep(5)

        # 드롭다운 → 100건 보기
        try:
            selector = wait.until(EC.presence_of_element_located(
                (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_sbxRecordCountPerPage1")
            ))
            selector.send_keys("100")
            time.sleep(2)
        except:
            print("⚠️ 목록 수 조정 실패 (기본값 사용)")

        input_box = wait.until(EC.presence_of_element_located(
            (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")
        ))
        search_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")
        ))

        for keyword in keywords:
            print(f"\n🔍 검색어: {keyword}")
            input_box.clear()
            input_box.send_keys(keyword)
            search_btn.click()
            time.sleep(3)

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
            print(f"🔎 검색결과 행 수: {len(rows)}")

            results = []
            for i, row in enumerate(rows):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 15:
                        continue

                    공고명 = cells[6].text.strip()
                    공고번호 = cells[5].text.strip()
                    용역구분 = cells[1].text.strip()
                    공고기관 = cells[8].text.strip()
                    수요기관 = cells[7].text.strip()
                    게시일자, 마감일자 = "", ""
                    try:
                        post_info = cells[9].text.strip()
                        게시일자, 마감일자 = post_info.split("\n")
                    except:
                        게시일자 = post_info

                    # 금액 정보 추출 - 요약 버튼 툴팁
                    summary_button = row.find_element(By.CSS_SELECTOR, "td[col_id='summary'] button")
                    webdriver.ActionChains(driver).move_to_element(summary_button).perform()
                    time.sleep(0.5)

                    tooltip = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_gridView1_tooltip")
                    tip_lines = tooltip.text.split("\n")

                    def extract_tooltip(field_name):
                        for line in tip_lines:
                            if field_name in line:
                                return line.split(" : ")[-1].replace("원", "").strip()
                        return ""

                    배정예산 = extract_tooltip("배정예산")
                    추정가격 = extract_tooltip("추정가격")
                    낙찰방법 = extract_tooltip("낙찰방법")
                    재입찰 = extract_tooltip("재입찰")
                    입찰사유 = extract_tooltip("입찰사유")
                    예가방법 = extract_tooltip("예가방법")
                    추첨공개 = extract_tooltip("추첨번호공개여부")

                    results.append({
                        "키워드": keyword,
                        "공고명": 공고명,
                        "공고번호": 공고번호,
                        "용역구분": 용역구분,
                        "공고기관": 공고기관,
                        "수요기관": 수요기관,
                        "게시일시": 게시일자.strip(),
                        "입찰마감일시": 마감일자.strip(),
                        "배정예산": 배정예산,
                        "추정가격": 추정가격,
                        "낙찰방법": 낙찰방법,
                        "재입찰": 재입찰,
                        "국내/국제 입찰사유": 입찰사유,
                        "예가방법": 예가방법,
                        "추첨번호공개여부": 추첨공개
                    })

                except Exception as e:
                    print(f"⚠️ 행 파싱 실패 (index {i}): {e}")
                    continue

            if results:
                all_results[keyword] = results
            else:
                print(f"❗ 검색결과 없음: {keyword}")

    finally:
        driver.quit()
        print("✅ 브라우저 종료 완료")

    if all_results:
        save_to_excel(all_results, now)
        print("📁 엑셀 저장 완료")

    # 설정 저장
    config = load_config()
    config["last_run_time"] = now.strftime("%Y%m%d%H%M%S")
    save_config(config)
    return now.strftime("%Y%m%d%H%M%S")
