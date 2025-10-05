"""
Import Documents to Pinecone

Script này đọc văn bản từ Supabase và import vào Pinecone
để RAG service có thể search được.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Add rag-service src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'rag-service', 'src'))

# Patch torch before importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'rag-service'))
import patch_torch

from models.vector_store import VectorStore

# Load .env từ rag-service
env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'rag-service', '.env')
load_dotenv(env_path)
print(f"Loaded .env from: {env_path}")


def fetch_documents_from_supabase():
    """Fetch documents từ Supabase"""
    print("📥 Fetching documents from Supabase...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        return []
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Fetch all documents
        response = supabase.table('documents').select('*').execute()
        docs = response.data
        
        # Convert to format compatible with vectorize
        documents = []
        for doc in docs:
            # Make sure we have a valid ID
            doc_id = doc.get('id')
            if not doc_id:
                continue
                
            mapc = doc.get('mapc')
            if not mapc or mapc == '':
                mapc = f"doc-{doc_id}"
            
            document = {
                'mapc': mapc,
                'ten': doc.get('ten', 'Untitled'),
                'noidung': doc.get('noi_dung', '') or doc.get('content', ''),
                'document_id': doc_id,
                'document_type': doc.get('loai', ''),
                'document_number': doc.get('so_hieu', ''),
            }
            
            # Only add if has content
            if document['noidung'] and len(document['noidung']) > 50:
                documents.append(document)
        
        print(f"✅ Fetched {len(documents)} documents")
        return documents
        
    except Exception as e:
        print(f"❌ Error fetching documents: {e}")
        import traceback
        traceback.print_exc()
        return []


def split_into_chunks(documents, chunk_size=1000):
    """Chia văn bản dài thành các chunks nhỏ hơn"""
    chunks = []
    
    for doc in documents:
        content = doc['noidung']
        
        # Nếu văn bản ngắn, giữ nguyên
        if len(content) <= chunk_size:
            chunks.append(doc)
            continue
        
        # Chia thành các chunks
        words = content.split()
        current_chunk = []
        current_length = 0
        chunk_idx = 1
        
        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1
            
            if current_length >= chunk_size:
                # Tạo chunk mới
                chunk = doc.copy()
                chunk['mapc'] = f"{doc['mapc']}-chunk{chunk_idx}"
                chunk['ten'] = f"{doc['ten']} (Phần {chunk_idx})"
                chunk['noidung'] = ' '.join(current_chunk)
                chunks.append(chunk)
                
                # Reset
                current_chunk = []
                current_length = 0
                chunk_idx += 1
        
        # Thêm phần còn lại
        if current_chunk:
            chunk = doc.copy()
            chunk['mapc'] = f"{doc['mapc']}-chunk{chunk_idx}"
            chunk['ten'] = f"{doc['ten']} (Phần {chunk_idx})"
            chunk['noidung'] = ' '.join(current_chunk)
            chunks.append(chunk)
    
    return chunks


def main():
    print("="*60)
    print("📚 IMPORT DOCUMENTS TO PINECONE")
    print("="*60)
    
    # Check environment
    provider = os.getenv('VECTOR_DB_PROVIDER', 'pinecone')
    print(f"\n🔧 Vector DB Provider: {provider}")
    
    if provider == 'pinecone':
        api_key = os.getenv('PINECONE_API_KEY')
        index_name = os.getenv('PINECONE_INDEX_NAME')
        
        if not api_key or not index_name:
            print("\n❌ Missing Pinecone configuration!")
            print("   Please set in .env:")
            print("   - PINECONE_API_KEY")
            print("   - PINECONE_INDEX_NAME")
            sys.exit(1)
        
        print(f"   Index: {index_name}")
    
    # Fetch documents
    documents = fetch_documents_from_supabase()
    
    if not documents:
        print("\n❌ No documents found!")
        sys.exit(1)
    
    # Split into chunks
    print(f"\n✂️  Splitting documents into chunks...")
    chunks = split_into_chunks(documents, chunk_size=1500)
    print(f"   Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Initialize vector store
    print(f"\n🔌 Initializing {provider} vector store...")
    try:
        vector_store = VectorStore(provider=provider)
        print("✅ Vector store initialized")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Confirm
    print(f"\n⚠️  About to create embeddings for {len(chunks)} text chunks")
    print(f"   This may take 5-10 minutes...")
    print(f"   Embedding model: paraphrase-multilingual-mpnet-base-v2")
    
    confirm = input("\n   Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        sys.exit(0)
    
    # Upload to vector store
    print(f"\n🚀 Creating embeddings and uploading to {provider}...")
    print("   This will take a while, please wait...")
    
    try:
        # Batch processing
        batch_size = 50
        total_uploaded = 0
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            count = vector_store.upsert_batch(batch)
            total_uploaded += count
            print(f"   Progress: {total_uploaded}/{len(chunks)} chunks uploaded")
        
        print(f"\n✅ SUCCESS! Uploaded {total_uploaded} embeddings to {provider}")
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Test search
    print("\n" + "="*60)
    print("🔍 TESTING VECTOR SEARCH")
    print("="*60)
    
    test_queries = [
        "thanh niên khởi nghiệp",
        "đoàn viên",
        "kế hoạch hoạt động"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        try:
            results = vector_store.search(query, top_k=3)
            print(f"   Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                score = result.get('score', 0)
                title = result.get('ten', 'Unknown')
                print(f"   {i}. {title[:60]}... (score: {score:.3f})")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    print("\n" + "="*60)
    print("✅ DONE! Pinecone is ready for RAG service")
    print("="*60)
    print("\n💡 Next steps:")
    print("   1. Start RAG service: python backend/rag-service/app.py")
    print("   2. Test search API at: http://localhost:8001/api/search")
    print("\n")


if __name__ == '__main__':
    main()
