"""
MEB TYMM Ortaöğretim Öğretim Programları Web Scraper
=====================================================
Bu script, MEB TYMM sitesinden ortaöğretim programlarını çeker ve
Supabase veritabanına kaydeder.

Akış:
1. Ana sayfa: #program-items -> Ders butonları
2. Ders sayfası: .container -> Sınıf düzeyleri (9, 10, 11, 12)
3. Sınıf sayfası: .featured-services -> Tema butonları
4. Tema sayfası: .article-details -> Ünite/kazanım verileri
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from supabase import create_client, Client

# Supabase bağlantı bilgileri
SUPABASE_URL = "https://ykmrystcfwjrrgkglyzr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrbXJ5c3RjZndqcnJna2dseXpyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzQyODIsImV4cCI6MjA4MDUxMDI4Mn0.T4yy_DqaDxilkAW8NMRbYiXiEyQNWknr04TD0sDC_R8"
# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Base URL
BASE_URL = "https://tymm.meb.gov.tr"

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_soup(url):
    """URL'den BeautifulSoup objesi döner"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Hata ({url}): {e}")
        return None


def get_dersler():
    """Ana sayfadan ders listesini çeker"""
    url = f"{BASE_URL}/ogretim-programlari/ortaogretim"
    soup = get_soup(url)
    
    if not soup:
        return []
    
    dersler = []
    program_items = soup.select("#program-items a")
    
    for item in program_items:
        href = item.get("href", "")
        ders_adi = item.get_text(strip=True)
        
        # Sadece ders linklerini al
        if "/ogretim-programlari/ders/" in href:
            full_url = href if href.startswith("http") else BASE_URL + href
            dersler.append({
                "ders_adi": ders_adi,
                "url": full_url
            })
    
    return dersler


def get_sinif_seviyeleri(ders_url):
    """Ders sayfasından sınıf seviyelerini çeker"""
    soup = get_soup(ders_url)
    
    if not soup:
        return []
    
    siniflar = []
    # Sınıf linkleri (.container içindeki linkler)
    container = soup.select(".container a")
    
    for link in container:
        href = link.get("href", "")
        text = link.get_text(strip=True)
        
        # Sınıf linklerini bul (9.Sınıf, 10.Sınıf vs.)
        if "Sınıf" in text or "sınıf" in text.lower():
            full_url = href if href.startswith("http") else BASE_URL + href
            
            # Sınıf numarasını çıkar
            sinif_match = re.search(r'(\d+)\.\s*[Ss]ınıf', text)
            sinif = sinif_match.group(1) if sinif_match else text
            
            siniflar.append({
                "sinif": sinif,
                "url": full_url
            })
    
    return siniflar


def get_temalar(sinif_url):
    """Sınıf sayfasından tema listesini çeker"""
    soup = get_soup(sinif_url)
    
    if not soup:
        return []
    
    temalar = []
    featured_services = soup.select(".featured-services a")
    
    for item in featured_services:
        href = item.get("href", "")
        tema_adi = item.get_text(strip=True)
        
        # Tema linklerini al
        if "/unite/" in href and tema_adi:
            full_url = href if href.startswith("http") else BASE_URL + href
            temalar.append({
                "tema_adi": tema_adi,
                "url": full_url
            })
    
    return temalar


