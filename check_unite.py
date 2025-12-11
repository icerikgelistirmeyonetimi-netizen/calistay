import pandas as pd
import glob

excel_files = glob.glob("*.xlsx")
excel_path = [f for f in excel_files if not f.startswith('~$')][0]

df = pd.read_excel(excel_path, sheet_name='Arapça', engine='openpyxl')

print("Sütunlar:", df.columns.tolist())
print("\nİlk 10 satır ünite:")
print(df[['ÜNİTE/TEMA/ÖĞRENME ALANI']].head(10))
print(f"\nNaN/Boş sayısı: {df['ÜNİTE/TEMA/ÖĞRENME ALANI'].isna().sum()}")
print(f"Toplam satır: {len(df)}")
