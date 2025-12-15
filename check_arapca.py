import pandas as pd
import os

# Dosyayı bul
files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'Arap' in f]
file_path = files[0] if files else None

if file_path:
    print(f"Dosya bulundu: {file_path}")
    
    # Sheet isimlerini listele
    xl = pd.ExcelFile(file_path)
    print(f"\nSheet sayısı: {len(xl.sheet_names)}")
    print("Sheet isimleri:")
    for i, sheet in enumerate(xl.sheet_names):
        print(f"  {i+1}. {sheet}")
    
    # İlk sheet'i oku ve sütunları göster
    df = pd.read_excel(file_path, sheet_name=0)
    print(f"\nİlk sheet: {xl.sheet_names[0]}")
    print(f"Satır sayısı: {len(df)}")
    print(f"\nSütunlar:")
    for col in df.columns:
        print(f"  - '{col}'")
    
    print(f"\nİlk 5 satır:")
    print(df.head(5).to_string())
else:
    print("Dosya bulunamadı!")
