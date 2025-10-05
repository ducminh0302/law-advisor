-- =====================================================
-- VN-LAW-MINI DATABASE SCHEMA
-- Supabase PostgreSQL Schema
-- =====================================================

-- Enable UUID extension (nếu chưa có)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLE: documents
-- Lưu thông tin văn bản pháp luật
-- =====================================================
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    mapc VARCHAR(100) UNIQUE,
    ten VARCHAR(500) NOT NULL,
    loai VARCHAR(100),
    so_hieu VARCHAR(200),
    ngay_ban_hanh DATE,
    ngay_hieu_luc DATE,
    trang_thai VARCHAR(50) DEFAULT 'Còn hiệu lực',
    co_quan_ban_hanh VARCHAR(300),
    nguoi_ky VARCHAR(200),
    noi_dung TEXT,
    ghi_chu TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TABLE: articles
-- Lưu các điều luật trong văn bản
-- =====================================================
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    mapc VARCHAR(100) UNIQUE NOT NULL,
    document_id INT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    ten VARCHAR(500),
    noi_dung TEXT NOT NULL,
    chuong VARCHAR(200),
    muc VARCHAR(200),
    thu_tu INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- INDEXES for performance
-- =====================================================

-- Index cho search by tên văn bản
CREATE INDEX idx_documents_ten ON documents USING gin(to_tsvector('simple', ten));

-- Index cho filter by loại văn bản
CREATE INDEX idx_documents_loai ON documents(loai);

-- Index cho filter by trạng thái
CREATE INDEX idx_documents_trang_thai ON documents(trang_thai);

-- Index cho search điều luật theo mã
CREATE INDEX idx_articles_mapc ON articles(mapc);

-- Index cho foreign key
CREATE INDEX idx_articles_document_id ON articles(document_id);

-- Index cho search nội dung điều luật
CREATE INDEX idx_articles_noidung ON articles USING gin(to_tsvector('simple', noi_dung));

-- Index cho sắp xếp theo thứ tự
CREATE INDEX idx_articles_thutu ON articles(document_id, thu_tu);

-- =====================================================
-- FUNCTIONS: Auto update updated_at timestamp
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger cho documents
CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger cho articles
CREATE TRIGGER update_articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA for testing (optional)
-- =====================================================
INSERT INTO documents (mapc, ten, loai, so_hieu, ngay_ban_hanh, ngay_hieu_luc, trang_thai, co_quan_ban_hanh)
VALUES
    ('91/2015/QH13', 'Bộ luật Dân sự 2015', 'Bộ luật', '91/2015/QH13', '2015-11-24', '2017-01-01', 'Còn hiệu lực', 'Quốc hội'),
    ('100/2015/QH13', 'Bộ luật Hình sự 2015', 'Bộ luật', '100/2015/QH13', '2015-11-27', '2018-01-01', 'Còn hiệu lực', 'Quốc hội'),
    ('45/2019/QH14', 'Luật Lao động 2019', 'Luật', '45/2019/QH14', '2019-11-20', '2021-01-01', 'Còn hiệu lực', 'Quốc hội');

INSERT INTO articles (mapc, document_id, ten, noi_dung, chuong, muc, thu_tu)
VALUES
    ('91/2015/QH13-1', 1, 'Điều 1. Phạm vi điều chỉnh',
     'Bộ luật này quy định về quan hệ nhân thân và quan hệ tài sản giữa cá nhân, pháp nhân, chủ thể khác trong lĩnh vực dân sự.',
     'Chương I: Những quy định chung', 'Mục 1: Phạm vi điều chỉnh và đối tượng áp dụng', 1),
    ('91/2015/QH13-2', 1, 'Điều 2. Đối tượng áp dụng',
     'Bộ luật này áp dụng đối với cá nhân, pháp nhân, chủ thể khác có liên quan trong quan hệ dân sự.',
     'Chương I: Những quy định chung', 'Mục 1: Phạm vi điều chỉnh và đối tượng áp dụng', 2),
    ('100/2015/QH13-1', 2, 'Điều 1. Phạm vi điều chỉnh',
     'Bộ luật Hình sự quy định về những hành vi phạm tội, hình phạt và trách nhiệm hình sự.',
     'Chương I: Nhiệm vụ, hiệu lực và áp dụng của Bộ luật Hình sự', NULL, 1);

-- =====================================================
-- ROW LEVEL SECURITY (optional - cho production)
-- =====================================================
-- Nếu cần bật RLS cho Supabase
-- ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- Policy cho phép đọc public
-- CREATE POLICY "Public read access for documents"
--     ON documents FOR SELECT
--     USING (true);

-- CREATE POLICY "Public read access for articles"
--     ON articles FOR SELECT
--     USING (true);

-- =====================================================
-- VIEWS for common queries (optional)
-- =====================================================

-- View: Thống kê số lượng điều theo văn bản
CREATE VIEW document_stats AS
SELECT
    d.id,
    d.ten,
    d.loai,
    d.trang_thai,
    COUNT(a.id) as so_luong_dieu,
    d.ngay_ban_hanh,
    d.ngay_hieu_luc
FROM documents d
LEFT JOIN articles a ON d.id = a.document_id
GROUP BY d.id, d.ten, d.loai, d.trang_thai, d.ngay_ban_hanh, d.ngay_hieu_luc;

-- =====================================================
-- COMMENTS for documentation
-- =====================================================
COMMENT ON TABLE documents IS 'Bảng lưu thông tin các văn bản quy phạm pháp luật';
COMMENT ON TABLE articles IS 'Bảng lưu các điều luật thuộc văn bản';
COMMENT ON COLUMN documents.mapc IS 'Mã pháp chế (unique identifier)';
COMMENT ON COLUMN articles.mapc IS 'Mã pháp chế của điều luật';
COMMENT ON COLUMN articles.thu_tu IS 'Thứ tự sắp xếp điều luật trong văn bản';
