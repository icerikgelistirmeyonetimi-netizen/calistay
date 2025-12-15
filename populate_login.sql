-- Önce mevcut verileri temizle
TRUNCATE TABLE login;

-- Moderatörlerden kullanıcı oluştur
WITH moderators AS (
  SELECT DISTINCT 
    TRIM(unnest(string_to_array(moderator, ','))) as full_name
  FROM icerik_kayitlari 
  WHERE moderator IS NOT NULL AND moderator != ''
),
usernames AS (
  SELECT 
    full_name,
    lower(substring(split_part(full_name, ' ', 1), 1, 1)) || '_' || 
    lower(regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', 
      CASE 
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ç%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%Ç%' THEN 'c'
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ğ%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%Ğ%' THEN 'g'
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ı%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%İ%' THEN 'i'
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ö%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%Ö%' THEN 'o'
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ş%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%Ş%' THEN 's'
        WHEN regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%ü%' OR 
             regexp_replace(split_part(full_name, ' ', array_length(string_to_array(full_name, ' '), 1)), '[çÇğĞıİöÖşŞüÜ]', '', 'g') LIKE '%Ü%' THEN 'u'
        ELSE ''
      END, 'g')) as username,
    substr(md5(random()::text || full_name), 1, 8) as password
  FROM moderators
  WHERE full_name != ''
)
INSERT INTO login (username, password, full_name)
SELECT username, password, full_name
FROM usernames
ORDER BY full_name;

-- Sonuçları göster
SELECT full_name, username, password 
FROM login 
ORDER BY full_name;
