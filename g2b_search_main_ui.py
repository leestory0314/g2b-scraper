from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def close_all_popups(driver):
    """팝업을 모두 닫는다 (메인 화면 + iframe 포함, 다중 대응)"""
    def try_click(el):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            driver.execute_script("arguments[0].click();", el)
            print("✅ 팝업 닫기 성공 (JS 클릭)")
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ 닫기 실패: {e}")

    print("🔍 팝업 닫기 시도 중...")

    # 1. 메인 화면
    candidates = driver.find_elements(By.XPATH, "//*[contains(text(), '닫기') or contains(text(), '×') or contains(@alt, '닫기') or contains(@title, '닫기')]")
    for el in candidates:
        if el.is_displayed():
            try_click(el)

    # 2. iframe 내
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"🔍 iframe 개수: {len(iframes)}")
    for i, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            print(f"➡ iframe {i} 진입")
            candidates = driver.find_elements(By.XPATH, "//*[contains(text(), '닫기') or contains(text(), '×') or contains(@alt, '닫기') or contains(@title, '닫기')]")
            for el in candidates:
                if el.is_displayed():
                    try_click(el)
            driver.switch_to.default_content()
        except:
            driver.switch_to.default_content()
            continue

# 크롬 드라이버 설정
chrome_driver_path = "./chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
wait = WebDriverWait(driver, 15)

try:
    # 1. 사이트 접속
    driver.get("https://www.g2b.go.kr")
    print("🌐 사이트 접속 완료")
    time.sleep(2)

    # 2. 팝업 닫기 시도
    close_all_popups(driver)

    # 3. 입찰 > 입찰공고 메뉴 클릭
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='입찰']")))
    ActionChains(driver).move_to_element(menu).click().perform()
    print("📂 입찰 메뉴 클릭")

    submenu = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "입찰공고")))
    submenu.click()
    print("🧾 입찰공고 클릭 완료")
    time.sleep(3)

    # 4. iframe 전환 후 검색
    driver.switch_to.frame("sub")

    keywords = ["인공지능", "클라우드", "데이터 분석"]
    for keyword in keywords:
        print(f"\n🔍 검색어: {keyword}")

        input_box = driver.find_element(By.ID, "bidNm")
        input_box.clear()
        input_box.send_keys(keyword)

        search_btn = driver.find_element(By.XPATH, "//a[contains(text(), '검색')]")
        search_btn.click()
        time.sleep(3)

        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if not rows:
            print("  👉 결과 없음")
            continue

        for i, row in enumerate(rows[:3]):
            try:
                title_tag = row.find_element(By.CSS_SELECTOR, "td:nth-child(4) a")
                title = title_tag.text.strip()
                link = title_tag.get_attribute("href")
                print(f"  [{i+1}] {title}\n  🔗 {link}")
            except:
                continue

finally:
    driver.quit()
    print("✅ 브라우저 종료")
