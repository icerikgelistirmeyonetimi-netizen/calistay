-- Login tablosunu oluştur
CREATE TABLE IF NOT EXISTS login (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index ekle
CREATE INDEX IF NOT EXISTS idx_login_username ON login(username);

-- RLS (Row Level Security) politikalarını ayarla
ALTER TABLE login ENABLE ROW LEVEL SECURITY;

-- Herkes okuyabilir
CREATE POLICY "Enable read access for all users" ON login
    FOR SELECT USING (true);

-- Herkes insert edebilir (gerekirse kaldırılabilir)
CREATE POLICY "Enable insert for all users" ON login
    FOR INSERT WITH CHECK (true);
