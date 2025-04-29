# utils/popup_handler.py
from selenium.webdriver.common.by import By

def force_remove_popups(driver):
    popup_selectors = [
        "div.popup", "div.popLayer", "div.pop_wrap", "div.w2window", "div.banner-wrap"
    ]
    print("🔍 팝업 제거 시도")
    for selector in popup_selectors:
        try:
            for div in driver.find_elements(By.CSS_SELECTOR, selector):
                if div.is_displayed():
                    driver.execute_script("arguments[0].remove()", div)
                    print(f"✅ 팝업 제거됨: {selector}")
        except Exception as e:
            print(f"⚠️ 팝업 제거 실패: {selector} / {e}")
