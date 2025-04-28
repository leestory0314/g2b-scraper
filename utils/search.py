from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_keyword(driver, keyword, from_date):
    wait = WebDriverWait(driver, 20)
    input_box = wait.until(EC.presence_of_element_located((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_bidPbancNm")))
    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")))
    per_page = Select(driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_sbxRecordCountPerPage1"))
    per_page.select_by_visible_text("100")

    input_box.clear()
    input_box.send_keys(keyword)
    search_btn.click()
    time.sleep(3)

    results = []
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody[id$='_body_gridView1_body_tbody'] > tr")
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            post_dt_raw = cells[9].text.split("\n")[0].replace("/", "").replace(":", "").replace(" ", "")
            if post_dt_raw <= from_date.strftime("%Y%m%d%H%M%S"):
                continue

            tooltip = row.find_element(By.CSS_SELECTOR, "td[col_id='summary'] div").text
            tooltip_dict = {}
            for line in tooltip.split("\n"):
                if " : " in line:
                    k, v = line.split(" : ", 1)
                    tooltip_dict[k.strip()] = v.strip().replace("원", "")

            results.append({
                "키워드": keyword,
                "공고명": cells[6].text.strip(),
                "공고번호": cells[5].text.strip(),
                "용역구분": cells[1].text.strip(),
                "공고기관": cells[7].text.strip(),
                "수요기관": cells[8].text.strip(),
                "게시일시": cells[9].text.split("\n")[0],
                "입찰마감일시": cells[9].text.split("\n")[1].strip("()") if "\n" in cells[9].text else "",
                "배정예산": tooltip_dict.get("배정예산", ""),
                "추정가격": tooltip_dict.get("추정가격", ""),
                "낙찰방법": tooltip_dict.get("낙찰방법", ""),
                "재입찰": tooltip_dict.get("재입찰", ""),
                "국내/국제 입찰사유": tooltip_dict.get("국내/국제 입찰사유", ""),
                "예가방법": tooltip_dict.get("예가방법", ""),
                "추첨번호공개여부": tooltip_dict.get("추첨번호공개여부", "")
            })

        except Exception as e:
            print(f"⚠️ 행 파싱 실패: {e}")
            continue
    return results
