# utils/popup_handler.py
# version: 1.1.0
# changelog:
# - v1.0.0: 기본 팝업 제거 함수
# - v1.1.0: 페이지 로딩 대기 후 팝업 제거 기능 통합

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def wait_and_remove_popups(driver, wait):
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("🔍 팝업 제거 시도")
        popup_selectors = [
            "div.w2window",
            "div.banner-wrap",
            "div[class*='popup']"
        ]
        for selector in popup_selectors:
            try:
                for elem in driver.find_elements(By.CSS_SELECTOR, selector):
                    if elem.is_displayed():
                        driver.execute_script("arguments[0].remove();", elem)
                        print(f"✅ 팝업 제거됨: {selector}")
            except Exception as e:
                print(f"⚠️ 팝업 제거 실패: {selector}")
    except Exception as e:
        print("❗ 페이지 로딩 실패 또는 팝업 제거 실패:", e)
