import pandas as pd
from supabase import create_client, Client
import os

# Supabase bağlantı bilgileri
SUPABASE_URL = "https://ykmrystcfwjrrgkglyzr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDkzNDI4MiwiZXhwIjoyMDgwNTEwMjgyfQ.iNM-2kLLLRnuqNFxHQkIQk_Q8SEXfSPFNEQ1YoS6hbI"

# Supabase client oluştur
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Excel dosyasını oku
import glob
excel_files = glob.glob("*.xlsx")
if not excel_files:
    print("Excel dosyası bulunamadı!")
    exit()
excel_path = excel_files[0]
print(f"Excel dosyası: {excel_path}")

print("Excel dosyası okunuyor...")
# UTF-8 encoding ile oku
df = pd.read_excel(excel_path, engine='openpyxl')

print(f"Toplam {len(df)} satır bulundu.")
print("\nSütunlar:")
print(df.columns.tolist())
print("\nİlk 3 satır:")
print(df.head(3))

# Sütun eşleştirmesi
print("\n📋 Sütun eşleştirmesi:")
column_mapping = {
    'SIRA NO': 'sira_no',
    'DERS ADI': 'ders',
    'ÜNİTE/TEMA/ÖĞRENME ALANI': 'unite',
    'KAZANIM/ÖĞRENME ÇIKTISI/BÖLÜM': 'kazanim',
    'AÇIKLAMA': 'aciklama',
    'E-İÇERİK TÜRÜ': 'sinif',
    'DİĞER': 'diger_aciklama'
}
for old, new in column_mapping.items():
    print(f"  {old} → {new}")

# Sütunları yeniden adlandır
df = df.rename(columns=column_mapping)

# Sadece veritabanında olan sütunları tut
db_columns = ['sira_no', 'ders', 'unite', 'kazanim', 'aciklama', 'sinif', 'diger_aciklama']
df_filtered = df[db_columns]

# Kullanıcıdan onay al
response = input("\n⚠️  UYARI: Mevcut tüm veriler silinecek ve Excel'den yeniden yüklenecek. Devam etmek istiyor musunuz? (evet/hayir): ")

if response.lower() != 'evet':
    print("İşlem iptal edildi.")
    exit()

print("\n1. Mevcut veriler siliniyor...")
try:
    # Tüm kayıtları sil
    result = supabase.table('icerik_kayitlari').delete().neq('id', 0).execute()
    print("✓ Mevcut veriler silindi.")
except Exception as e:
    print(f"✗ Silme hatası: {e}")
    exit()

print("\n2. Yeni veriler yükleniyor...")

# DataFrame'i dictionary listesine çevir
records = df_filtered.to_dict('records')

# Batch insert (100'er kayıt)
batch_size = 100
success_count = 0
error_count = 0

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    
    # NaN değerlerini None'a çevir
    cleaned_batch = []
    for record in batch:
        cleaned_record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
        cleaned_batch.append(cleaned_record)
    
    try:
        result = supabase.table('icerik_kayitlari').insert(cleaned_batch).execute()
        success_count += len(batch)
        print(f"  {success_count}/{len(records)} kayıt yüklendi...")
    except Exception as e:
        error_count += len(batch)
        print(f"  ✗ Hata (batch {i//batch_size + 1}): {e}")

print(f"\n✓ İşlem tamamlandı!")
print(f"  Başarılı: {success_count}")
print(f"  Hatalı: {error_count}")
