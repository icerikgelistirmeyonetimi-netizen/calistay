import pandas as pd
import glob

excel_files = glob.glob("*.xlsx")
excel_path = [f for f in excel_files if not f.startswith('~$')][0]

xl_file = pd.ExcelFile(excel_path, engine='openpyxl')

for sheet_name in xl_file.sheet_names:
    df_sheet = pd.read_excel(xl_file, sheet_name=sheet_name, engine='openpyxl')
    
    has_unite = 'ÜNİTE/TEMA/ÖĞRENME ALANI' in df_sheet.columns
    
    if has_unite:
        nan_count = df_sheet['ÜNİTE/TEMA/ÖĞRENME ALANI'].isna().sum()
        total = len(df_sheet)
        print(f"{sheet_name}: ✓ Sütun var, {nan_count}/{total} boş")
    else:
        print(f"{sheet_name}: ✗ SÜTUN YOK! Sütunlar: {df_sheet.columns.tolist()[:5]}")
