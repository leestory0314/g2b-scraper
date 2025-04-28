from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1. 기본 설정
chrome_driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')  # 테스트 시 꺼두는 게 좋음

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 2. 나라장터 공고 리스트 페이지 열기
search_url = "https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCd=5"
driver.get(search_url)
time.sleep(3)

# 3. 공고명 입력창 찾기 → 키워드 입력 → 엔터
keyword = "인공지능"  # ← 원하는 키워드로 수정 가능
input_box = driver.find_element(By.ID, "bidNm")
input_box.send_keys(keyword)
input_box.send_keys(Keys.ENTER)
time.sleep(5)  # 검색 결과 대기

# 4. 결과 리스트에서 공고 제목/링크 추출
items = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

print(f"🔍 '{keyword}' 검색 결과:")
for item in items[:5]:  # 상위 5개만 출력
    try:
        title_tag = item.find_element(By.CSS_SELECTOR, "td:nth-child(4) a")
        title = title_tag.text.strip()
        link = title_tag.get_attribute("href")
        print(f"📌 {title}\n🔗 {link}\n")
    except:
        continue

# 5. 종료
driver.quit()
