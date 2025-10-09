# VN Law Advisor Mini - Cloud Deployment Parameters

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Service Resource Requirements](#service-resource-requirements)
3. [Database Requirements](#database-requirements)
4. [Vector Database Requirements](#vector-database-requirements)
5. [LLM Service Requirements](#llm-service-requirements-arcee-vylinh)
6. [Traffic & Usage Patterns](#traffic--usage-patterns)
7. [Cost Breakdown](#cost-breakdown)
8. [Security & Compliance](#security--compliance)
9. [Deployment Architecture](#deployment-architecture)
10. [Deployment Strategy](#deployment-strategy)

## Architecture Overview

VN Law Advisor Mini is a microservices application with the following components:

1. **Frontend (Next.js 14)**: Homepage with search and chat features, built with TypeScript and TailwindCSS
2. **Law Service (Node.js/Express)**: CRUD operations for legal documents, connects to Self-host Supabase PostgreSQL
3. **RAG Service (Python/Flask)**: Vector search functionality and LLM inference for Q&A, connects to ChromaDB
4. **LLM Service (GreenNode)**: Self-hosted Arcee-VyLinh model for Vietnamese language processing
5. **External Services**: Self-host Supabase (PostgreSQL), ChromaDB (Vector Database)

## Service Resource Requirements

### 1. Frontend Service (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Deployment**: Vercel
- **Resource Requirements**:
  - Static assets: ~20-50 MB
  - Bandwidth: Depends on user interactions
  - CPU/Memory: Low during static serving, medium during SSR
  - Concurrent users: Dependent on traffic patterns

### 2. Law Service (Node.js/Express)
- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Dependencies**: @supabase/supabase-js, cors, dotenv, express (self-hosted Supabase)
- **Resource Requirements**:
  - Memory: 256-512 MB
  - CPU: Low to Medium (depends on database queries)
  - I/O: High (database connections)
  - Concurrent connections: Should handle 100+ concurrent requests
  - Database connections: 10-20 max

### 3. RAG Service (Python/Flask)
- **Runtime**: Python 3.8+
- **Framework**: Flask
- **Dependencies**: flask, flask-cors, supabase, chromadb, sentence-transformers, transformers, requests
- **Resource Requirements**:
  - Memory: 512MB-1GB (for embeddings model)
  - CPU: Medium (vector computations, embedding generation)
  - I/O: Medium (vector database and LLM service connections)
  - Cold start: Low (no model loading)

### 4. LLM Service (GreenNode)
- **Runtime**: Python 3.8+
- **Framework**: FastAPI/Flask
- **Model**: Arcee-VyLinh (3B parameters, Vietnamese-optimized)
- **Dependencies**: transformers, torch, fastapi, uvicorn
- **Resource Requirements**:
  - Memory: 8-16 GB (for 3B parameter model)
  - CPU: High (inference computation)
  - GPU: Recommended (NVIDIA GPU with 8GB+ VRAM)
  - Storage: 7-10 GB (model files)
  - Cold start: High (model loading ~30-60 seconds)

## Database Requirements (Self-host Supabase PostgreSQL)

### Current Data Size
- 87 documents
- 857 articles
- Document size: ~3KB per document (including metadata and content)
- Article size: ~2KB per article (including metadata and content)

### Estimated Storage Requirements
- Current: ~2.3MB
- With 10x growth: ~23MB
- With 100x growth: ~230MB
- With 1000x growth: ~2.3GB

### Performance Requirements
- Full-text search indexes on documents.title and articles.content
- Regular indexes on foreign keys and filters
- Connection requirements: ~30 concurrent connections recommended
- **Recommended Self-host Supabase Setup**: Docker container with 5GB storage, 120 concurrent connections

## Vector Database Requirements (ChromaDB)

### Current Data Size
- 857 vector embeddings
- Each embedding: 768 dimensions using float32 (3KB each)
- Total vector storage: ~2.57MB

### Projected Growth
- With 10x growth: 8,570 vectors = ~25.7MB
- With 100x growth: 85,700 vectors = ~257MB
- With 1000x growth: 857,000 vectors = ~2.57GB

### Index Configuration
- Metric: Cosine similarity
- Dimension: 768
- Metadata includes: mapc, ten, document_id, noidung (first 1000 chars)

### Performance Requirements
- High-dimensional vector search (768D)
- Approximate nearest neighbor search for speed
- Support for top-k retrieval (default k=3)

### Recommended ChromaDB Setup
- Docker container with persistent volume for initial deployment
- Horizontal scaling with multiple ChromaDB instances for better performance as data grows

## LLM Service Requirements (Arcee-VyLinh)

### Model Specifications
- **Model**: Arcee-VyLinh ([arcee-ai/Arcee-VyLinh](https://huggingface.co/arcee-ai/Arcee-VyLinh))
- **Parameters**: 3 billion
- **Context Length**: 32K tokens
- **Language**: Vietnamese-optimized with English support
- **Architecture**: Based on Qwen2.5-3B

### Performance Characteristics
- **Memory Requirements**: 8-16 GB RAM (depending on precision)
- **Storage**: 7-10 GB for model files
- **Inference Speed**: 
  - CPU: 2-5 tokens/second
  - GPU (8GB VRAM): 15-30 tokens/second
  - GPU (16GB+ VRAM): 30-60 tokens/second
- **Latency**: 1-3 seconds for typical responses

### Deployment Considerations
- **Cold Start**: 30-60 seconds for model loading
- **Warm-up Strategy**: Keep model in memory for better response times
- **Scaling**: Single instance can handle 10-50 concurrent requests
- **Monitoring**: Track GPU utilization, memory usage, and response times

## Traffic & Usage Patterns

### Conservative Usage (Early Stage)
- Daily Active Users: 100
- Queries per user per day: 3
- Daily requests: 300
- Peak concurrent users: 10
- Search requests: 200/day
- Q&A requests: 100/day

### Moderate Usage (Growth Stage)
- Daily Active Users: 1,000
- Queries per user per day: 5
- Daily requests: 5,000
- Peak concurrent users: 50
- Search requests: 3,000/day
- Q&A requests: 2,000/day

### Ambitious Usage (Mature Stage)
- Daily Active Users: 10,000
- Queries per user per day: 3
- Daily requests: 30,000
- Peak concurrent users: 200
- Search requests: 20,000/day
- Q&A requests: 10,000/day

### Request Patterns
- 70% traffic during business hours (8am-8pm)
- Peak load during 12pm-2pm and 6pm-8pm
- Search requests: Low compute, fast response (100ms-300ms)
- Q&A requests: High compute, longer response (2-10 seconds)

## Cost Breakdown

### Infrastructure Costs (Private Cloud)
- **GreenNode Server**: 
  - CPU: 8-16 cores (for LLM inference)
  - RAM: 16-32 GB (for 3B parameter model)
  - GPU: NVIDIA GPU with 8GB+ VRAM (recommended)
  - Storage: 50-100 GB (for model files, databases, logs)
  - Estimated monthly cost: $200-500 depending on provider

### Storage Requirements
- Self-host Supabase PostgreSQL: 2.3MB to 2.3GB
- ChromaDB Vector DB: 2.57MB to 2.57GB
- Arcee-VyLinh Model: 7-10 GB (fixed)
- Vercel hosting: Static assets (~100MB)

### Operational Costs
- **Electricity**: GPU-intensive workloads (~$50-100/month)
- **Internet**: High-speed connection for model downloads
- **Maintenance**: System administration and updates
- **Backup**: Model and database backup storage

### Bandwidth Estimation (per month)
- Conservative usage: 50GB/month
- Moderate usage: 500GB/month
- Ambitious usage: 2TB/month

### Bandwidth Costs
- Self-host Supabase: Internal network bandwidth only
- ChromaDB: Internal network bandwidth only
- LLM Service: Internal network bandwidth only
- Vercel: Free tier includes 1TB transfer

## Security & Compliance

### Data Protection
- Legal documents are public information
- All API endpoints secured with HTTPS
- Environment variables with secrets properly managed

### API Security
- Rate limiting to prevent abuse
- Input validation and sanitization
- Authentication for administrative functions (future consideration)

### Infrastructure Security
- CORS policies configured (in Flask app)
- Self-host Supabase Row Level Security (could be enabled)
- Private network isolation for database and LLM services
- API rate limiting for LLM service
- Model access controls and authentication

### Compliance
- HTTPS encryption for all data in transit
- Standard web application security practices

## Deployment Architecture

```
                    Internet
                       |
                  [Load Balancer]
                       |
        ┌──────────────┼──────────────┐
        |              |              |
    [Frontend]   [Law Service]   [RAG Service]
    (Vercel)      (Vercel)       (Vercel)
    Next.js        Node.js        Python/Flask
        |              |              |
        └──────────────┼──────────────┘
                       |
                [API Gateway]
                       |
        ┌──────────────┼──────────────┐
        |              |              |
[Self-host Supabase] [ChromaDB]   [LLM Service]
(PostgreSQL)    (Vector DB)    (GreenNode)
    87 docs       857 vectors    Arcee-VyLinh
   857 articles   768-dim emb.   3B params

Legend:
[ ] = Service/Component
| = Data Flow
```

### Components:
1. **Frontend (Vercel)**: Next.js 14 application with global CDN
2. **Law Service (Vercel)**: Node.js/Express API connecting to Self-host Supabase
3. **RAG Service (Vercel)**: Python/Flask API connecting to ChromaDB and LLM Service
4. **Self-host Supabase (PostgreSQL)**: Self-hosted PostgreSQL database
5. **ChromaDB (Vector Database)**: Self-hosted vector database
6. **LLM Service (GreenNode)**: Self-hosted Arcee-VyLinh model for Vietnamese Q&A

## Deployment Strategy

### Recommended Approach
1. **Deploy on private cloud** with self-hosted databases and LLM for full control
2. **Use Docker containers** for Supabase, ChromaDB, and LLM Service deployment
3. **Deploy LLM Service on GreenNode** with GPU acceleration for optimal performance
4. **Monitor usage closely** and scale gradually
5. **Consider container orchestration** (Kubernetes) for production scaling
6. **Implement model caching** and response optimization for better performance
7. **Set up monitoring** for model inference latency and resource usage
