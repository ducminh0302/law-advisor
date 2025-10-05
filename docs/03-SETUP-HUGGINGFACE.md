# 🤗 Setup HuggingFace Inference API

Hướng dẫn setup HuggingFace để sử dụng Large Language Model cho Q&A system.

---

## 🎯 Tại Sao Dùng HuggingFace?

-   ✅ **Free tier**: ~30,000 tokens/tháng miễn phí
-   ✅ **Serverless**: Không cần host model
-   ✅ **Nhiều models**: Vietnamese LLM (VietGPT, PhoGPT, etc.)
-   ✅ **Dễ migrate**: Sau này chuyển sang AWS chỉ cần đổi endpoint

---

## 📋 Bước 1: Tạo HuggingFace Account

1. Truy cập: https://huggingface.co
2. Click **"Sign Up"** (góc phải trên)
3. Đăng ký với:

    - Email + Password
    - GitHub (khuyến nghị)
    - Google

4. Verify email

---

## 🔑 Bước 2: Tạo Access Token

1. Login vào HuggingFace
2. Click vào **Avatar** (góc phải trên) → **Settings**
3. Trong menu bên trái, chọn **"Access Tokens"**
4. Click **"New token"**

Điền thông tin:

```
Name: vn-law-mini
Role: read (đủ cho inference)
```

5. Click **"Generate token"**
6. **COPY TOKEN NGAY** (chỉ hiện 1 lần!)

```
hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **LƯU Ý**: Token này có quyền truy cập tài khoản của bạn, giữ bí mật!

---

## 🧪 Bước 3: Test Inference API

### Option A: Test qua Web UI

1. Vào model page: https://huggingface.co/vinai/phobert-base-v2
2. Trong tab **"Hosted inference API"** bên phải
3. Nhập text tiếng Việt để test
4. Nếu thấy kết quả → API hoạt động ✅

### Option B: Test qua Python

```bash
pip install requests
```

```python
# test_hf_api.py
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/VietAI/viet-gpt-2"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Test
output = query({
    "inputs": "Xin chào, tôi là"
})

print("✅ HuggingFace API connection successful!")
print(f"Output: {output}")
```

```bash
export HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python test_hf_api.py
```

---

## 🤖 Bước 4: Chọn Model Phù Hợp

### Các models tiếng Việt khuyến nghị:

| Model                       | Size | Use Case                | Free Tier?      |
| --------------------------- | ---- | ----------------------- | --------------- |
| **arcee-ai/Arcee-VyLinh**   | N/A  | Vietnamese legal domain | ✅ Tốt nhất     |
| **VietAI/viet-gpt-2**       | 110M | Fast generation         | ✅ Rất tốt      |
| **vinai/phobert-base-v2**   | 135M | Understanding           | ✅ Rất tốt      |
| **Viet-Mistral/Vistral-7B** | 7B   | Best quality            | ⚠️ Slow/Limited |

**Khuyến nghị cho demo**: `arcee-ai/Arcee-VyLinh` (được huấn luyện đặc biệt cho pháp luật Việt Nam)

---

## 📝 Bước 5: Setup cho RAG System

### Code mẫu cho Q&A:

```python
# backend/rag-service/model_client.py
import requests
import os

class ModelClient:
    def __init__(self, provider='huggingface'):
        self.provider = provider
        if provider == 'huggingface':
            self.api_url = os.getenv(
                "HF_INFERENCE_API",
                "https://api-inference.huggingface.co/models/arcee-ai/Arcee-VyLinh"
            )
            self.headers = {
                "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
            }

    def generate(self, prompt, max_length=512, temperature=0.7):
        """
        Generate answer from prompt
        """
        if self.provider == 'huggingface':
            return self._call_hf(prompt, max_length, temperature)
        elif self.provider == 'aws':
            # Implement later when migrate to AWS
            return self._call_aws(prompt, max_length, temperature)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _call_hf(self, prompt, max_length, temperature):
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "do_sample": True,
                "top_p": 0.9,
                "return_full_text": False
            }
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            return ""
        else:
            raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")

    def _call_aws(self, prompt, max_length, temperature):
        # TODO: Implement AWS endpoint when migrating
        raise NotImplementedError("AWS integration coming soon")
```

### Usage trong RAG:

```python
from model_client import ModelClient

# Initialize
llm = ModelClient(provider='huggingface')

# RAG prompt
context = "Điều 1. Bộ luật này quy định về quan hệ dân sự..."
question = "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"

prompt = f"""Dựa vào văn bản sau đây:
{context}

Hãy trả lời câu hỏi: {question}

Trả lời:"""

