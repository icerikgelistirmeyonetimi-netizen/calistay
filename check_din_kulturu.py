import pandas as pd
import glob

excel_files = glob.glob("*.xlsx")
excel_path = [f for f in excel_files if not f.startswith('~$')][0]

df = pd.read_excel(excel_path, sheet_name='Din Kültürü ve Ahlak Bilgisi4-8', engine='openpyxl')

print("Sütunlar:", df.columns.tolist())
print("\nİlk 10 satır:")
for i, row in df.head(10).iterrows():
    print(f"{i}: DERS ADI={row.get('DERS ADI', 'YOK')}, ÜNİTE/TEMA/ÖĞRENME ALANI={row.get('ÜNİTE/TEMA/ÖĞRENME ALANI', 'YOK')}")
