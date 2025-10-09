# Environment Setup for RAG Service

## Required Configuration

Create a `.env` file in `backend/rag-service/` with the following content:

```bash
# ===========================================
# VN-LAW-MINI RAG SERVICE CONFIGURATION
# ===========================================

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Vector Database Configuration
VECTOR_DB_PROVIDER=pinecone

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=law-advisor-mini
PINECONE_ENVIRONMENT=gcp-starter

# HuggingFace Configuration (for LLM)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Model Configuration
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
LLM_MODEL=meta-llama/Llama-2-7b-chat-hf

# Service Configuration
PORT=8001
HOST=0.0.0.0

# Debug Mode
DEBUG=True
```

## How to Get API Keys

### 1. Supabase
- Go to: https://supabase.com/dashboard
- Select your project
- Go to: Settings > API
- Copy `URL` and `anon public` key

### 2. Pinecone
- Go to: https://app.pinecone.io
- Sign up/Login
- Go to: API Keys
- Create new API key
- Create index with name: `law-advisor-mini`
  - Dimensions: 768 (for paraphrase-multilingual-mpnet-base-v2)
  - Metric: cosine

### 3. HuggingFace (Optional, for LLM)
- Go to: https://huggingface.co/settings/tokens
- Create new token
- Copy token

## Quick Setup Script

Run this in PowerShell:

```powershell
# Navigate to rag-service directory
cd backend\rag-service

# Create .env file (edit with your values)
@"
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=law-advisor-mini
PINECONE_ENVIRONMENT=gcp-starter
HUGGINGFACE_API_KEY=your_hf_key
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
PORT=8001
HOST=0.0.0.0
DEBUG=True
"@ | Out-File -FilePath .env -Encoding UTF8
```

## Verify Setup

After creating `.env`, test the connection:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SUPABASE_URL:', os.getenv('SUPABASE_URL')); print('PINECONE_API_KEY:', 'Set' if os.getenv('PINECONE_API_KEY') else 'Not Set')"
```

