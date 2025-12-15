import sys
from supabase import create_client
import random
import string

print("Script başlatılıyor...", flush=True)

# Supabase bağlantısı
SUPABASE_URL = "https://fbeygjbqojwbfpxkukmz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZXlnamJxb2p3YmZweGt1a216Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI4MDg3NTQsImV4cCI6MjA0ODM4NDc1NH0.CKQ6tMDnYpH3RUWEVe-W2KOQhpb_lEipgjnD5r8lXrc"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase bağlantısı kuruldu", flush=True)
except Exception as e:
    print(f"Supabase bağlantı hatası: {e}", flush=True)
    sys.exit(1)

def generate_random_password(length=8):
    """Rastgele şifre oluştur"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def create_username(full_name):
    """İsimden kullanıcı adı oluştur: ilk harf _ son kelime"""
    full_name = full_name.strip()
    if not full_name:
        return None
    
    parts = full_name.split()
    if len(parts) == 0:
        return None
    
    first_letter = parts[0][0].lower()
    last_word = parts[-1].lower()
    
    # Türkçe karakterleri değiştir
    turkish_map = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'c', 'Ğ': 'g', 'İ': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u'
    }
    
    for tr_char, en_char in turkish_map.items():
        first_letter = first_letter.replace(tr_char, en_char)
        last_word = last_word.replace(tr_char, en_char)
    
    return f"{first_letter}_{last_word}"

def main():
    print("Moderatörler çekiliyor...", flush=True)
    
    try:
        # Tüm moderatörleri çek
        response = supabase.table('icerik_kayitlari').select('moderator').execute()
        print(f"Sorgu sonucu: {len(response.data) if response.data else 0} satır", flush=True)
    except Exception as e:
        print(f"Veri çekme hatası: {e}", flush=True)
        return
    
    if not response.data:
        print("Veri bulunamadı!", flush=True)
        return
    
    # Benzersiz moderatörleri topla
    all_moderators = set()
    for row in response.data:
        if row['moderator']:
            # Virgülle ayrılmış isimleri ayır
            moderators = [m.strip() for m in row['moderator'].split(',')]
            all_moderators.update(moderators)
    
    # Boş veya geçersiz isimleri temizle
    all_moderators = {m for m in all_moderators if m}
    
    print(f"\n{len(all_moderators)} benzersiz moderatör bulundu:", flush=True)
    
    # Login tablosu için veriler hazırla
    login_data = []
    
    for moderator in sorted(all_moderators):
        username = create_username(moderator)
        if not username:
            continue
            
        password = generate_random_password()
        
        login_data.append({
            'username': username,
            'password': password,
            'full_name': moderator
        })
        
        print(f"  {moderator:30} -> Kullanıcı Adı: {username:20} Şifre: {password}", flush=True)
    
    if not login_data:
        print("\nEklenecek kullanıcı bulunamadı!", flush=True)
        return
    
    print(f"\n\n{len(login_data)} kullanıcı login tablosuna ekleniyor...", flush=True)
    
    # Verileri ekle
    try:
        # Önce mevcut verileri sil
        print("Mevcut veriler siliniyor...", flush=True)
        supabase.table('login').delete().neq('id', 0).execute()
        
        # Yeni verileri ekle
        print("Yeni veriler ekleniyor...", flush=True)
        response = supabase.table('login').insert(login_data).execute()
        
        if response.data:
            print(f"\n✓ {len(response.data)} kullanıcı başarıyla eklendi!", flush=True)
            print("\n=== KULLANICI LİSTESİ ===", flush=True)
            for user in sorted(response.data, key=lambda x: x['full_name']):
                print(f"{user['full_name']:30} | {user['username']:20} | {user['password']}", flush=True)
        else:
            print("\n✗ Kullanıcı eklenirken bir sorun oluştu!", flush=True)
            
    except Exception as e:
        print(f"\n✗ Hata: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
