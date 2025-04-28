from selenium.webdriver.common.by import By

def remove_popups(driver):
    selectors = [
        "div.popup", "div.popLayer", "div.pop_wrap", "div.w2window", "div.banner-wrap"
    ]
    for sel in selectors:
        try:
            for el in driver.find_elements(By.CSS_SELECTOR, sel):
                if el.is_displayed():
                    driver.execute_script("arguments[0].remove()", el)
        except:
            continue
