# RAG Service API

API service cho Q&A về pháp luật Việt Nam sử dụng RAG (Retrieval-Augmented Generation) - VN-Law-Mini

---

## Features

-   **Vector Search**: Tìm kiếm điều luật liên quan bằng embeddings
-   **LLM Generation**: Tạo câu trả lời chính xác từ context
-   **Citations**: Trích dẫn nguồn với relevance score
-   **Multi-Provider**: Hỗ trợ HuggingFace và AWS (dễ dàng migration)
-   **Vietnamese Optimized**: Sử dụng Vietnamese SBERT embeddings

---

## Tech Stack

-   **Python** 3.9+
-   **Flask** 2.x
-   **LangChain** - RAG framework
-   **Sentence Transformers** - Vietnamese embeddings
-   **Pinecone** / **ChromaDB** - Vector database
-   **HuggingFace API** - LLM inference
-   **Vercel** - Deployment

---

## Setup Local

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Cập nhật values:

```env
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...

# Vector DB (choose one)
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=xxxxx
PINECONE_INDEX_NAME=vn-law-embeddings

# LLM Provider
MODEL_PROVIDER=huggingface
HF_API_TOKEN=hf_xxxxx
HF_INFERENCE_API=https://api-inference.huggingface.co/models/XXX

# RAG Settings
RAG_TOP_K=3
RAG_MAX_LENGTH=512
RAG_TEMPERATURE=0.7

PORT=5001
```

### 3. Create embeddings

Trước khi chạy service, cần tạo embeddings cho dữ liệu:

```bash
python vectorize.py
```

Script này sẽ:

1. Load articles từ Supabase
2. Tạo embeddings với Vietnamese SBERT
3. Upload to Pinecone/ChromaDB

### 4. Run development server

```bash
python app.py
```

Server chạy tại: `http://localhost:5001`

---

## API Endpoints

### Base URL

-   **Local**: `http://localhost:5001`
-   **Production**: `https://your-rag-service.vercel.app`

---

### 1. Health Check

**GET** `/`

Response:

```json
{
    "service": "VN-Law-Mini RAG Service",
    "version": "1.0.0",
    "status": "running",
    "endpoints": {
        "question": "POST /api/v1/question"
    }
}
```

**GET** `/health`

Response:

```json
{
    "status": "ok",
    "vector_store": "ready",
    "llm_client": "ready"
}
```

---

### 2. Ask Question

**POST** `/api/v1/question`

Body:

```json
{
    "question": "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
}
```

Parameters:

-   `question` (string, required): Câu hỏi về pháp luật

Response (Success):

```json
{
    "success": true,
    "question": "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?",
    "answer": "Bộ luật Dân sự điều chỉnh quan hệ nhân thân và quan hệ tài sản giữa các chủ thể bình đẳng...",
    "citations": [
        {
            "mapc": "91/2015/QH13-Điều-1",
            "ten": "Điều 1. Phạm vi điều chỉnh",
            "noi_dung": "Bộ luật này quy định về quan hệ nhân thân...",
            "score": 0.892
        },
        {
            "mapc": "91/2015/QH13-Điều-2",
            "ten": "Điều 2. Áp dụng Bộ luật Dân sự",
            "noi_dung": "...",
            "score": 0.785
        }
    ]
}
```

Response (Error):

```json
{
    "success": false,
    "error": "No relevant articles found"
}
```

---

## How RAG Works

### Pipeline Overview

```
User Question
     ↓
[1] Vectorize Question (Embeddings)
     ↓
[2] Vector Search (Pinecone/ChromaDB)
     ↓
[3] Retrieve Top-K Articles (default: 3)
     ↓
[4] Build Context from Articles
     ↓
[5] Generate Answer with LLM (HuggingFace)
     ↓
[6] Return Answer + Citations
```

### Configuration

Environment variables để tune RAG:

| Variable          | Default | Description                            |
| ----------------- | ------- | -------------------------------------- |
| `RAG_TOP_K`       | 3       | Số lượng articles liên quan nhất       |
| `RAG_MAX_LENGTH`  | 512     | Max tokens cho LLM response            |
| `RAG_TEMPERATURE` | 0.7     | Creativity (0-1, thấp = chính xác hơn) |

---

## Vector Database Options

### Option 1: Pinecone (Recommended)

**Pros**: Managed, fast, free tier 100K vectors

Setup:

```env
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=xxxxx
PINECONE_INDEX_NAME=vn-law-embeddings
```

Create index: 768 dimensions (Vietnamese SBERT)

### Option 2: ChromaDB (Local)

**Pros**: Fully local, no cost, no API limits

Setup:

```env
VECTOR_DB_PROVIDER=chroma
CHROMA_PERSIST_DIR=./chroma_db
```

Tự động tạo khi chạy `vectorize.py`

---

## LLM Provider Options

### Option 1: HuggingFace API (Default)

**Pros**: Free tier ~30K tokens/month, easy setup

Setup:

