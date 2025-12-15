import os
from supabase import create_client

# Supabase bağlantısı
SUPABASE_URL = "https://fbeygjbqojwbfpxkukmz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZXlnamJxb2p3YmZweGt1a216Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzOTI4MDEsImV4cCI6MjA0ODk2ODgwMX0.T5d4fGDGVfRZDJjZHv-0HxvfJjGVU7Pz_egqvpFpRMc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Login tablosunu çek
response = supabase.table('login').select('*').order('full_name').execute()

# Txt dosyasına yaz
with open('login_kullanicilari.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("LOGIN KULLANICILARI\n")
    f.write("=" * 80 + "\n\n")
    
    for user in response.data:
        f.write(f"Tam Ad: {user['full_name']}\n")
        f.write(f"Kullanıcı Adı: {user['username']}\n")
        f.write(f"Şifre: {user['password']}\n")
        f.write(f"Oluşturulma: {user['created_at']}\n")
        f.write("-" * 80 + "\n")
    
    f.write(f"\nToplam {len(response.data)} kullanıcı\n")

print(f"✓ {len(response.data)} kullanıcı login_kullanicilari.txt dosyasına yazıldı")
