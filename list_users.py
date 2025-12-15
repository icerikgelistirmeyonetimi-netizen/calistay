from supabase import create_client

SUPABASE_URL = "https://fbeygjbqojwbfpxkukmz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZXlnamJxb2p3YmZweGt1a216Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4MDg3NTQsImV4cCI6MjA0ODM4NDc1NH0.CKQ6tMDnYpH3RUWEVe-W2KOQhpb_lEipgjnD5r8lXrc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Login tablosundaki kullanicilar:\n")
print(f"{'Tam Ad':30} | {'Kullanici Adi':20} | Sifre")
print("-" * 75)

response = supabase.table('login').select('*').order('full_name').execute()

if response.data:
    for user in response.data:
        print(f"{user['full_name']:30} | {user['username']:20} | {user['password']}")
    print(f"\nToplam: {len(response.data)} kullanici")
else:
    print("Tabloda veri yok!")
