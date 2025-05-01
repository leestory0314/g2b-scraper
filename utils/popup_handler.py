# utils/popup_handler.py
import time
from selenium.webdriver.common.by import By

def force_remove_popups(driver, retries=3, delay=2):
    popup_selectors = [
        "div.popup", "div.popLayer", "div.pop_wrap",
        "div.w2window", "div.banner-wrap"
    ]
    print("🔍 팝업 제거 시도")
    
    for i in range(retries):
        removed = False
        for selector in popup_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed():
                        driver.execute_script("arguments[0].remove();", el)
                        print(f"✅ 팝업 제거됨: {selector}")
                        removed = True
            except Exception as e:
                print(f"⚠️ 팝업 제거 실패: {selector} / {e}")
        if removed:
            time.sleep(delay)
        else:
            break
