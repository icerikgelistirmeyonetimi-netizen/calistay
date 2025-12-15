-- Login tablosunu temizle
TRUNCATE TABLE login RESTART IDENTITY;

-- Moderatörlerden kullanıcı oluştur ve ekle
INSERT INTO login (username, password, full_name)
WITH moderators AS (
  -- Virgülle ayrılmış moderatörleri ayır
  SELECT DISTINCT 
    TRIM(unnest(string_to_array(moderator, ','))) as full_name
  FROM icerik_kayitlari 
  WHERE moderator IS NOT NULL 
    AND moderator != ''
),
cleaned_moderators AS (
  -- Boş olmayan moderatörleri filtrele
  SELECT full_name
  FROM moderators
  WHERE full_name != '' AND full_name IS NOT NULL
),
with_usernames AS (
  -- Her moderatör için kullanıcı adı ve şifre oluştur
  SELECT 
    full_name,
    -- İlk harfi al
    lower(
      translate(
        substring(split_part(full_name, ' ', 1) from 1 for 1),
        'çğıöşüÇĞİÖŞÜ',
        'cgiosuCGIOSU'
      )
    ) || '_' ||
    -- Son kelimeyi al
    lower(
      translate(
        split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)),
        'çğıöşüÇĞİÖŞÜ',
        'cgiosuCGIOSU'
      )
    ) as username,
    -- Rastgele 8 karakterlik şifre oluştur
    substring(md5(random()::text || full_name || random()::text) from 1 for 8) as password
  FROM cleaned_moderators
)
SELECT username, password, full_name
FROM with_usernames
ORDER BY full_name;

-- Eklenen kullanıcıları göster
SELECT 
  full_name as "Tam Ad",
  username as "Kullanıcı Adı", 
  password as "Şifre"
FROM login 
ORDER BY full_name;