def get_tema_detay(tema_url):
    """Tema sayfasından detayları çeker"""
    soup = get_soup(tema_url)
    
    if not soup:
        return None
    
    # article-details içeriği
    article_details = soup.select_one(".article-details")
    
    if not article_details:
        return None
    
    # HTML içeriği
    html_content = str(article_details)
    
    # Öğrenme çıktıları bölümünü bul
    kazanimlar = []
    
    # "Öğrenme Çıktıları ve Süreç Bileşenleri" başlığını bul
    ogrenme_section = None
    rows = soup.select(".row.border")
    
    for row in rows:
        title_div = row.select_one(".title")
        if title_div and "Öğrenme Çıktıları" in title_div.get_text():
            content_div = row.select_one(".content")
            if content_div:
                ogrenme_section = content_div
                break
    
    if ogrenme_section:
        # Tüm <p> taglarını bul
        paragraphs = ogrenme_section.find_all("p")
        
        # Ders tipini kontrol et
        # 1. İngilizce dersi mi? (ENG ile başlayan kazanımlar)
        # 2. Türk Dili mi? (TDE ile başlayan kazanımlar)
        is_english = False
        is_turk_dili = False
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            strong = p.find("strong")
            
            # İngilizce kontrolü (strong içinde ENG var)
            if strong and re.match(r'^\.?\s*ENG\.\d+', strong.get_text(strip=True)):
                is_english = True
                break
            
            # Türk Dili kontrolü (TDE kodları var, word boundary olmadan)
            if re.search(r'TDE\d+\.\d+\.', text):
                is_turk_dili = True
                break
        
        if is_turk_dili:
            # Türk Dili dersi için özel parse
            # Başlıklar: <strong> içinde (Metin Tahlili, Dinleme/İzleme vb.)
            # Kazanımlar: TDE1.1. ile başlar
            # Açıklamalar: a), b), c) ile başlar
            
            current_basliklar = []  # Aktif başlıkları tut
            current_kazanim = None
            current_aciklamalar = []
            
            for p in paragraphs:
                # <br> etiketlerini newline'a çevir
                for br in p.find_all("br"):
                    br.replace_with("\n")
                
                # Tüm metni al
                text = p.get_text()
                
                # Satır satır parse et
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                
                for line in lines:
                    # Strong başlık mı kontrol et (TDE ile başlamıyorsa)
                    if not line.startswith("TDE") and not re.match(r'^[a-zçğışüö]\)', line):
                        # Başlık olabilir
                        if "Metin Tahlili" in line or "Edebiyat Atölyesi" in line:
                            current_basliklar = [line]
                            continue
                        elif line in ["Dinleme/İzleme", "Okuma", "Konuşma", "Yazma"]:
                            # Alt başlık
                            if current_basliklar:
                                current_basliklar = [current_basliklar[0], line]
                            else:
                                current_basliklar = [line]
                            continue
                    
                    # Ana kazanım mı? (TDE1.1., TDE2.1. vb.)
                    kazanim_match = re.match(r'^(TDE\d+\.\d+\.)\s*(.+)', line)
                    
                    if kazanim_match:
                        # Önceki kazanımı kaydet
                        if current_kazanim:
                            kazanimlar.append({
                                "kazanim": current_kazanim,
                                "aciklama": "\n".join(current_aciklamalar)
                            })
                        
                        # Yeni kazanım başladı (başlıkları da ekle)
                        baslik_prefix = " - ".join(current_basliklar) + " - " if current_basliklar else ""
                        current_kazanim = baslik_prefix + line
                        current_aciklamalar = []
                        
                    # Açıklama mı? (a), b), c) ile başlar)
                    elif re.match(r'^[a-zçğışüö]\)', line):
                        if current_kazanim:
                            current_aciklamalar.append(line)
                    
                    # Devam eden açıklama (tırnak içinde veya önceki açıklamanın devamı)
                    elif current_kazanim and current_aciklamalar:
                        # Son açıklamaya ekle
                        if not line.startswith("TDE") and not any(line.startswith(x) for x in ["Metin Tahlili", "Edebiyat", "Dinleme", "Okuma", "Konuşma", "Yazma"]):
                            current_aciklamalar[-1] += " " + line
            
            # Son kazanımı kaydet
            if current_kazanim:
                kazanimlar.append({
                    "kazanim": current_kazanim,
                    "aciklama": "\n".join(current_aciklamalar)
                })
        
        elif is_english:
            # İngilizce dersi için özel parse
            # <p><strong>ENG.x.x.xx.</strong> Tüm metin...</p> -> Kazanım (tüm paragraf)
            # Sonraki <p> tagları (strong olmayan) -> Açıklama
            current_kazanim = None
            current_aciklamalar = []
            
            for p in paragraphs:
                strong = p.find("strong")
                full_text = p.get_text(strip=True)
                
                if strong:
                    strong_text = strong.get_text(strip=True)
                    # ENG ile başlayan kazanım kodu var mı?
                    if re.match(r'^\.?\s*ENG\.\d+', strong_text):
                        # Önceki kazanımı kaydet
                        if current_kazanim:
                            kazanimlar.append({
                                "kazanim": current_kazanim,
                                "aciklama": "\n".join(current_aciklamalar)
                            })
                        
                        # Yeni kazanım - tüm paragraf metni
                        current_kazanim = full_text
                        current_aciklamalar = []
                    else:
                        # Strong var ama ENG ile başlamıyor, açıklama olarak ekle
                        if current_kazanim and full_text:
                            current_aciklamalar.append(full_text)
                else:
                    # Strong yok, açıklama paragrafı
                    if current_kazanim and full_text:
                        current_aciklamalar.append(full_text)
            
            # Son kazanımı kaydet
            if current_kazanim:
                kazanimlar.append({
                    "kazanim": current_kazanim,
                    "aciklama": "\n".join(current_aciklamalar)
                })
        else:
            # Diğer dersler için mevcut parse (Türkçe dersler)
            for p in paragraphs:
                # <strong> tagları kazanımları içerir
                strongs = p.find_all("strong")
                
                for strong in strongs:
                    kazanim_text = strong.get_text(strip=True)
                    if kazanim_text:
                        # Kazanım kodunu kontrol et (örn: BİY.9.1.1.)
                        if re.match(r'^[A-ZÇĞİÖŞÜ]+\.\d+', kazanim_text):
                            # Açıklamaları bul (strong dışındaki metin)
                            # p tag'ının tam metnini al ve strong kısımlarını çıkar
                            full_text = p.get_text()
                            
                            # Strong'dan sonraki açıklamaları bul
                            aciklamalar = []
                            
                            # BR taglarından sonraki metinleri al
                            for content in p.children:
                                if content.name == "br":
                                    continue
                                elif content.name == "strong":
                                    continue
                                elif isinstance(content, str):
                                    text = content.strip()
                                    if text and text.startswith(('a)', 'b)', 'c)', 'ç)', 'd)', 'e)', 'f)')):
                                        aciklamalar.append(text)
                            
                            # Alternatif yöntem: Regex ile açıklamaları bul
                            if not aciklamalar:
                                pattern = r'[a-çd-f]\)\s*[^a-ç)]+(?=(?:[a-çd-f]\)|$))'
                                aciklama_text = full_text.replace(kazanim_text, "")
                                matches = re.findall(r'[a-fç]\)[^\n]+', aciklama_text)
                                aciklamalar = matches
                            
                            aciklama = "\n".join(aciklamalar) if aciklamalar else ""
                            
                            kazanimlar.append({
                                "kazanim": kazanim_text,
                                "aciklama": aciklama
                            })
    
    return {
        "html": html_content,
        "kazanimlar": kazanimlar
    }


