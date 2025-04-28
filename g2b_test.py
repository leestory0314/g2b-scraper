from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 드라이버 경로
chrome_driver_path = "./chromedriver.exe"  # 이 경로 정확하게!

# 옵션 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 일단 주석 상태 유지 or 선택
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')  # ← 추가

# 드라이버 실행
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 페이지 접속
driver.get("https://www.g2b.go.kr/index.jsp")

# 대기 (페이지 로딩)
time.sleep(3)

# 출력
print("페이지 제목:", driver.title)

# 종료
driver.quit()
