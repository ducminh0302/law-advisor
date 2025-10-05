# VN Law Advisor Mini

> A lightweight Vietnamese legal document Q&A system with RAG (Retrieval-Augmented Generation)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

##  Overview

VN Law Advisor Mini is a simplified legal advisory system that helps users search and understand Vietnamese legal documents through:
- **Document Management** - Store and organize Vietnamese legal documents
- **AI-Powered Q&A** - Ask legal questions in natural language and get accurate answers
- **RAG Technology** - Combines retrieval and generation for context-aware responses

##  Architecture

```

              Frontend (Next.js 14)                  
  - Legal Document Search                            
  - Q&A Chat Interface                               

                                
                                
  
  Law Service           RAG Service             
  (Node.js/Express)     (Python/Flask)          
  - CRUD operations     - Vector search         
  - Search API          - LLM inference         
  
                                  
                                  
        
   Supabase               Pinecone      
   (PostgreSQL)           (Vector DB)   
        
```

##  Features

-  **Document Management** - Store Vietnamese legal documents with metadata
-  **Full-Text Search** - Search across documents and articles
-  **AI Q&A Chat** - Natural language legal questions
-  **RAG System** - Accurate answers using retrieval-augmented generation
-  **Vercel Deployable** - Ready for free tier deployment
-  **Secure Configuration** - Environment-based setup

##  Quick Start

### 🚀 Deploy to Production (5 minutes)

**Want to deploy immediately?** 

📘 Read: [`QUICK-DEPLOY.md`](./QUICK-DEPLOY.md) - 3-step deployment guide
📋 Checklist: [`DEPLOYMENT-CHECKLIST.md`](./DEPLOYMENT-CHECKLIST.md) - Full deployment checklist
📖 Detailed Guide: [`DEPLOYMENT.md`](./DEPLOYMENT.md) - Complete deployment documentation

### 💻 Local Development

#### Prerequisites

- Node.js 18+
- Python 3.8+
- Supabase account (free tier available)
- Pinecone account (optional, for vector search)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ducminh0302/law-advisor.git
cd law-advisor
```

2. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- Supabase URL and API key
- Pinecone API key (optional)
- Hugging Face token (for embeddings)

3. **Initialize database**
```bash
# Run the SQL schema in your Supabase project
# File: infrastructure/supabase-schema.sql
```

4. **Install dependencies and run services**

**Backend - Law Service:**
```bash
cd backend/law-service
npm install
npm start
```

**Backend - RAG Service:**
```bash
cd backend/rag-service
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd web
npm install
npm run dev
```

Access at `http://localhost:3000`

##  Project Structure

```
law-advisor/
 backend/
    law-service/          # REST API for legal documents
       src/
          routes/       # API endpoints
          db/           # Database connection
       package.json
    rag-service/          # RAG Q&A service
        app.py            # Flask application
        vectorize.py      # Document vectorization
        requirements.txt
 crawler/                  # Data collection scripts
    crawler.py           # Web scraper
    export_to_supabase.py # Database importer
 web/                     # Next.js frontend
    src/app/
       page.tsx         # Home page
       search/          # Search interface
       chat/            # Q&A chat
    package.json
 infrastructure/
    supabase-schema.sql  # Database schema
 docs/                    # Documentation
    01-SETUP-SUPABASE.md
    02-SETUP-VECTOR-DB.md
    03-SETUP-HUGGINGFACE.md
 crawl thu cong/          # Manual PDF documents
```

##  Tech Stack

### Backend
- **Law Service**: Node.js, Express.js, Supabase Client
- **RAG Service**: Python, Flask, LangChain, Sentence Transformers
- **Database**: PostgreSQL (via Supabase)
- **Vector Store**: Pinecone

### Frontend
- **Framework**: Next.js 14 with App Router
- **UI**: TailwindCSS
- **Language**: TypeScript

### AI/ML
- **Embeddings**: Sentence Transformers (Vietnamese models)
- **LLM Integration**: Compatible with OpenAI API
- **Vector Search**: Pinecone for similarity search

##  API Documentation

### Law Service Endpoints

```
GET    /api/documents          # List all documents
GET    /api/documents/:id      # Get document by ID
GET    /api/articles           # List all articles
GET    /api/search             # Search documents
```

### RAG Service Endpoints

```
POST   /api/ask                # Ask a legal question
POST   /api/vectorize          # Vectorize documents
```

##  Deployment

### Deploy to Vercel

Each service can be deployed independently:

```bash
# Deploy Law Service
cd backend/law-service
vercel --prod

# Deploy RAG Service
cd backend/rag-service
vercel --prod

# Deploy Frontend
cd web
vercel --prod
```

Update environment variables in Vercel dashboard for each deployment.

##  Database Schema

**Documents Table:**
- Stores legal document metadata (title, type, issue date, etc.)

**Articles Table:**
- Individual articles/clauses within documents
- Linked to parent document via foreign key

See `infrastructure/supabase-schema.sql` for complete schema.

##  Documentation

Detailed setup guides:

- [Quick Start Guide](docs/00-QUICK-START.md)
- [Supabase Setup](docs/01-SETUP-SUPABASE.md)
- [Vector Database Configuration](docs/02-SETUP-VECTOR-DB.md)
- [Hugging Face Integration](docs/03-SETUP-HUGGINGFACE.md)

##  Contributing

This is a personal project. Contributions, issues, and feature requests are welcome!

##  License

This project is licensed under the MIT License.

##  Acknowledgments

- Vietnamese legal documents from public government sources
- Built with modern AI/ML frameworks and cloud services

##  Contact

For questions or feedback, please open an issue on GitHub.

---

**Developed by ducminh0302**