```env
MODEL_PROVIDER=huggingface
HF_API_TOKEN=hf_xxxxx
HF_INFERENCE_API=https://api-inference.huggingface.co/models/arcee-ai/Arcee-VyLinh
```

**Models for Vietnamese**:

-   `arcee-ai/Arcee-VyLinh` (Recommended - specifically trained for Vietnamese legal domain)
-   `VietAI/vit5-large-vietnews-summarization`
-   `vinai/phobert-base`
-   `VietAI/gpt-neo-1.3B-vietnamese`

### Option 2: AWS SageMaker (For Scale)

**Pros**: No rate limits, full control, better performance

Setup:

```env
MODEL_PROVIDER=aws
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
SAGEMAKER_ENDPOINT_NAME=vn-law-llm
```

Deploy model to SageMaker → Update env → Zero code change! 🎉

---

## Error Responses

All errors follow this format:

```json
{
    "success": false,
    "error": "Error message",
    "message": "Detailed error"
}
```

HTTP Status Codes:

-   `400`: Bad Request (missing/invalid question)
-   `404`: Not Found (no relevant articles)
-   `500`: Internal Server Error (LLM/vector store failure)
-   `503`: Service Unavailable (not initialized)

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
-   Add tất cả variables từ `.env`

### 5. Deploy embeddings TRƯỚC

⚠️ **Important**: Chạy `vectorize.py` local để upload embeddings to Pinecone TRƯỚC KHI deploy service!

---

## Testing

### Using cURL

```bash
# Health check
curl http://localhost:5001/health

# Ask question
curl -X POST http://localhost:5001/api/v1/question \
  -H "Content-Type: application/json" \
  -d '{"question":"Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"}'
```

### Using Python

```python
import requests

response = requests.post(
    'http://localhost:5001/api/v1/question',
    json={'question': 'Điều kiện kết hôn là gì?'}
)

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Citations: {len(data['citations'])}")
```

---

## Development

### Project Structure

```
rag-service/
├── src/
│   └── models/
│       ├── model_client.py      # LLM abstraction (HF/AWS)
│       └── vector_store.py      # Vector DB abstraction
├── app.py                       # Flask API
├── vectorize.py                 # Script tạo embeddings
├── requirements.txt
├── vercel.json
└── README.md
```

### Adding New LLM Providers

1. Edit `src/models/model_client.py`
2. Add new provider class
3. Update `ModelClient.__init__()` switch case
4. Add env variables to `.env.example`

Example:

```python
class AzureOpenAIClient:
    def generate(self, prompt, **kwargs):
        # Implementation
        pass
```

---

## Performance Tuning

### Vector Search

-   Increase `RAG_TOP_K` for broader context (slower)
-   Use filters in vector search (by document type)

### LLM Generation

-   Lower `RAG_TEMPERATURE` for factual answers
-   Increase `RAG_MAX_LENGTH` for detailed responses
-   Use prompt engineering in `app.py:150`

### Embeddings

Model choice affects quality:

-   `keepitreal/vietnamese-sbert` - Best for legal text
-   `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` - Multilingual

---

## Troubleshooting

### "Service not properly initialized"

Check logs:

```bash
python app.py
```

Verify environment variables are set.

### "No relevant articles found"

-   Check embeddings exist: `vectorize.py` đã chạy?
-   Lower similarity threshold in `vector_store.py`
-   Check question language (phải tiếng Việt)

### HuggingFace API rate limit

-   Wait for quota reset (monthly)
-   Switch to AWS provider
-   Use smaller model

### Slow response time

-   Use Pinecone instead of ChromaDB
-   Deploy LLM on AWS SageMaker
-   Cache frequent questions (Redis)

---

## Migration Path to AWS

Khi HuggingFace free tier không đủ:

### 1. Deploy model lên SageMaker

```bash
# Sử dụng AWS CLI hoặc Console
aws sagemaker create-endpoint --endpoint-name vn-law-llm ...
```

### 2. Update environment

```env
MODEL_PROVIDER=aws
SAGEMAKER_ENDPOINT_NAME=vn-law-llm
AWS_REGION=us-east-1
```

### 3. Zero code change! 🎉

Abstraction layer trong `model_client.py` handle switching tự động.

---

## Cost Estimation

### Free Tier (Demo)

-   **Pinecone**: 100K vectors (free)
-   **HuggingFace**: ~30K tokens/month (free)
-   **Vercel**: Deployment (free)

**Total**: $0/month

### Production (AWS)

-   **SageMaker**: ml.t2.medium ($0.05/hour × 720h = $36/month)
-   **Pinecone**: Standard ($70/month for 10M vectors)

**Total**: ~$106/month

---

## Related

-   [VN-Law-Mini Main Project](../../README.md)
-   [Law Service API](../law-service/README.md)
-   [Crawler Documentation](../../crawler/README.md)
-   [Setup Vector DB Guide](../../docs/02-SETUP-VECTOR-DB.md)
-   [Setup HuggingFace Guide](../../docs/03-SETUP-HUGGINGFACE.md)

---

## License

GPL-3.0
