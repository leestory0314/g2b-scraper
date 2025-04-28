import os
import sys
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔧 로그 저장 경로 및 파일명 지정
now = datetime.now()
log_dir = f"./logs/{now.strftime('%Y-%m-%d')}"
os.makedirs(log_dir, exist_ok=True)
log_path = f"{log_dir}/log_{now.strftime('%Y%m%d_%H%M%S')}.txt"

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

sys.stdout = DualLogger(log_path)

# 🔍 팝업 제거
def force_remove_popups(driver):
    popup_selectors = [
        "div.popup", "div.popLayer", "div.pop_wrap", "div.w2window", "div.banner-wrap"
    ]
    print("🔍 팝업 제거 시도")
    for selector in popup_selectors:
        try:
            for div in driver.find_elements(By.CSS_SELECTOR, selector):
                try:
                    if div.is_displayed():
                        driver.execute_script("arguments[0].remove()", div)
                        print(f"✅ 팝업 제거됨: {selector}")
                except:
                    continue
        except Exception as e:
            print(f"⚠️ 팝업 제거 실패: {selector} / {e}")

# 🔧 브라우저 세팅
chrome_driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
wait = WebDriverWait(driver, 20)

# 키워드 리스트 로드
with open("keyword.txt", encoding="utf-8") as f:
    keywords = [line.strip() for line in f.readlines() if line.strip()]

try:
    driver.get("https://www.g2b.go.kr")
    print("🌐 사이트 접속 완료")
    time.sleep(8)  # 전체 로딩 대기

    force_remove_popups(driver)

    # '입찰' 메뉴 오버 후 바로 '입찰공고목록' 클릭
    menus = driver.find_elements(By.XPATH, "//span[text()='입찰공고목록']")
    if menus:
        driver.execute_script("arguments[0].click();", menus[0])
        print("✅ 입찰공고목록 클릭 완료")

    time.sleep(5)  # 페이지 전환 대기

    # 검색 UI
    input_box = wait.until(EC.presence_of_element_located((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")))
    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")))
    print("✅ 검색 UI 구성 완료")

    for keyword in keywords:
        print(f"\n🔍 검색어: {keyword}")
        input_box.clear()
        input_box.send_keys(keyword)
        search_btn.click()
        time.sleep(3)

        rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
        print(f"🔎 검색결과 행 수: {len(rows)}")

        results = []
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                title = cells[6].text.strip()
                url = cells[6].find_element(By.TAG_NAME, "a").get_attribute("onclick")
                post_info = cells[9].text.strip()
                price_info = row.find_element(By.CSS_SELECTOR, "td[col_id='summary'] div").text
                budget_line = [line for line in price_info.split("\n") if "배정예산" in line]
                amount = budget_line[0].split("배정예산 : ")[-1] if budget_line else ""

                posted, deadline = post_info.split("\n") if "\n" in post_info else (post_info, "")
                results.append({
                    "키워드": keyword,
                    "공고명": title,
                    "게시일자": posted.strip(),
                    "마감일자": deadline.replace("(", "").replace(")", "").strip(),
                    "공고금액": amount.strip(),
                    "URL": url
                })
            except Exception as e:
                print(f"⚠️ 파싱 오류: {e}")
                continue

        if results:
            result_dir = f"./result/{now.strftime('%Y-%m-%d')}"
            os.makedirs(result_dir, exist_ok=True)
            result_path = f"{result_dir}/{keyword}_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
            df = pd.DataFrame(results)
            df.to_excel(result_path, index=False)
            print(f"📁 저장 완료: {result_path}")
        else:
            print(f"❗ 검색결과 없음: {keyword}")

finally:
    driver.quit()
    print("✅ 브라우저 종료 완료")
