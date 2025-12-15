import sys
sys.stdout.reconfigure(encoding='utf-8')

from supabase import create_client
import random
import string

SUPABASE_URL = "https://fbeygjbqojwbfpxkukmz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZXlnamJxb2p3YmZweGt1a216Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4MDg3NTQsImV4cCI6MjA0ODM4NDc1NH0.CKQ6tMDnYpH3RUWEVe-W2KOQhpb_lEipgjnD5r8lXrc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_username(name):
    name = name.strip()
    if not name:
        return None
    
    parts = name.split()
    first_letter = parts[0][0].lower()
    last_word = parts[-1].lower()
    
    tr_map = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')
    first_letter = first_letter.translate(tr_map)
    last_word = last_word.translate(tr_map)
    
    return f"{first_letter}_{last_word}"

# Moderatörleri çek
print("Moderatorler cekiliyor...")
response = supabase.table('icerik_kayitlari').select('moderator').execute()

moderators = set()
for row in response.data:
    if row['moderator']:
        for m in row['moderator'].split(','):
            m = m.strip()
            if m:
                moderators.add(m)

print(f"{len(moderators)} moderator bulundu\n")

# Kullanıcıları oluştur
users = []
for mod in sorted(moderators):
    username = create_username(mod)
    if username:
        password = generate_password()
        users.append({
            'username': username,
            'password': password,
            'full_name': mod
        })
        print(f"{mod:30} -> {username:20} | {password}")

# Veritabanına ekle
print(f"\n{len(users)} kullanici login tablosuna ekleniyor...")

try:
    # Mevcut verileri sil
    supabase.table('login').delete().neq('id', 0).execute()
    
    # Yeni verileri ekle
    result = supabase.table('login').insert(users).execute()
    
    if result.data:
        print(f"\nBASARILI! {len(result.data)} kullanici eklendi!")
    else:
        print("\nHATA: Veri eklenemedi")
        
except Exception as e:
    print(f"\nHATA: {e}")
