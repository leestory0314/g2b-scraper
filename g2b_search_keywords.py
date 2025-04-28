from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 🔧 1. 키워드 불러오기
with open("keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f.readlines() if line.strip()]

# 🔧 2. 크롬 드라이버 설정
chrome_driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')  # 테스트 시 꺼두세요

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    for keyword in keywords:
        # 3. 검색 페이지 새로 열기 (각 키워드마다 새로 시작)
        driver.get("https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCd=5")
        time.sleep(5)

        # 4. 키워드 입력 + 엔터
        input_box = driver.find_element(By.ID, "bidNm")
        input_box.clear()
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.ENTER)
        time.sleep(5)

        # 5. 결과 추출
        print(f"\n🔍 '{keyword}' 검색 결과:")
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        if not rows:
            print("  👉 결과 없음")
            continue

        for i, row in enumerate(rows[:3]):  # 상위 3개만 예시로 출력
            try:
                title_tag = row.find_element(By.CSS_SELECTOR, "td:nth-child(4) a")
                title = title_tag.text.strip()
                link = title_tag.get_attribute("href")
                print(f"  [{i+1}] {title}\n  🔗 {link}")
            except:
                continue

finally:
    driver.quit()
