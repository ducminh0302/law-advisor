# 🔍 Setup Vector Database

Hướng dẫn setup Vector Database cho RAG system. Bạn có 2 lựa chọn: **Pinecone** (khuyến nghị) hoặc **ChromaDB Cloud**.

---

## 📊 So Sánh 2 Options

| Feature         | Pinecone                 | ChromaDB Cloud    |
| --------------- | ------------------------ | ----------------- |
| Free Tier       | ✅ 1 index, 100K vectors | ✅ Beta (limited) |
| Dễ setup        | ⭐⭐⭐⭐⭐               | ⭐⭐⭐            |
| Performance     | Rất nhanh                | Nhanh             |
| Scalability     | Tốt                      | Vừa phải          |
| Docs            | Xuất sắc                 | Đang phát triển   |
| **Khuyến nghị** | ✅ Cho production        | Cho dev/test      |

**Khuyến nghị**: Dùng **Pinecone** cho đơn giản và ổn định.

---

## 🎯 OPTION 1: Pinecone (Khuyến nghị)

### Bước 1: Tạo Pinecone Account

1. Truy cập: https://www.pinecone.io
2. Click **"Sign Up"** hoặc **"Start Free"**
3. Đăng ký với:
    - Email + Password, hoặc
    - Google Account
4. Verify email

---

### Bước 2: Tạo Index

1. Login vào Pinecone Console: https://app.pinecone.io
2. Click **"Create Index"**
3. Điền thông tin:

```
Index Name: vn-law-embeddings
Dimensions: 768  (Vietnamese SBERT output size)
Metric: cosine
Capacity Mode: Serverless (free tier)
Cloud: AWS
Region: us-east-1 (hoặc gần nhất)
```

4. Click **"Create Index"**
5. Đợi ~1 phút để index ready

---

### Bước 3: Lấy API Keys

1. Vào tab **"API Keys"** (bên trái)
2. Click **"Create API Key"** (nếu chưa có)
3. Copy thông tin:

**API Key**:

```
pcsk_xxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Environment**:

```
us-east-1-aws (hoặc region bạn chọn)
```

---

### Bước 4: Test Connection (Python)

```bash
pip install pinecone-client
```

```python
# test_pinecone.py
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_PINECONE_API_KEY")

# List indexes
indexes = pc.list_indexes()
print("✅ Pinecone connection successful!")
print(f"Available indexes: {indexes}")

# Connect to index
index = pc.Index("vn-law-embeddings")
stats = index.describe_index_stats()
print(f"Index stats: {stats}")
```

```bash
python test_pinecone.py
```

---

### Bước 5: Environment Variables

Thêm vào `.env`:

```bash
# Pinecone Configuration
PINECONE_API_KEY=pcsk_xxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=vn-law-embeddings
```

---

### 📚 Pinecone Integration Code

```python
# backend/rag-service/vector_store.py
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os

# Initialize
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")

# Upsert vectors
def upsert_articles(articles):
    """
    articles: List of dicts with keys: id, mapc, noidung, metadata
    """
    vectors = []
    for article in articles:
        embedding = embedding_model.encode(article['noidung']).tolist()
        vectors.append({
            "id": article['mapc'],
            "values": embedding,
            "metadata": {
                "mapc": article['mapc'],
                "ten": article['ten'],
                "document_id": article['document_id'],
                "noidung": article['noidung'][:1000]  # Pinecone metadata limit
            }
        })
    index.upsert(vectors=vectors)
    print(f"✅ Upserted {len(vectors)} vectors")

# Query vectors
def search_similar(question, top_k=3):
    embedding = embedding_model.encode(question).tolist()
    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results['matches']
```

---

## 🧪 OPTION 2: ChromaDB Cloud

> ⚠️ ChromaDB Cloud đang trong beta, có thể không ổn định.

### Bước 1: Request Access

1. Truy cập: https://www.trychroma.com/cloud
2. Click **"Request Access"** hoặc **"Join Waitlist"**
3. Điền email và đợi invite (có thể mất vài ngày)

---

### Bước 2: Setup sau khi có access

1. Login vào ChromaDB Cloud dashboard
2. Tạo workspace mới: `vn-law-mini`
3. Tạo collection: `law_embeddings`
4. Copy API endpoint và token

---

### Bước 3: Test Connection (Python)

```bash
pip install chromadb
```

```python
# test_chroma.py
import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
    host="YOUR_CHROMA_HOST",
    port=8000,
    settings=Settings(
        chroma_api_impl="rest",
        chroma_auth_token="YOUR_CHROMA_TOKEN"
    )
)

