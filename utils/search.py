# utils/search.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_bids(driver, wait, keywords):
    all_results = {}

    for keyword in keywords:
        print(f"\n🔍 검색어 입력: {keyword}")
        try:
            input_box = wait.until(EC.presence_of_element_located(
                (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")
            ))
            input_box.clear()
            input_box.send_keys(keyword)

            search_btn = wait.until(EC.element_to_be_clickable(
                (By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")
            ))
            search_btn.click()
            time.sleep(2)

            rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
            print(f"🧾 검색 결과: {len(rows)}건")
            results = []

            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    summary_btn = row.find_element(By.CSS_SELECTOR, "td[col_id='summary'] button")

                    # 툴팁 내용 추출
                    tooltip_html = summary_btn.get_attribute("outerHTML")
                    tooltip_data = extract_summary_tooltip(tooltip_html)

                    results.append({
                        "키워드": keyword,
                        "공고명": cells[6].text.strip(),
                        "공고번호": cells[5].text.strip(),
                        "용역구분": cells[1].text.strip(),
                        "공고기관": cells[7].text.strip(),
                        "수요기관": cells[8].text.strip(),
                        "게시일시": cells[9].text.strip().split("\n")[0],
                        "입찰마감일시": cells[9].text.strip().split("\n")[-1].replace("(", "").replace(")", ""),
                        **tooltip_data
                    })
                except Exception as e:
                    print(f"⚠️ 요약 툴팁 정보 없음 / 행 파싱 실패: {e}")
                    continue

            all_results[keyword] = results
        except Exception as e:
            print(f"❗ 검색 중 오류: {e}")
            all_results[keyword] = []

    return all_results

def extract_summary_tooltip(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    tooltip = {
        "배정예산": "", "추정가격": "", "낙찰방법": "", "재입찰": "",
        "국내/국제 입찰사유": "", "예가방법": "", "추첨번호공개여부": ""
    }

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if "배정예산" in text:
            tooltip["배정예산"] = text.split("배정예산 :")[-1].strip().replace("원", "")
        elif "추정가격" in text:
            tooltip["추정가격"] = text.split("추정가격 :")[-1].strip().replace("원", "")
        elif "낙찰방법" in text:
            tooltip["낙찰방법"] = text.split("낙찰방법 :")[-1].strip()
        elif "재입찰" in text:
            tooltip["재입찰"] = text.split("재입찰 :")[-1].strip()
        elif "국내/국제 입찰사유" in text:
            tooltip["국내/국제 입찰사유"] = text.split("국내/국제 입찰사유 :")[-1].strip()
        elif "예가방법" in text:
            tooltip["예가방법"] = text.split("예가방법 :")[-1].strip()
        elif "추첨번호공개여부" in text:
            tooltip["추첨번호공개여부"] = text.split("추첨번호공개여부 :")[-1].strip()

    return tooltip
