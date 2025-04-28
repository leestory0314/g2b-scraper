import pandas as pd

def save_to_excel(data_by_keyword, file_path):
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for keyword, data in data_by_keyword.items():
            if not data:
                continue
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=keyword[:31], index=False)
