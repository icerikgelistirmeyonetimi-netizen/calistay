-- Bu sorguyu Supabase SQL Editor'de çalıştırın
-- Sonuçları CSV olarak export edip txt'ye çevirebilirsiniz

SELECT 
  full_name as "Tam Ad",
  username as "Kullanıcı Adı", 
  password as "Şifre",
  created_at as "Oluşturulma Tarihi"
FROM login 
ORDER BY full_name;
