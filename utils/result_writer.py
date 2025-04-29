import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font

def save_to_excel(results, path):
    if not results:
        print("⚠️ 저장할 데이터가 없습니다.")
        return

    df = pd.DataFrame(results)
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='입찰공고목록', index=False)

        workbook = writer.book
        sheet = writer.sheets['입찰공고목록']

        for column_cells in sheet.columns:
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

        font = Font(name="맑은 고딕", size=10)
        for row in sheet.iter_rows():
            for cell in row:
                cell.font = font
                cell.alignment = Alignment(vertical="center", wrap_text=True)