# Generate answer
answer = llm.generate(prompt, max_length=300)
print(f"Answer: {answer}")
```

---

## 💰 Bước 6: Hiểu Rate Limits & Pricing

### Free Tier:

-   **Requests**: Không giới hạn số lượng
-   **Compute**: ~30,000 tokens/tháng
-   **Rate limit**: ~10 requests/phút cho cold models
-   **Model loading**: 20s đầu tiên (cold start)

### Khi Vượt Quota:

-   Lỗi 429: "Rate limit exceeded"
-   Giải pháp:
    1. Dùng cache (Redis) để giảm calls
    2. Upgrade lên Pro ($9/tháng): 1M tokens
    3. Migrate sang AWS SageMaker

### Tips Tiết Kiệm:

-   ✅ Cache câu trả lời với Redis
-   ✅ Giới hạn `max_length` output
-   ✅ Dùng model nhỏ hơn nếu đủ quality
-   ✅ Implement retry logic với exponential backoff

---

## 🔐 Bước 7: Environment Variables

Thêm vào `.env`:

```bash
# HuggingFace Configuration
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HF_INFERENCE_API=https://api-inference.huggingface.co/models/arcee-ai/Arcee-VyLinh

# Fallback model (optional)
HF_FALLBACK_MODEL=VietAI/viet-gpt-2
```

---

## 🔧 Bước 8: Handle Errors & Retries

```python
import time
from functools import wraps

def retry_on_error(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"⚠️ Attempt {attempt+1} failed: {e}")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

class ModelClient:
    # ... previous code ...

    @retry_on_error(max_retries=3, delay=2)
    def generate(self, prompt, max_length=512, temperature=0.7):
        # ... existing generate code ...
```

---

## 📊 Bước 9: Monitor Usage

### Check quota qua API:

```python
import requests

def check_quota(api_token):
    url = "https://huggingface.co/api/usage"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Usage
quota = check_quota(os.getenv('HF_API_TOKEN'))
print(f"Monthly quota used: {quota}")
```

### Dashboard:

-   Vào: https://huggingface.co/settings/billing
-   Xem usage và quota remaining

---

## ✅ Checklist

-   [ ] Tạo HuggingFace account
-   [ ] Generate Access Token với role `read`
-   [ ] Test Inference API với Python
-   [ ] Chọn model phù hợp (khuyến nghị: `arcee-ai/Arcee-VyLinh`)
-   [ ] Implement `ModelClient` với abstraction
-   [ ] Test RAG prompt với sample context
-   [ ] Setup error handling và retry logic
-   [ ] Lưu `HF_API_TOKEN` vào `.env`
-   [ ] Verify rate limits và quota

---

## 🔧 Troubleshooting

### Lỗi: "Model is currently loading"

-   **Nguyên nhân**: Cold start (model chưa được load vào memory)
-   **Giải pháp**: Đợi 20-30s và retry

### Lỗi: "Rate limit exceeded" (429)

-   **Nguyên nhân**: Vượt quota hoặc quá nhiều requests
-   **Giải pháp**:
    1. Implement exponential backoff
    2. Dùng cache
    3. Upgrade plan

### Lỗi: "Unauthorized" (401)

-   **Nguyên nhân**: Token sai hoặc expired
-   **Giải pháp**: Regenerate token và update `.env`

### Output quality kém:

-   **Giải pháp**:
    1. Thử model lớn hơn
    2. Improve prompt engineering
    3. Tăng `max_length`
    4. Điều chỉnh `temperature` (0.5-0.9)

---

## 🚀 Migration Path to AWS (Tương Lai)

Khi cần migrate sang AWS:

1. **Deploy model lên AWS SageMaker**
2. **Update `model_client.py`**:

    ```python
    elif self.provider == 'aws':
        return self._call_aws(prompt, max_length, temperature)
    ```

3. **Implement `_call_aws()`**:

    ```python
    def _call_aws(self, prompt, max_length, temperature):
        import boto3
        client = boto3.client('sagemaker-runtime')
        response = client.invoke_endpoint(
            EndpointName=os.getenv('AWS_ENDPOINT_NAME'),
            Body=json.dumps({"inputs": prompt}),
            ContentType='application/json'
        )
        # Parse and return
    ```

4. **Change env var**: `MODEL_PROVIDER=aws`

✅ **Zero code change** trong RAG pipeline, chỉ đổi provider!

---

## 📚 Tài Liệu Tham Khảo

-   [HuggingFace Inference API Docs](https://huggingface.co/docs/api-inference/index)
-   [Vietnamese Models Hub](https://huggingface.co/models?language=vi&sort=downloads)
-   [Rate Limits & Pricing](https://huggingface.co/pricing)
-   [Best Practices](https://huggingface.co/docs/api-inference/best-practices)

---

**🎉 Xong Phase 1 - Infrastructure Setup!**

Bây giờ bạn đã có:

-   ✅ Supabase Database
-   ✅ Vector Database (Pinecone/ChromaDB)
-   ✅ HuggingFace LLM API

➡️ Tiếp theo: **Phase 2 - Crawler & Data**