def parse_kazanimlar_from_html(html_content):
    """HTML içeriğinden kazanımları ayrıştırır"""
    soup = BeautifulSoup(html_content, 'html.parser')
    kazanimlar = []
    
    # Tüm <p> taglarını bul
    paragraphs = soup.find_all("p")
    
    current_kazanim = None
    current_aciklamalar = []
    
    for p in paragraphs:
        text = p.get_text()
        strong = p.find("strong")
        
        if strong:
            # Önceki kazanımı kaydet
            if current_kazanim:
                kazanimlar.append({
                    "kazanim": current_kazanim,
                    "aciklama": "\n".join(current_aciklamalar)
                })
            
            # Yeni kazanım
            current_kazanim = strong.get_text(strip=True)
            current_aciklamalar = []
            
            # Strong dışındaki metni al
            for content in p.stripped_strings:
                content_text = str(content).strip()
                if content_text != current_kazanim:
                    # a), b), c) gibi maddeleri bul
                    if re.match(r'^[a-fç]\)', content_text):
                        current_aciklamalar.append(content_text)
        else:
            # Sadece açıklama içeren paragraf
            text = p.get_text(strip=True)
            if text and re.match(r'^[a-fç]\)', text):
                current_aciklamalar.append(text)
    
    # Son kazanımı kaydet
    if current_kazanim:
        kazanimlar.append({
            "kazanim": current_kazanim,
            "aciklama": "\n".join(current_aciklamalar)
        })
    
    return kazanimlar


def save_unite_bilgisi(unite_adi, html_content):
    """unite_bilgileri tablosuna kaydet ve ID döner"""
    try:
        # Önce mevcut kaydı kontrol et
        existing = supabase.table("unite_bilgileri").select("id").eq("unite_adi", unite_adi).execute()
        
        if existing.data:
            # Güncelle
            result = supabase.table("unite_bilgileri").update({
                "html": html_content
            }).eq("unite_adi", unite_adi).execute()
            return existing.data[0]["id"]
        else:
            # Yeni kayıt
            result = supabase.table("unite_bilgileri").insert({
                "unite_adi": unite_adi,
                "html": html_content
            }).execute()
            return result.data[0]["id"] if result.data else None
    except Exception as e:
        print(f"unite_bilgileri kaydetme hatası: {e}")
        return None


