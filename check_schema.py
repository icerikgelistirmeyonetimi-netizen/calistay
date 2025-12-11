from supabase import create_client

SUPABASE_URL = "https://ykmrystcfwjrrgkglyzr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDkzNDI4MiwiZXhwIjoyMDgwNTEwMjgyfQ.iNM-2kLLLRnuqNFxHQkIQk_Q8SEXfSPFNEQ1YoS6hbI"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test insert
test_data = {
    'sinif': '1',
    'ders': 'Test',
    'unite': 'Test Unite',
    'kazanim': 'Test Kazanim',
    'aciklama': 'Test Aciklama'
}

try:
    result = supabase.table('icerik_kayitlari').insert(test_data).execute()
    print("✓ Test insert başarılı!")
    print("ID:", result.data[0]['id'])
    
    # Şimdi sil
    supabase.table('icerik_kayitlari').delete().eq('id', result.data[0]['id']).execute()
    print("✓ Test kaydı silindi")
except Exception as e:
    print(f"✗ Hata: {e}")
