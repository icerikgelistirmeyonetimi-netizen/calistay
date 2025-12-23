from supabase import create_client

SUPABASE_URL = "https://ykmrystcfwjrrgkglyzr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDkzNDI4MiwiZXhwIjoyMDgwNTEwMjgyfQ.iNM-2kLLLRnuqNFxHQkIQk_Q8SEXfSPFNEQ1YoS6hbI"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Kur'an-ı Kerim dersini 5-6-7-8 sınıfları için güncelle
result = supabase.table('icerik_kayitlari').update({
    'ders_adi': "Kur'an-ı Kerim 5-6-7-8"
}).eq('ders_adi', "Kur'an-ı Kerim").in_('sinif', ['5', '6', '7', '8']).execute()

print(f"Güncellenen kayıt sayısı: {len(result.data)}")
