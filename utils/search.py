# utils/search.py
# version: 3.0.2
# changelog:
# - 툴팁 정보 dict에 포함 누락 문제 해결
# - 키워드별 rows 처리 고정값 사용 버그 수정

import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def search_bids(driver, wait, keywords, last_run_time=None):
    all_results = {}
    for keyword in keywords:
        print(f"\n🔍 검색어 입력: {keyword}")

        try:
            menu = driver.find_elements(By.XPATH, "//span[text()='입찰공고목록']")
            if menu:
                driver.execute_script("arguments[0].click();", menu[0])
                time.sleep(3)

            input_box = wait.until(EC.presence_of_element_located(
                (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")))
            search_btn = wait.until(EC.element_to_be_clickable(
                (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")))

            input_box.clear()
            input_box.send_keys(keyword)
            search_btn.click()
            time.sleep(3)

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
            print(f"🧾 검색 결과: {len(rows)}건")

            results = []
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    title = cells[6].text.strip()
                    number = cells[5].text.strip()
                    service_type = cells[1].text.strip()
                    org = cells[7].text.strip()
                    buyer = cells[8].text.strip()
                    post_info = cells[9].text.strip()
                    posted, deadline = post_info.split("\n") if "\n" in post_info else (post_info, "")

                    tooltip_data = {}
                    try:
                        summary_btn = cells[15].find_element(By.TAG_NAME, "button")
                        ActionChains(driver).move_to_element(summary_btn).perform()
                        time.sleep(0.5)
                        div = summary_btn.find_element(By.TAG_NAME, "div")
                        paragraphs = div.find_elements(By.TAG_NAME, "p")
                        for p in paragraphs:
                            text = p.text.strip()
                            if " : " in text:
                                k, v = text.split(" : ", 1)
                                tooltip_data[k.strip()] = v.strip().replace(",", "").replace("원", "")
                    except Exception as e:
                        print("⚠️ 요약 툴팁 정보 없음")

                    results.append({
                        "키워드": keyword,
                        "공고명": title,
                        "공고번호": number,
                        "용역구분": service_type,
                        "공고기관": org,
                        "수요기관": buyer,
                        "게시일시": posted.strip(),
                        "입찰마감일시": deadline.replace("(", "").replace(")", "").strip(),
                        "배정예산": tooltip_data.get("배정예산", ""),
                        "추정가격": tooltip_data.get("추정가격", ""),
                        "낙찰방법": tooltip_data.get("낙찰방법", ""),
                        "재입찰": tooltip_data.get("재입찰", ""),
                        "국내/국제 입찰사유": tooltip_data.get("국내/국제 입찰사유", ""),
                        "예가방법": tooltip_data.get("예가방법", ""),
                        "추첨번호공개여부": tooltip_data.get("추첨번호공개여부", "")
                    })

                except Exception as e:
                    print("⚠️ 행 파싱 실패:", e)
                    continue

            all_results[keyword] = results

        except Exception as e:
            print(f"❗ 검색 중 오류: {e}")
            continue

    return all_results, datetime.now().strftime("%Y%m%d%H%M%S")
