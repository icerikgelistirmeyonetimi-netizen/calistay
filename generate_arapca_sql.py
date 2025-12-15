import pandas as pd
import os
import re

# Dosyayı bul
files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'Arap' in f and not f.startswith('~$')]
file_path = files[0] if files else None

if not file_path:
    print("Dosya bulunamadı!")
    exit(1)

print(f"Dosya: {file_path}")

# Excel'i oku
df = pd.read_excel(file_path, sheet_name=0)
print(f"Toplam satır: {len(df)}")

# SQL çıktı dosyası
sql_output = []
sql_output.append("-- Arapça içerik eşleme verileri")
sql_output.append("-- Otomatik oluşturuldu")
sql_output.append("")

def escape_sql(val):
    """SQL için string escape"""
    if pd.isna(val) or val is None:
        return "NULL"
    val = str(val).strip()
    if not val:
        return "NULL"
    # Tek tırnak escape
    val = val.replace("'", "''")
    # Newline karakterlerini koru
    val = val.replace("\n", "\\n")
    return f"'{val}'"

# Her satır için INSERT oluştur
for idx, row in df.iterrows():
    ders_adi = row.get('Ders Adı', '')
    unite = row.get('Ünite/Öğrenme Alanı', '')
    kazanim = row.get('Kazanım/Öğrenme Çıktısı/Bölüm', '')
    
    # Boş satırları atla
    if pd.isna(ders_adi) or not str(ders_adi).strip():
        continue
    
    # Sınıf bilgisi - Arapça için 10. sınıf gibi görünüyor (kazanımlardan anlıyoruz 10.1.x.x)
    # Kazanımın başındaki numaradan sınıf çıkarabiliriz
    sinif = "10. Sınıf"  # Varsayılan
    if kazanim and not pd.isna(kazanim):
        match = re.match(r'^(\d+)\.', str(kazanim))
        if match:
            sinif_no = match.group(1)
            sinif = f"{sinif_no}. Sınıf"
    
    # GM bilgisi - Din Öğretimi Genel Müdürlüğü (Arapça dersi)
    gm = "Din Öğretimi Genel Müdürlüğü"
    
    # İçerik türü - Kazanım
    icerik_turu = "Kazanım"
    
    sql = f"""INSERT INTO icerik_kayitlari (ders_adi, sinif, unite, kazanim, aciklama, icerik_turu, gm, katilimci) VALUES ({escape_sql(ders_adi)}, {escape_sql(sinif)}, {escape_sql(unite)}, {escape_sql(kazanim)}, NULL, {escape_sql(icerik_turu)}, {escape_sql(gm)}, NULL);"""
    
    sql_output.append(sql)

# SQL dosyasını kaydet
with open('import_arapca.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_output))

print(f"\nToplam {len(sql_output) - 3} INSERT oluşturuldu")
print("Dosya: import_arapca.sql")

# Önizleme
print("\nÖnizleme (ilk 3 INSERT):")
for line in sql_output[3:6]:
    print(line[:200] + "..." if len(line) > 200 else line)
