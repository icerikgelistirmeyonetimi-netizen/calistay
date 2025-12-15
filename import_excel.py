import pandas as pd
from supabase import create_client, Client
import glob
import re

# Supabase bağlantı bilgileri
SUPABASE_URL = "https://ykmrystcfwjrrgkglyzr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDkzNDI4MiwiZXhwIjoyMDgwNTEwMjgyfQ.iNM-2kLLLRnuqNFxHQkIQk_Q8SEXfSPFNEQ1YoS6hbI"

# Supabase client oluştur
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Excel dosyasını bul
excel_all = [f for f in glob.glob("*.xlsx") if not f.startswith("~$")]
excel_files = [f for f in excel_all if f.lower().startswith("e-icerik-tablo-")]
if not excel_files:
    excel_files = excel_all
if not excel_files:
    print("Excel dosyası bulunamadı!")
    raise SystemExit(1)
excel_path = excel_files[0]
print(f"Excel dosyası: {excel_path}")

print("Excel dosyası okunuyor...")
xl_file = pd.ExcelFile(excel_path, engine='openpyxl')
print(f"Bulunan sekmeler: {xl_file.sheet_names}")

# Tüm sekmeleri oku ve birleştir
all_frames = []
for sheet_name in xl_file.sheet_names:
    df_sheet = pd.read_excel(xl_file, sheet_name=sheet_name, engine='openpyxl')

    # Sütun isimlerini normalize et (bazı dosyalarda araya fazladan boşluk girebiliyor)
    fixed_cols = []
    for col in df_sheet.columns:
        if isinstance(col, str):
            col2 = col.replace('ÜNİTE/TEMA/ ÖĞRENME ALANI', 'ÜNİTE/TEMA/ÖĞRENME ALANI')
            col2 = col2.replace('KAZANIM/ÖĞRENME ÇIKTISI/ BÖLÜM', 'KAZANIM/ÖĞRENME ÇIKTISI/BÖLÜM')
            fixed_cols.append(col2)
        else:
            fixed_cols.append(col)
    df_sheet.columns = fixed_cols

    # Sekme adını referans için tutalım
    df_sheet['ders_adi_sekme'] = sheet_name
    all_frames.append(df_sheet)

df = pd.concat(all_frames, ignore_index=True)
print(f"Toplam {len(df)} satır bulundu.")

# Sütun eşleştirmesi (veritabanı şemasına uygun)
column_mapping = {
    'E-İÇERİK TÜRÜ': 'icerik_turu',
    'ÜNİTE/TEMA/ÖĞRENME ALANI': 'unite',
    'KAZANIM/ÖĞRENME ÇIKTISI/BÖLÜM': 'kazanim',
    'AÇIKLAMA': 'aciklama',
    'DİĞER': 'diger_aciklama'
}
df = df.rename(columns=column_mapping)

# Ders adı ve sınıf ayrıştırma yardımcıları
def parse_from_sheet(sheet: str):
    if pd.isna(sheet):
        return None, None
    if sheet in ['Bilim Sanat', 'Türk İşaret Dili', 'OÖ Özel Eğitim', 'ÖE Uygulama', 'Sayfa5']:
        return sheet, None
    m = re.match(r'^(.*?)(\d+[-\d]*)$', str(sheet))
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return str(sheet), None

def split_ders_adi_tail_class(text: str):
    if pd.isna(text):
        return None, None
    s = str(text).strip()
    parts = s.rsplit(' ', 1)
    if len(parts) == 2 and parts[1].replace('-', '').isdigit():
        return parts[0].strip(), parts[1].strip()
    return s, None

# Önce sekmeden ders_adi/sinif çıkar
df[['ders_adi', 'sinif_sekme']] = df['ders_adi_sekme'].apply(lambda x: pd.Series(parse_from_sheet(x)))

# Eğer Excel'de "DERS ADI" sütunu varsa bundan da ayrıştır (sondaki sınıf numarasını al)
if 'DERS ADI' in df.columns:
    ders_parsed = df['DERS ADI'].apply(split_ders_adi_tail_class)
    df['ders_adi_excel'] = ders_parsed.apply(lambda t: t[0] if isinstance(t, tuple) else None)
    df['sinif_excel'] = ders_parsed.apply(lambda t: t[1] if isinstance(t, tuple) else None)

    # ders_adi: Öncelik Excel'deki temiz isimde, değilse sekmedeki isim
    df['ders_adi'] = df['ders_adi_excel'].fillna(df['ders_adi'])
    # sinif: Öncelik Excel'deki son parça, değilse sekmedeki sınıf
    df['sinif'] = df['sinif_excel'].fillna(df['sinif_sekme'])

    df = df.drop(columns=['ders_adi_excel', 'sinif_excel', 'sinif_sekme', 'DERS ADI'])
else:
    df['sinif'] = df['sinif_sekme']
    df = df.drop(columns=['sinif_sekme'])

df = df.drop(columns=['ders_adi_sekme'])

# Temizlik: string alanları trim et, anlamsız karakterleri kaldır
for col in ['ders_adi', 'sinif', 'unite', 'kazanim', 'aciklama', 'icerik_turu', 'diger_aciklama']:
    if col in df.columns:

        df[col] = df[col].apply(lambda x: str(x).replace('·', '').strip() if pd.notna(x) and str(x) != 'nan' else None if pd.isna(x) else x)

# Veritabanına yazılacak sütunlar
db_columns = ['ders_adi', 'sinif', 'unite', 'kazanim', 'aciklama', 'icerik_turu', 'diger_aciklama']
# Eksik sütunları None ile ekle
for col in db_columns:
    if col not in df.columns:
        df[col] = None
df = df[db_columns]

print("\n📋 Veritabanına aktarılacak sütunlar:")
print(db_columns)
print("Örnek ilk 3 satır:")
print(df.head(3))

# Kullanıcıdan onay al
response = input("\n⚠️  UYARI: icerik_kayitlari tablosu TRUNCATE edilecek ve Excel'den yeniden yüklenecek. Devam? (evet/hayir): ")
if response.lower() != 'evet':
    print("İşlem iptal edildi.")
    raise SystemExit(0)

print("\n1) Mevcut veriler siliniyor (TRUNCATE)...")
try:
    supabase.table('icerik_kayitlari').delete().neq('id', 0).execute()
    print("✓ Mevcut veriler silindi.")
except Exception as e:
    print(f"✗ Silme hatası: {e}")
    raise SystemExit(2)

print("\n2) Yeni veriler yükleniyor (batch)...")
records = df.to_dict('records')
batch_size = 100
success_count = 0
error_count = 0

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    # None olmayan değerleri bırak, NaN zaten None'a çevrilmiş durumda
    cleaned_batch = []
    for rec in batch:
        cleaned = {k: (None if (rec[k] is None or (isinstance(rec[k], float) and pd.isna(rec[k]))) else rec[k]) for k in db_columns}
        cleaned_batch.append(cleaned)
    try:
        supabase.table('icerik_kayitlari').insert(cleaned_batch).execute()
        success_count += len(cleaned_batch)
        print(f"  {success_count}/{len(records)} kayıt yüklendi...")
    except Exception as e:
        error_count += len(cleaned_batch)
        print(f"  ✗ Hata (batch {i//batch_size + 1}): {e}")

print("\n✓ İşlem tamamlandı!")
print(f"  Başarılı: {success_count}")
print(f"  Hatalı: {error_count}")
