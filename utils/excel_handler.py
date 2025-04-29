# utils/excel_handler.py
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

def save_to_excel(results, save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    # 키워드별로 그룹핑
    keyword_groups = {}
    for record in results:
        keyword = record.get('키워드', 'Unknown')
        keyword_groups.setdefault(keyword, []).append(record)

    # 키워드별 시트 저장
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for keyword, records in keyword_groups.items():
            if not records:
                continue
            df = pd.DataFrame(records)
            sheet_name = keyword[:31] if keyword else "Unknown"  # 시트명은 최대 31자
            df.to_excel(writer, index=False, sheet_name=sheet_name)

    # 서식 적용
    wb = load_workbook(filepath)
    font = Font(name="맑은 고딕", size=10)

    for ws in wb.worksheets:
        # 폰트 적용
        for row in ws.iter_rows():
            for cell in row:
                cell.font = font

        # 열 너비 자동조정
        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(filepath)
    print(f"📁 엑셀 저장 완료 (키워드별 시트 분리): {filepath}")
