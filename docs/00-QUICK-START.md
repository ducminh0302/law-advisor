# ⚡ Quick Start Guide

Hướng dẫn nhanh để setup Phase 1 trong 15-20 phút.

---

## ✅ Checklist Phase 1

Hoàn thành các bước sau theo thứ tự:

### 1️⃣ Supabase (5 phút)

-   [ ] Đăng ký tài khoản: https://supabase.com
-   [ ] Tạo project `vn-law-mini`
-   [ ] Chạy SQL từ `infrastructure/supabase-schema.sql`
-   [ ] Copy `SUPABASE_URL` và `SUPABASE_ANON_KEY`

📖 **Chi tiết**: [01-SETUP-SUPABASE.md](./01-SETUP-SUPABASE.md)

---

### 2️⃣ Pinecone (5 phút)

-   [ ] Đăng ký tài khoản: https://pinecone.io
-   [ ] Tạo index `vn-law-embeddings`:
    -   Dimensions: **768**
    -   Metric: **cosine**
    -   Capacity: **Serverless**
-   [ ] Copy `PINECONE_API_KEY` và `PINECONE_ENVIRONMENT`

📖 **Chi tiết**: [02-SETUP-VECTOR-DB.md](./02-SETUP-VECTOR-DB.md)

---

### 3️⃣ HuggingFace (3 phút)

-   [ ] Đăng ký tài khoản: https://huggingface.co
-   [ ] Tạo Access Token (role: `read`)
-   [ ] Copy `HF_API_TOKEN`

📖 **Chi tiết**: [03-SETUP-HUGGINGFACE.md](./03-SETUP-HUGGINGFACE.md)

---

### 4️⃣ Environment Setup (2 phút)

```bash
# 1. Copy template
cp .env.example .env

# 2. Mở file .env và điền values:
# - SUPABASE_URL
# - SUPABASE_ANON_KEY
# - PINECONE_API_KEY
# - PINECONE_ENVIRONMENT
# - HF_API_TOKEN
```

---

## 🧪 Test Connections

### Test Supabase (Node.js)

```bash
cd vn-law-mini
npm install @supabase/supabase-js
node -e "
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);
supabase.from('documents').select('*').limit(1).then(
  ({data, error}) => console.log(error ? '❌ Error' : '✅ Supabase OK', data)
);
"
```

### Test Pinecone (Python)

```bash
pip install pinecone-client
python -c "
from pinecone import Pinecone
import os
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
print('✅ Pinecone OK:', pc.list_indexes())
"
```

### Test HuggingFace (Python)

```bash
pip install requests
python -c "
import requests, os
url = 'https://api-inference.huggingface.co/models/VietAI/viet-gpt-2'
headers = {'Authorization': f'Bearer {os.getenv(\"HF_API_TOKEN\")}'}
r = requests.post(url, headers=headers, json={'inputs': 'Test'})
print('✅ HuggingFace OK' if r.status_code == 200 else '❌ Error')
"
```

---

## 🎉 Phase 1 Complete!

Nếu tất cả tests pass, bạn đã sẵn sàng cho Phase 2!

```
✅ Supabase: Connected
✅ Pinecone: Connected
✅ HuggingFace: Connected

🎯 Next: Phase 2 - Crawler & Data
```

---

## ❓ Troubleshooting

### "Cannot find module"

```bash
# Cài dependencies
npm install  # cho Node.js
pip install -r requirements.txt  # cho Python
```

### "Unauthorized" errors

-   Verify API keys trong `.env` file
-   Check không có spaces thừa
-   Regenerate tokens nếu cần

### "Network error"

-   Check internet connection
-   Verify firewall không block

---

## 📞 Need Help?

-   📖 Đọc detailed docs trong `docs/`
-   🐛 Report issues tại GitHub
-   💬 Join Discord community

---

**Time estimate**: 15-20 phút cho toàn bộ Phase 1
