import pandas as pd
import glob

# Excel dosyasını oku
excel_files = glob.glob("*.xlsx")
excel_path = excel_files[0]
print(f"Excel dosyası: {excel_path}\n")

# Tüm sekmeleri oku
print("Excel dosyası okunuyor...")
xl_file = pd.ExcelFile(excel_path, engine='openpyxl')
print(f"Bulunan sekmeler: {xl_file.sheet_names}\n")

# Tüm sekmeleri birleştir
all_data = []
for sheet_name in xl_file.sheet_names:
    print(f"  Okuyorum: {sheet_name}")
    df_sheet = pd.read_excel(xl_file, sheet_name=sheet_name, engine='openpyxl')
    
    # Sütun isimlerini normalize et: 'ÜNİTE/TEMA/ ÖĞRENME ALANI' -> 'ÜNİTE/TEMA/ÖĞRENME ALANI'
    new_columns = []
    for col in df_sheet.columns:
        if isinstance(col, str):
            # Tüm boşlukları temizle, sonra / işaretlerinden ayır ve tek boşlukla birleştir
            cleaned = col.replace('ÜNİTE/TEMA/ ÖĞRENME ALANI', 'ÜNİTE/TEMA/ÖĞRENME ALANI')
            cleaned = cleaned.replace('KAZANIM/ÖĞRENME ÇIKTISI/ BÖLÜM', 'KAZANIM/ÖĞRENME ÇIKTISI/BÖLÜM')
            new_columns.append(cleaned)
        else:
            new_columns.append(col)
    df_sheet.columns = new_columns
    
    # Sekme ismini ders_adi_sekme olarak ekle
    df_sheet['ders_adi_sekme'] = sheet_name
    all_data.append(df_sheet)

df = pd.concat(all_data, ignore_index=True)
print(f"\nToplam {len(df)} satır bulundu.")

# Sütun eşleştirmesi - veritabanındaki gerçek sütun adlarına göre
column_mapping = {
    'E-İÇERİK TÜRÜ': 'icerik_turu',
    'ÜNİTE/TEMA/ÖĞRENME ALANI': 'unite',
    'KAZANIM/ÖĞRENME ÇIKTISI/BÖLÜM': 'kazanim',
    'AÇIKLAMA': 'aciklama',
    'DİĞER': 'diger_aciklama'
}

df = df.rename(columns=column_mapping)

# Ders adını sekme isminden al
# Sekme ismi "Din Kültürü ve Ahlak Bilgisi4-8" ise -> ders_adi: "Din Kültürü ve Ahlak Bilgisi", sinif: "4-8"
import re
def parse_sekme_ders_sinif(sekme_adi):
    if pd.isna(sekme_adi):
        return None, None
    
    # Özel durumlar
    if sekme_adi in ['Bilim Sanat', 'Türk İşaret Dili', 'OÖ Özel Eğitim', 'ÖE Uygulama', 'Sayfa5']:
        return sekme_adi, None
    
    # Regex ile son kısımdaki sayıları ayır
    # "Din Kültürü ve Ahlak Bilgisi4-8" -> "Din Kültürü ve Ahlak Bilgisi" + "4-8"
    # "Arapça" -> "Arapça" + None
    match = re.match(r'^(.+?)(\d+[-\d]*)$', sekme_adi)
    if match:
        ders = match.group(1).strip()
        sinif = match.group(2).strip()
        return ders, sinif
    else:
        return sekme_adi, None

df[['ders_adi', 'sinif_sekme']] = df['ders_adi_sekme'].apply(lambda x: pd.Series(parse_sekme_ders_sinif(x)))

# Eğer Excel'de DERS ADI sütunu varsa ve boş değilse, ondan da sınıf bilgisi alınabilir
if 'DERS ADI' in df.columns:
    def parse_excel_ders_sinif(ders_adi_tam):
        if pd.isna(ders_adi_tam):
            return None
        # Son kelime sayı mı kontrol et: "Arapça 2" -> "2"
        parts = str(ders_adi_tam).rsplit(' ', 1)
        if len(parts) == 2 and parts[1].replace('-', '').isdigit():
            return parts[1]
        return None
    
    df['sinif_excel'] = df['DERS ADI'].apply(parse_excel_ders_sinif)
    # Önce Excel'deki sınıf bilgisini kullan, yoksa sekmedekini kullan
    df['sinif'] = df['sinif_excel'].fillna(df['sinif_sekme'])
    df = df.drop(columns=['sinif_excel', 'sinif_sekme', 'DERS ADI'])
else:
    df['sinif'] = df['sinif_sekme']
    df = df.drop(columns=['sinif_sekme'])

df = df.drop(columns=['ders_adi_sekme'])

# Tüm string sütunlardaki · karakterini temizle ve baş/son boşlukları trim et
string_columns = ['ders_adi', 'sinif', 'unite', 'kazanim', 'aciklama', 'icerik_turu', 'diger_aciklama']
for col in string_columns:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: str(x).replace('·', '').strip() if pd.notna(x) and str(x) != 'nan' else x)

# Veritabanında olan sütunlar
db_columns = ['ders_adi', 'sinif', 'unite', 'kazanim', 'aciklama', 'icerik_turu', 'diger_aciklama']
df = df[db_columns]

# SQL dosyası oluştur
with open('import_data.sql', 'w', encoding='utf-8') as f:
    f.write("-- Mevcut verileri sil\n")
    f.write("TRUNCATE TABLE icerik_kayitlari RESTART IDENTITY CASCADE;\n\n")
    f.write("-- Yeni verileri ekle\n")
    
    for idx, row in df.iterrows():
        values = []
        for col in db_columns:
            val = row[col]
            if pd.isna(val):
                values.append('NULL')
            elif isinstance(val, str):
                # SQL injection koruması için tek tırnakları escape et
                escaped = val.replace("'", "''")
                values.append(f"'{escaped}'")
            else:
                values.append(f"'{val}'")
        
        sql = f"INSERT INTO icerik_kayitlari (ders_adi, sinif, unite, kazanim, aciklama, icerik_turu, diger_aciklama) VALUES ({', '.join(values)});\n"
        f.write(sql)

print("✓ SQL dosyası oluşturuldu: import_data.sql")
print(f"✓ Toplam {len(df)} satır SQL komutu hazırlandı")
print("\nSupabase Dashboard -> SQL Editor'da bu dosyayı açıp çalıştırabilirsiniz.")
