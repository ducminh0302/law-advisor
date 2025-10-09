"""
Clean up Supabase data only

Script này sẽ xóa tất cả dữ liệu trừ 3 dòng đầu tiên trên Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'rag-service', '.env')
load_dotenv(env_path)
print(f"✓ Loaded .env from: {env_path}")


def cleanup_supabase():
    """Clean up Supabase data, keep only first 3 rows"""
    print("\n" + "="*60)
    print("🗑️  CLEANING UP SUPABASE")
    print("="*60)
    
    supabase_url = os.getenv('SUPABASE_URL')
    
    # Try service key first, fallback to anon key
    supabase_key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        print("   Make sure SUPABASE_URL and (SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY) are set in .env")
        return False
    
    key_type = "SERVICE_KEY" if os.getenv('SUPABASE_SERVICE_KEY') else "ANON_KEY"
    print(f"   Using {key_type} for authentication")
    
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
            
            # Delete documents one by one or in batch
            delete_ids = [d['id'] for d in docs_to_delete]
            
            # Try batch delete first
            try:
                result = supabase.table('documents').delete().in_('id', delete_ids).execute()
                print(f"   ✅ Deleted {len(docs_to_delete)} documents")
            except Exception as batch_error:
                print(f"   ⚠️  Batch delete failed: {batch_error}")
                print("   🔄 Trying individual deletes...")
                
                success_count = 0
                for doc_id in delete_ids:
                    try:
                        supabase.table('documents').delete().eq('id', doc_id).execute()
                        success_count += 1
                    except Exception as e:
                        print(f"      ❌ Failed to delete document {doc_id}: {e}")
                
                print(f"   ✅ Deleted {success_count}/{len(docs_to_delete)} documents")
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
            
            # Try batch delete first
            try:
                result = supabase.table('articles').delete().in_('id', delete_ids).execute()
                print(f"   ✅ Deleted {len(articles_to_delete)} articles")
            except Exception as batch_error:
                print(f"   ⚠️  Batch delete failed: {batch_error}")
                print("   🔄 Trying individual deletes...")
                
                success_count = 0
                for article_id in delete_ids:
                    try:
                        supabase.table('articles').delete().eq('id', article_id).execute()
                        success_count += 1
                    except Exception as e:
                        print(f"      ❌ Failed to delete article {article_id}: {e}")
                
                print(f"   ✅ Deleted {success_count}/{len(articles_to_delete)} articles")
        else:
            print(f"   ℹ️  Only {len(all_articles)} articles found, nothing to delete")
        
        print("\n✅ Supabase cleanup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("🧹 SUPABASE DATA CLEANUP TOOL")
    print("="*60)
    print("\n⚠️  WARNING: This will delete all data except the first 3 rows")
    print("   from Supabase (documents and articles tables)!")
    print("\n" + "="*60)
    
    success = cleanup_supabase()
    
    if success:
        print("\n✅ Cleanup completed successfully!")
    else:
        print("\n⚠️  Cleanup failed. Please check the logs above.")


if __name__ == '__main__':
    main()
