# Law Service API

API service để tra cứu văn bản pháp luật Việt Nam - VN-Law-Mini

---

## Features

-   Get list of legal documents với pagination
-   Get chi tiết văn bản theo ID
-   Get chi tiết điều luật theo mã pháp chế
-   Search văn bản và điều luật by keyword
-   Filter by loại văn bản, trạng thái

---

## Tech Stack

-   **Node.js** 18+
-   **Express** 4.x
-   **Supabase** (PostgreSQL)
-   **Vercel** (deployment)

---

## Setup Local

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Cập nhật values:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
PORT=5000
```

### 3. Run development server

```bash
npm run dev
```

Server chạy tại: `http://localhost:5000`

---

## API Endpoints

### Base URL

-   **Local**: `http://localhost:5000`
-   **Production**: `https://your-law-service.vercel.app`

---

### 1. Health Check

**GET** `/`

Response:

```json
{
  "service": "VN-Law-Mini Law Service",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {...}
}
```

**GET** `/health`

Response:

```json
{
    "status": "ok",
    "timestamp": "2024-..."
}
```

---

### 2. Get Documents List

**GET** `/api/v1/documents`

Query parameters:

-   `page` (number): Page number (default: 1)
-   `limit` (number): Items per page (default: 20, max: 100)
-   `loai` (string): Filter by document type (optional)
-   `trang_thai` (string): Filter by status (optional)

Example:

```bash
GET /api/v1/documents?page=1&limit=20&loai=Bộ luật
```

Response:

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "ten": "Bộ luật Dân sự 2015",
            "so_hieu": "91/2015/QH13",
            "loai": "Bộ luật",
            "ngay_ban_hanh": "2015-11-24",
            "ngay_hieu_luc": "2017-01-01",
            "trang_thai": "Còn hiệu lực",
            "co_quan_ban_hanh": "Quốc hội"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 100,
        "totalPages": 5
    }
}
```

---

### 3. Get Document Detail

**GET** `/api/v1/documents/:id`

Example:

```bash
GET /api/v1/documents/1
```

Response:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "ten": "Bộ luật Dân sự 2015",
        "so_hieu": "91/2015/QH13",
        "loai": "Bộ luật",
        "ngay_ban_hanh": "2015-11-24",
        "ngay_hieu_luc": "2017-01-01",
        "trang_thai": "Còn hiệu lực",
        "co_quan_ban_hanh": "Quốc hội",
        "nguoi_ky": "Nguyễn Sinh Hùng",
        "noi_dung": "...",
        "articles_count": 689
    }
}
```

---

### 4. Get Articles of Document

**GET** `/api/v1/documents/:id/articles`

Example:

```bash
GET /api/v1/documents/1/articles
```

Response:

```json
{
    "success": true,
    "document": {
        "id": 1,
        "ten": "Bộ luật Dân sự 2015"
    },
    "data": [
        {
            "id": 1,
            "mapc": "91/2015/QH13-Điều-1",
            "ten": "Điều 1. Phạm vi điều chỉnh",
            "noi_dung": "...",
            "chuong": "Chương I",
            "muc": "",
            "thu_tu": 0
        }
    ]
}
```

---

### 5. Get Article by MAPC

**GET** `/api/v1/articles/:mapc`

Example:

```bash
GET /api/v1/articles/91/2015/QH13-Điều-1
```

Response:

```json
{
    "success": true,
    "data": {
        "id": 1,
        "mapc": "91/2015/QH13-Điều-1",
        "ten": "Điều 1. Phạm vi điều chỉnh",
        "noi_dung": "...",
        "chuong": "Chương I",
        "thu_tu": 0,
        "document": {
            "id": 1,
            "ten": "Bộ luật Dân sự 2015",
            "so_hieu": "91/2015/QH13",
            "loai": "Bộ luật"
        }
    }
}
```

---

### 6. Search

**POST** `/api/v1/search`

Body:

```json
{
    "keyword": "dân sự",
    "type": "both",
    "limit": 20
}
```

Parameters:

-   `keyword` (string, required): Từ khóa tìm kiếm
-   `type` (string): 'documents' | 'articles' | 'both' (default: 'both')
-   `limit` (number): Max results (default: 20, max: 50)

Response:

```json
{
  "success": true,
  "keyword": "dân sự",
  "total": 15,
  "results": {
    "documents": [...],
    "articles": [...]
  }
}
```

---

### 7. Get Search Suggestions

**GET** `/api/v1/search/suggestions`

Lấy danh sách loại văn bản, cơ quan để filter

Response:

```json
{
  "success": true,
  "data": {
    "loai": ["Bộ luật", "Luật", "Nghị định", "Thông tư"],
    "co_quan_ban_hanh": ["Quốc hội", "Chính phủ", ...],
    "trang_thai": ["Còn hiệu lực", "Hết hiệu lực"]
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
    "success": false,
    "error": "Error message",
    "message": "Detailed error message"
}
```

HTTP Status Codes:

-   `400`: Bad Request (missing parameters, validation error)
-   `404`: Not Found (document/article not found)
-   `500`: Internal Server Error

---

## Deploy to Vercel

### 1. Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Login

```bash
vercel login
```

### 3. Deploy

```bash
vercel --prod
```

### 4. Set Environment Variables

Trong Vercel dashboard:

-   Go to **Settings → Environment Variables**
-   Add:
    -   `SUPABASE_URL`
    -   `SUPABASE_ANON_KEY`

---

## Testing

### Using cURL

```bash
# Health check
curl http://localhost:5000/health

# Get documents
curl http://localhost:5000/api/v1/documents?limit=5

# Get document detail
curl http://localhost:5000/api/v1/documents/1

# Search
curl -X POST http://localhost:5000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"keyword":"dân sự","type":"both"}'
```

### Using Postman/Thunder Client

Import endpoints:

1. Create new request
2. Method: GET/POST
3. URL: `http://localhost:5000/api/v1/...`
4. For POST: Set body to JSON

---

## Development

### Project Structure

```
law-service/
├── src/
│   ├── db/
│   │   └── supabase.js      # Supabase client
│   ├── routes/
│   │   ├── documents.js     # Documents endpoints
│   │   ├── articles.js      # Articles endpoints
│   │   └── search.js        # Search endpoints
│   └── index.js             # Main Express app
├── package.json
├── vercel.json
└── README.md
```

### Adding New Endpoints

1. Create route file trong `src/routes/`
2. Import và use trong `src/index.js`
3. Test local
4. Deploy

---

## Troubleshooting

### "Failed to connect to Supabase"

-   Check `SUPABASE_URL` và `SUPABASE_ANON_KEY` trong `.env`
-   Verify Supabase project is running
-   Check network/firewall

### "Module not found"

```bash
npm install
```

### Port already in use

Change `PORT` in `.env` or:

```bash
PORT=3000 npm run dev
```

---

## License

GPL-3.0

---

## Related

-   [VN-Law-Mini Main Project](../../README.md)
-   [Crawler Documentation](../../crawler/README.md)
-   [RAG Service](../rag-service/README.md)
