# 🗄️ Setup Supabase Database

Hướng dẫn từng bước để setup Supabase PostgreSQL database cho VN-Law-Mini.

---

## 📋 Prerequisites

-   Email để đăng ký Supabase (free tier)
-   Trình duyệt web

---

## 🚀 Bước 1: Tạo Supabase Account

1. Truy cập: https://supabase.com
2. Click **"Start your project"** hoặc **"Sign up"**
3. Chọn phương thức đăng ký:
    - GitHub (khuyến nghị)
    - Google
    - Email

---

## 🏗️ Bước 2: Tạo Project Mới

1. Sau khi đăng nhập, click **"New project"**
2. Điền thông tin:

    - **Organization**: Chọn hoặc tạo mới (ví dụ: "VN-Law")
    - **Project Name**: `vn-law-mini`
    - **Database Password**: Tạo password mạnh (LƯU LẠI PASSWORD NÀY!)
    - **Region**: Chọn `Southeast Asia (Singapore)` (gần VN nhất)
    - **Pricing Plan**: Free ($0/month)

3. Click **"Create new project"**
4. Đợi ~2 phút để Supabase provision database

---

## 📊 Bước 3: Chạy SQL Schema

1. Trong dashboard project, vào tab **"SQL Editor"** (biểu tượng 📝 bên trái)
2. Click **"New query"**
3. Copy toàn bộ nội dung file `infrastructure/supabase-schema.sql`
4. Paste vào SQL Editor
5. Click **"Run"** (hoặc Ctrl+Enter)
6. Kiểm tra kết quả:
    - ✅ "Success. No rows returned"
    - ❌ Nếu có lỗi, check syntax hoặc permissions

---

## 🔍 Bước 4: Verify Tables

1. Vào tab **"Table Editor"** (biểu tượng 📋 bên trái)
2. Kiểm tra các bảng đã được tạo:
    - ✅ `documents` (3 sample rows)
    - ✅ `articles` (3 sample rows)
3. Click vào từng bảng để xem cấu trúc và data mẫu

---

## 🔑 Bước 5: Lấy API Keys

1. Vào tab **"Settings"** (biểu tượng ⚙️ bên trái)
2. Chọn **"API"** trong menu settings
3. Copy các thông tin sau:

### **Project URL**

```
https://xxxxxxxxxxxxx.supabase.co
```

→ Lưu vào `.env` với tên `SUPABASE_URL`

### **anon/public Key**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

→ Lưu vào `.env` với tên `SUPABASE_ANON_KEY`

### **service_role Key** (⚠️ BẢO MẬT - chỉ dùng server-side)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

→ Lưu vào `.env` với tên `SUPABASE_SERVICE_KEY` (chỉ dùng cho crawler/backend)

---

## ✅ Bước 6: Test Connection

### Option 1: Qua Supabase Dashboard

1. Vào **"Table Editor"**
2. Click vào bảng `documents`
3. Thử thêm 1 row mới:
    - ten: "Test Document"
    - loai: "Thông tư"
    - trang_thai: "Còn hiệu lực"
4. Nếu save thành công → Database hoạt động ✅

### Option 2: Qua JavaScript (Node.js)

```bash
npm install @supabase/supabase-js
```

```javascript
// test-supabase.js
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient('YOUR_SUPABASE_URL', 'YOUR_SUPABASE_ANON_KEY');

async function testConnection() {
    const { data, error } = await supabase.from('documents').select('*').limit(5);

    if (error) {
        console.error('❌ Error:', error);
    } else {
        console.log('✅ Connection successful!');
        console.log('Documents:', data);
    }
}

testConnection();
```

```bash
node test-supabase.js
```

### Option 3: Qua Python

```bash
pip install supabase
```

```python
# test_supabase.py
from supabase import create_client, Client

url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_ANON_KEY"
supabase: Client = create_client(url, key)

response = supabase.table("documents").select("*").limit(5).execute()
print("✅ Connection successful!")
print(f"Documents: {response.data}")
```

```bash
python test_supabase.py
```

---

## 📝 Environment Variables

Thêm vào file `.env`:

```bash
# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Database Password (để backup/restore)
SUPABASE_DB_PASSWORD=your_database_password
```

---

## 🎯 Database Schema Summary

### **documents** table:

-   `id` (PK): Auto-increment
-   `ten`: Tên văn bản (VD: "Bộ luật Dân sự 2015")
-   `loai`: Loại văn bản (VD: "Bộ luật", "Luật", "Nghị định")
-   `so_hieu`: Số hiệu (VD: "91/2015/QH13")
-   `ngay_ban_hanh`, `ngay_hieu_luc`: Dates
-   `trang_thai`: "Còn hiệu lực" / "Hết hiệu lực"
-   `noi_dung`: Full text của văn bản

### **articles** table:

-   `id` (PK): Auto-increment
-   `mapc`: Mã pháp chế (unique)
-   `document_id` (FK): Link to documents
-   `ten`: Tên điều (VD: "Điều 1. Phạm vi điều chỉnh")
-   `noi_dung`: Nội dung điều luật
-   `chuong`, `muc`: Cấu trúc văn bản
-   `thu_tu`: Thứ tự sắp xếp

---

## 🔧 Troubleshooting

### Lỗi: "new row violates row-level security policy"

**Giải pháp**: Tắt RLS trong development:

```sql
ALTER TABLE documents DISABLE ROW LEVEL SECURITY;
ALTER TABLE articles DISABLE ROW LEVEL SECURITY;
```

### Lỗi: "permission denied for table"

**Giải pháp**: Dùng `service_role` key thay vì `anon` key cho operations như INSERT/UPDATE/DELETE.

### Lỗi: "relation does not exist"

**Giải pháp**: Chạy lại SQL schema từ đầu.

---

## 📚 Tài Liệu Tham Khảo

-   [Supabase Documentation](https://supabase.com/docs)
-   [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript/introduction)
-   [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
-   [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)

---

## ✅ Checklist

-   [ ] Tạo Supabase account
-   [ ] Tạo project `vn-law-mini`
-   [ ] Chạy SQL schema thành công
-   [ ] Verify tables `documents` và `articles` có data mẫu
-   [ ] Copy SUPABASE_URL và SUPABASE_ANON_KEY
-   [ ] Test connection (JavaScript hoặc Python)
-   [ ] Lưu credentials vào `.env`

---

**🎉 Xong! Bây giờ bạn có thể chuyển sang setup Vector Database.**

➡️ Tiếp theo: [02-SETUP-VECTOR-DB.md](./02-SETUP-VECTOR-DB.md)
