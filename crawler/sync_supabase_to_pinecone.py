"""
Sync Supabase Articles to Pinecone

Script này đọc articles từ Supabase và import vào Pinecone
để RAG service có thể search được các điều luật chi tiết.
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
print(f"📁 Loaded .env from: {env_path}")


def fetch_articles_from_supabase():
    """Fetch articles với thông tin document từ Supabase"""
    print("\n📥 Fetching articles from Supabase...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        return []
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Fetch all articles with document info
        print("   Querying articles table...")
        response = supabase.table('articles').select('*, documents(*)').execute()
        articles = response.data
        
        print(f"   Raw articles: {len(articles)}")
        
        # Convert to format compatible with vector store
        formatted_articles = []
        for art in articles:
            # Get article info
            article_id = art.get('id')
            if not article_id:
                continue
            
            # Get document info
            doc_info = art.get('documents', {})
            if not doc_info:
                doc_info = {}
            
            # Create mapc
            mapc = art.get('mapc', f"article-{article_id}")
            
            # Combine content
            ten = art.get('ten', 'Untitled')
            noi_dung = art.get('noi_dung', '')
            
            # Skip if no content
            if not noi_dung or len(noi_dung) < 20:
                continue
            
            # Create rich content for embedding
            doc_ten = doc_info.get('ten', '')
            doc_loai = doc_info.get('loai', '')
            chuong = art.get('chuong', '')
            
            # Tạo nội dung đầy đủ cho embedding
            full_content = f"{ten}\n\n{noi_dung}"
            if doc_ten:
                full_content = f"Văn bản: {doc_ten}\n{ten}\n\n{noi_dung}"
            
            article_data = {
                'mapc': mapc,
                'ten': ten,
                'noidung': full_content,
                'article_id': article_id,
                'document_id': art.get('document_id'),
                'document_name': doc_ten,
                'document_type': doc_loai,
                'document_number': doc_info.get('so_hieu', ''),
                'chuong': chuong,
                'muc': art.get('muc', ''),
                'thu_tu': art.get('thu_tu', 0),
            }
            
            formatted_articles.append(article_data)
        
        print(f"✅ Fetched {len(formatted_articles)} articles with content")
        return formatted_articles
        
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        import traceback
        traceback.print_exc()
        return []


def split_long_articles(articles, max_length=2000):
    """Chia các articles dài thành chunks nhỏ hơn"""
    chunks = []
    
    for art in articles:
        content = art['noidung']
        
        # Nếu ngắn, giữ nguyên
        if len(content) <= max_length:
            chunks.append(art)
            continue
        
        # Chia thành các chunks
        # Cố gắng chia theo đoạn văn
        paragraphs = content.split('\n\n')
        current_chunk = []
        current_length = 0
        chunk_idx = 1
        
        for para in paragraphs:
            para_length = len(para)
            
            if current_length + para_length > max_length and current_chunk:
                # Tạo chunk
                chunk = art.copy()
                chunk['mapc'] = f"{art['mapc']}-p{chunk_idx}"
                chunk['ten'] = f"{art['ten']} (Phần {chunk_idx})"
                chunk['noidung'] = '\n\n'.join(current_chunk)
                chunks.append(chunk)
                
                # Reset
                current_chunk = [para]
                current_length = para_length
                chunk_idx += 1
            else:
                current_chunk.append(para)
                current_length += para_length
        
        # Thêm phần còn lại
        if current_chunk:
            chunk = art.copy()
            if chunk_idx > 1:
                chunk['mapc'] = f"{art['mapc']}-p{chunk_idx}"
                chunk['ten'] = f"{art['ten']} (Phần {chunk_idx})"
            chunk['noidung'] = '\n\n'.join(current_chunk)
            chunks.append(chunk)
    
    return chunks


def main():
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description='Sync Supabase to Pinecone')
    parser.add_argument('--auto-confirm', '-y', action='store_true', 
                        help='Auto-confirm without prompting')
    parser.add_argument('--batch-size', type=int, default=50,
                        help='Batch size for uploading (default: 50)')
    args = parser.parse_args()
    
    print("="*70)
    print("🔄 SYNC SUPABASE ARTICLES TO PINECONE")
    print("="*70)
    
    # Check environment
    provider = os.getenv('VECTOR_DB_PROVIDER', 'pinecone')
    print(f"\n🔧 Vector DB Provider: {provider}")
    
    if provider == 'pinecone':
        api_key = os.getenv('PINECONE_API_KEY')
        index_name = os.getenv('PINECONE_INDEX_NAME')
        
        if not api_key or not index_name:
            print("\n❌ Missing Pinecone configuration!")
            print("   Please set in backend/rag-service/.env:")
            print("   - PINECONE_API_KEY=your_api_key")
            print("   - PINECONE_INDEX_NAME=your_index_name")
            sys.exit(1)
        
        print(f"   Index: {index_name}")
    
    # Fetch articles
    articles = fetch_articles_from_supabase()
    
    if not articles:
        print("\n❌ No articles found in Supabase!")
        print("   Run: python crawler/generate_fake_data.py")
        sys.exit(1)
    
    # Split long articles
    print(f"\n✂️  Processing articles...")
    chunks = split_long_articles(articles, max_length=2000)
    print(f"   Created {len(chunks)} chunks from {len(articles)} articles")
    
    # Show statistics
    print(f"\n📊 Statistics:")
    print(f"   - Total articles: {len(articles)}")
    print(f"   - Total chunks: {len(chunks)}")
    avg_length = sum(len(c['noidung']) for c in chunks) / len(chunks)
    print(f"   - Average chunk length: {int(avg_length)} chars")
    
    # Initialize vector store
    print(f"\n🔌 Initializing {provider} vector store...")
    try:
        vector_store = VectorStore(provider=provider)
        print("✅ Vector store connected")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Confirm
    if not args.auto_confirm:
        print(f"\n⚠️  About to create embeddings for {len(chunks)} text chunks")
        print(f"   This may take 5-15 minutes depending on data size...")
        print(f"   Embedding model: paraphrase-multilingual-mpnet-base-v2")
        
        confirm = input("\n   Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Cancelled")
            sys.exit(0)
    else:
        print("\n✅ Auto-confirm enabled, proceeding...")
    
    # Upload to vector store
    print(f"\n🚀 Creating embeddings and uploading to {provider}...")
    print("   This will take a while, please be patient...")
    
    try:
        batch_size = args.batch_size
        total_uploaded = 0
        failed_count = 0
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(chunks) + batch_size - 1) // batch_size
            
            print(f"\n   📦 Batch {batch_num}/{total_batches} ({len(batch)} items)...")
            
            try:
                count = vector_store.upsert_batch(batch)
                total_uploaded += count
                print(f"      ✅ Uploaded {count} vectors")
                print(f"      Progress: {total_uploaded}/{len(chunks)} ({100*total_uploaded//len(chunks)}%)")
            except Exception as e:
                failed_count += len(batch)
                print(f"      ❌ Batch failed: {e}")
        
        print(f"\n{'='*70}")
        print(f"✅ UPLOAD COMPLETE!")
        print(f"   - Successfully uploaded: {total_uploaded} vectors")
        print(f"   - Failed: {failed_count}")
        print(f"   - Success rate: {100*total_uploaded//len(chunks)}%")
        print(f"{'='*70}")
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Test search
    print("\n" + "="*70)
    print("🔍 TESTING VECTOR SEARCH")
    print("="*70)
    
    test_queries = [
        "quyền sở hữu đất đai",
        "thành lập doanh nghiệp",
        "thuế thu nhập doanh nghiệp",
        "điều kiện đầu tư",
        "xử lý vi phạm"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        try:
            results = vector_store.search(query, top_k=3)
            print(f"   Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                score = result.get('score', 0)
                title = result.get('ten', 'Unknown')
                doc_name = result.get('document_name', '')
                if doc_name:
                    print(f"   {i}. [{doc_name[:30]}...] {title[:40]}... (score: {score:.3f})")
                else:
                    print(f"   {i}. {title[:60]}... (score: {score:.3f})")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    print("\n" + "="*70)
    print("✅ DONE! Pinecone is ready for RAG")
    print("="*70)
    print("\n💡 Next steps:")
    print("   1. Start RAG service: cd backend/rag-service && python app.py")
    print("   2. Test search API at: http://localhost:8001/api/search")
    print("   3. Check Pinecone dashboard to verify vectors")
    print("\n")


if __name__ == '__main__':
    main()

