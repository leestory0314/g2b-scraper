# utils/search.py
from selenium.webdriver.common.by import By
import time

def search_bids(driver, keywords):
    results = []
    
    # 페이지당 100개 설정
    try:
        record_count_select = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_sbxRecordCountPerPage1")
        record_count_select.click()
        option_100 = driver.find_element(By.XPATH, "//select[@id='mf_wfm_container_tacBidPbancLst_contents_tab2_body_sbxRecordCountPerPage1']/option[text()='100']")
        option_100.click()
        time.sleep(2)
        print("✅ 검색 결과 표시 개수를 100개로 설정 완료")
    except Exception as e:
        print(f"⚠️ 검색 결과 표시 개수 설정 실패: {e}")

    input_box = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")
    search_button = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")

    for keyword in keywords:
        print(f"\n🔍 검색어 입력: {keyword}")
        input_box.clear()
        input_box.send_keys(keyword)
        search_button.click()
        time.sleep(3)

        rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
        print(f"🧾 검색 결과: {len(rows)}건")

        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                title = cells[6].text.strip()
                bid_no = cells[5].text.strip()
                service_type = cells[1].text.strip()
                agency = cells[7].text.strip()
                client = cells[8].text.strip()
                
                post_info = cells[9].text.strip()
                posted_date, deadline = post_info.split("\n") if "\n" in post_info else (post_info, "")

                # summary 버튼에서 툴팁 텍스트 읽기
                tooltip_data = {}
                try:
                    summary_button = cells[15].find_element(By.TAG_NAME, "button")
                    tooltip_text = summary_button.get_attribute("title") or summary_button.get_attribute("data-tooltip") or summary_button.text
                    
                    for line in tooltip_text.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            tooltip_data[key.strip()] = value.strip()
                except Exception as e:
                    print(f"⚠️ 요약정보 읽기 실패: {e}")

                result = {
                    "키워드": keyword,
                    "공고명": title,
                    "공고번호": bid_no,
                    "용역구분": service_type,
                    "공고기관": agency,
                    "수요기관": client,
                    "게시일시": posted_date.strip(),
                    "입찰마감일시": deadline.strip(),
                    "배정예산": tooltip_data.get("배정예산", ""),
                    "추정가격": tooltip_data.get("추정가격", ""),
                    "낙찰방법": tooltip_data.get("낙찰방법", ""),
                    "재입찰": tooltip_data.get("재입찰", ""),
                    "국내/국제 입찰사유": tooltip_data.get("국내/국제 입찰사유", ""),
                    "예가방법": tooltip_data.get("예가방법", ""),
                    "추첨번호공개여부": tooltip_data.get("추첨번호공개여부", "")
                }

                results.append(result)

            except Exception as e:
                print(f"⚠️ 행 파싱 실패: {e}")

    return results