def save_icerik_kaydi(ders_adi, sinif, unite, kazanim, aciklama, unite_id):
    """icerik_kayitlari tablosuna kaydet"""
    try:
        # Mevcut kaydı kontrol et
        existing = supabase.table("icerik_kayitlari").select("id")\
            .eq("ders_adi", ders_adi)\
            .eq("sinif", sinif)\
            .eq("kazanim", kazanim).execute()
        
        data = {
            "ders_adi": ders_adi,
            "sinif": sinif,
            "unite": unite,
            "kazanim": kazanim,
            "aciklama": aciklama,
            "durum": True,
            "unite_id": unite_id,
            "gm": "Orta Öğretim Genel Müdürlüğü"
        }
        
        if existing.data:
            # Güncelle
            supabase.table("icerik_kayitlari").update(data).eq("id", existing.data[0]["id"]).execute()
            print(f"  Güncellendi: {kazanim[:50]}...")
        else:
            # Yeni kayıt
            supabase.table("icerik_kayitlari").insert(data).execute()
            print(f"  Eklendi: {kazanim[:50]}...")
        
        return True
    except Exception as e:
        print(f"icerik_kayitlari kaydetme hatası: {e}")
        return False


def scrape_all():
    """Tüm verileri çeker ve veritabanına kaydeder"""
    print("=" * 60)
    print("MEB TYMM Ortaöğretim Programları Scraper")
    print("=" * 60)
    
    # 1. Dersleri çek
    print("\n[1/4] Dersler çekiliyor...")
    dersler = get_dersler()
    dersler.reverse()  # Sondan başla (Türk Dili önce gelsin)
    print(f"Toplam {len(dersler)} ders bulundu.")
    
    for ders in dersler:
        print(f"\n{'='*60}")
        print(f"DERS: {ders['ders_adi']}")
        print(f"{'='*60}")
        
        # 2. Sınıf seviyelerini çek
        print("\n[2/4] Sınıf seviyeleri çekiliyor...")
        siniflar = get_sinif_seviyeleri(ders["url"])
        print(f"  {len(siniflar)} sınıf bulundu.")
        
        for sinif in siniflar:
            print(f"\n  SINIF: {sinif['sinif']}")
            
            # 3. Temaları çek
            print("  [3/4] Temalar çekiliyor...")
            temalar = get_temalar(sinif["url"])
            print(f"    {len(temalar)} tema bulundu.")
            
            for tema in temalar:
                print(f"\n    TEMA: {tema['tema_adi']}")
                
                # 4. Tema detaylarını çek
                print("    [4/4] Tema detayları çekiliyor...")
                detay = get_tema_detay(tema["url"])
                
                if detay:
                    # unite_bilgileri tablosuna kaydet
                    unite_id = save_unite_bilgisi(tema["tema_adi"], detay["html"])
                    print(f"      Unite ID: {unite_id}")
                    
                    # Kazanımları kaydet
                    kazanimlar = detay["kazanimlar"]
                    print(f"      {len(kazanimlar)} kazanım bulundu.")
                    
                    for kaz in kazanimlar:
                        save_icerik_kaydi(
                            ders_adi=ders["ders_adi"],
                            sinif=sinif["sinif"],
                            unite=tema["tema_adi"],
                            kazanim=kaz["kazanim"],
                            aciklama=kaz["aciklama"],
                            unite_id=unite_id
                        )
                
                # Rate limiting
                time.sleep(1)
            
            time.sleep(0.5)
        
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("TAMAMLANDI!")
    print("=" * 60)


def test_single_tema():
    """Tek bir tema için test"""
    print("Test: Biyoloji Dersi - 9.Sınıf - 1. TEMA: YAŞAM")
    
    tema_url = "https://tymm.meb.gov.tr/biyoloji-dersi/unite/2"
    detay = get_tema_detay(tema_url)
    
    if detay:
        print(f"\nHTML uzunluğu: {len(detay['html'])} karakter")
        print(f"Kazanım sayısı: {len(detay['kazanimlar'])}")
        
        for i, kaz in enumerate(detay['kazanimlar'], 1):
            print(f"\n--- Kazanım {i} ---")
            print(f"Kazanım: {kaz['kazanim']}")
            print(f"Açıklama: {kaz['aciklama'][:200]}..." if len(kaz['aciklama']) > 200 else f"Açıklama: {kaz['aciklama']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_single_tema()
    else:
        scrape_all()
