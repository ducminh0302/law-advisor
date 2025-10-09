"""
Clean up data on Supabase and Pinecone

Script này sẽ xóa tất cả dữ liệu trừ 3 dòng đầu tiên trên:
- Supabase (documents và articles tables)
- Pinecone vector database
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
print(f"✓ Loaded .env from: {env_path}")


def cleanup_supabase():
    """Clean up Supabase data, keep only first 3 rows"""
    print("\n" + "="*60)
    print("🗑️  CLEANING UP SUPABASE")
    print("="*60)
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY')  # Need service key for deletion
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        print("   Make sure SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env")
        return False
    
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Clean up documents table
        print("\n📋 Documents table:")
        response = supabase.table('documents').select('id').order('id').execute()
        all_docs = response.data
        
        print(f"   Total documents: {len(all_docs)}")
        
        if len(all_docs) > 3:
            # Keep first 3, delete the rest
            docs_to_keep = all_docs[:3]
            docs_to_delete = all_docs[3:]
            
            print(f"   ✓ Keeping first 3 documents: {[d['id'] for d in docs_to_keep]}")
            print(f"   🗑️  Deleting {len(docs_to_delete)} documents...")
            
            # Delete documents
            delete_ids = [d['id'] for d in docs_to_delete]
            result = supabase.table('documents').delete().in_('id', delete_ids).execute()
            
            print(f"   ✅ Deleted {len(docs_to_delete)} documents")
        else:
            print(f"   ℹ️  Only {len(all_docs)} documents found, nothing to delete")
        
        # Clean up articles table
        print("\n📰 Articles table:")
        response = supabase.table('articles').select('id').order('id').execute()
        all_articles = response.data
        
        print(f"   Total articles: {len(all_articles)}")
        
        if len(all_articles) > 3:
            # Keep first 3, delete the rest
            articles_to_keep = all_articles[:3]
            articles_to_delete = all_articles[3:]
            
            print(f"   ✓ Keeping first 3 articles: {[a['id'] for a in articles_to_keep]}")
            print(f"   🗑️  Deleting {len(articles_to_delete)} articles...")
            
            # Delete articles
            delete_ids = [a['id'] for a in articles_to_delete]
            result = supabase.table('articles').delete().in_('id', delete_ids).execute()
            
            print(f"   ✅ Deleted {len(articles_to_delete)} articles")
        else:
            print(f"   ℹ️  Only {len(all_articles)} articles found, nothing to delete")
        
        print("\n✅ Supabase cleanup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_pinecone():
    """Clean up Pinecone data, keep only first 3 vectors"""
    print("\n" + "="*60)
    print("🗑️  CLEANING UP PINECONE")
    print("="*60)
    
    try:
        # Initialize VectorStore
        print("\n🔧 Initializing Pinecone connection...")
        vector_store = VectorStore()
        
        # Get all vector IDs
        print("\n📊 Fetching all vectors from Pinecone...")
        
        # Query to get all IDs (fetch in batches)
        all_ids = []
        
        # Use describe_index_stats to get total count
        stats = vector_store.index.describe_index_stats()
        total_vectors = stats.total_vector_count
        print(f"   Total vectors in Pinecone: {total_vectors}")
        
        if total_vectors <= 3:
            print(f"   ℹ️  Only {total_vectors} vectors found, nothing to delete")
            return True
        
        # Fetch all IDs by querying
        # We'll query with a dummy vector to get all matches
        print("\n🔍 Fetching vector IDs...")
        
        # Get first 3 IDs to keep
        query_result = vector_store.index.query(
            vector=[0.0] * 768,  # Dummy vector
            top_k=3,
            include_metadata=False
        )
        
        ids_to_keep = [match['id'] for match in query_result['matches']]
        print(f"   ✓ Keeping first 3 vectors: {ids_to_keep}")
        
        # Get all other IDs to delete
        # Query with larger top_k to get all vectors
        query_result = vector_store.index.query(
            vector=[0.0] * 768,
            top_k=10000,  # Large number to get all
            include_metadata=False
        )
        
        all_ids = [match['id'] for match in query_result['matches']]
        ids_to_delete = [id for id in all_ids if id not in ids_to_keep]
        
        print(f"   🗑️  Deleting {len(ids_to_delete)} vectors...")
        
        if ids_to_delete:
            # Delete in batches of 100
            batch_size = 100
            for i in range(0, len(ids_to_delete), batch_size):
                batch = ids_to_delete[i:i+batch_size]
                vector_store.index.delete(ids=batch)
                print(f"      Deleted batch {i//batch_size + 1}/{(len(ids_to_delete)-1)//batch_size + 1}")
            
            print(f"   ✅ Deleted {len(ids_to_delete)} vectors")
        
        print("\n✅ Pinecone cleanup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up Pinecone: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main cleanup function"""
    print("\n" + "="*60)
    print("🧹 DATA CLEANUP TOOL")
    print("="*60)
    print("\n⚠️  WARNING: This will delete all data except the first 3 rows")
    print("   from both Supabase and Pinecone!")
    print("\n" + "="*60)
    
    # Check for --force flag to skip confirmation
    if '--force' not in sys.argv:
        # Ask for confirmation
        confirm = input("\n❓ Are you sure you want to continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("\n❌ Cleanup cancelled")
            return
    else:
        print("\n⚠️  Running in FORCE mode (skipping confirmation)")
    
    print("\n🚀 Starting cleanup process...")
    
    # Clean up Supabase
    supabase_success = cleanup_supabase()
    
    # Clean up Pinecone
    pinecone_success = cleanup_pinecone()
    
    # Summary
    print("\n" + "="*60)
    print("📊 CLEANUP SUMMARY")
    print("="*60)
    print(f"   Supabase: {'✅ Success' if supabase_success else '❌ Failed'}")
    print(f"   Pinecone: {'✅ Success' if pinecone_success else '❌ Failed'}")
    print("="*60)
    
    if supabase_success and pinecone_success:
        print("\n✅ All cleanup operations completed successfully!")
    else:
        print("\n⚠️  Some cleanup operations failed. Please check the logs above.")


if __name__ == '__main__':
    main()