# Test
collections = client.list_collections()
print("✅ ChromaDB connection successful!")
print(f"Collections: {collections}")
```

---

### Bước 4: Environment Variables

```bash
# ChromaDB Configuration
CHROMA_HOST=your-workspace.chromadb.cloud
CHROMA_PORT=8000
CHROMA_TOKEN=your_auth_token
CHROMA_COLLECTION=law_embeddings
```

---

### 📚 ChromaDB Integration Code

```python
# backend/rag-service/vector_store.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

# Initialize
client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST"),
    port=int(os.getenv("CHROMA_PORT", 8000)),
    settings=Settings(
        chroma_api_impl="rest",
        chroma_auth_token=os.getenv("CHROMA_TOKEN")
    )
)

collection = client.get_or_create_collection(
    name=os.getenv("CHROMA_COLLECTION"),
    metadata={"description": "Vietnamese Law Articles Embeddings"}
)

embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")

# Add documents
def add_articles(articles):
    ids = [a['mapc'] for a in articles]
    documents = [a['noidung'] for a in articles]
    metadatas = [{
        "mapc": a['mapc'],
        "ten": a['ten'],
        "document_id": a['document_id']
    } for a in articles]

    embeddings = embedding_model.encode(documents).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"✅ Added {len(ids)} documents")

# Query
def search_similar(question, top_k=3):
    embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results
```

---

## 🔄 Alternative: Local ChromaDB (Dev only)

Nếu chưa có cloud access, dùng local cho development:

```python
import chromadb

# Local persistent storage
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("law_embeddings")
```

**Lưu ý**: Local ChromaDB không thể deploy lên Vercel. Chỉ dùng cho dev local.

---

## 📊 Embedding Model: Vietnamese SBERT

Cả 2 options đều dùng model này để tạo embeddings:

```bash
pip install sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

# Download model (lần đầu ~400MB)
model = SentenceTransformer("keepitreal/vietnamese-sbert")

# Test
text = "Điều 1. Phạm vi điều chỉnh của Bộ luật Dân sự"
embedding = model.encode(text)
print(f"Embedding shape: {embedding.shape}")  # (768,)
```

---

## ✅ Checklist

**Pinecone**:

-   [ ] Tạo Pinecone account
-   [ ] Tạo index `vn-law-embeddings` (768 dimensions, cosine)
-   [ ] Copy API key và environment
-   [ ] Test connection với Python
-   [ ] Lưu credentials vào `.env`

**ChromaDB Cloud** (alternative):

-   [ ] Request access và đợi invite
-   [ ] Tạo workspace và collection
-   [ ] Copy host, port, token
-   [ ] Test connection
-   [ ] Lưu credentials vào `.env`

**Embedding Model**:

-   [ ] Install `sentence-transformers`
-   [ ] Download `keepitreal/vietnamese-sbert`
-   [ ] Test encoding với sample text

---

## 🔧 Troubleshooting

### Pinecone: "Index not found"

-   Đợi 1-2 phút sau khi tạo index
-   Verify index name trong code khớp với dashboard

### ChromaDB: "Connection refused"

-   Check host và port
-   Verify auth token
-   ChromaDB Cloud có thể unstable (beta)

### Embedding Model: Download chậm

-   Model ~400MB, cần internet tốt
-   Hoặc download manual: https://huggingface.co/keepitreal/vietnamese-sbert

---

## 📚 Tài Liệu Tham Khảo

-   [Pinecone Documentation](https://docs.pinecone.io/)
-   [ChromaDB Documentation](https://docs.trychroma.com/)
-   [Vietnamese SBERT Model](https://huggingface.co/keepitreal/vietnamese-sbert)
-   [Sentence Transformers](https://www.sbert.net/)

---

**🎉 Xong! Bây giờ bạn có vector database để lưu embeddings.**

➡️ Tiếp theo: [03-SETUP-HUGGINGFACE.md](./03-SETUP-HUGGINGFACE.md)
