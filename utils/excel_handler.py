# utils/excel_handler.py
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

def save_to_excel(all_results, save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    # ✅ 리스트인 경우 예외 처리
    if isinstance(all_results, list):
        all_results = {"검색결과": all_results}

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        empty = True
        for keyword, records in all_results.items():
            if not records:
                continue
            df = pd.DataFrame(records)
            if df.empty:
                continue
            df.to_excel(writer, index=False, sheet_name=keyword[:31])
            empty = False

        if empty:
            pd.DataFrame([{"메시지": "검색 결과 없음"}]).to_excel(writer, index=False, sheet_name="정보없음")

    # 서식 적용
    wb = load_workbook(filepath)
    font = Font(name="맑은 고딕", size=10)

    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                cell.font = font
        for col in ws.columns:
            max_len = max((len(str(cell.value)) if cell.value else 0 for cell in col), default=10)
            ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 2

    wb.save(filepath)
    print(f"📁 엑셀 저장 완료: {filepath}")
