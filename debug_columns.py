import pandas as pd
import glob

excel_files = glob.glob("*.xlsx")
excel_path = [f for f in excel_files if not f.startswith('~$')][0]

xl_file = pd.ExcelFile(excel_path, engine='openpyxl')

for sheet_name in xl_file.sheet_names[:5]:
    df_sheet = pd.read_excel(xl_file, sheet_name=sheet_name, engine='openpyxl')
    
    # Temizlik öncesi
    print(f"\n{sheet_name} - ÖNCESİ:")
    unite_cols = [col for col in df_sheet.columns if 'ÜNİTE' in str(col)]
    print(f"  Ünite sütunları: {unite_cols}")
    
    # Temizlik
    new_columns = []
    for col in df_sheet.columns:
        if isinstance(col, str):
            cleaned = ' '.join(col.split())
            new_columns.append(cleaned)
        else:
            new_columns.append(col)
    df_sheet.columns = new_columns
    
    # Temizlik sonrası
    print(f"{sheet_name} - SONRASI:")
    unite_cols = [col for col in df_sheet.columns if 'ÜNİTE' in str(col)]
    print(f"  Ünite sütunları: {unite_cols}")
    print(f"  'ÜNİTE/TEMA/ÖĞRENME ALANI' var mı? {'ÜNİTE/TEMA/ÖĞRENME ALANI' in df_sheet.columns}")
