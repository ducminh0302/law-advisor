"""
Vectorize Script

Tạo embeddings cho tất cả articles từ Supabase
và upload lên Vector DB (Pinecone/ChromaDB)
"""

import os
import sys

# Patch torch.load BEFORE importing anything else
import patch_torch

from dotenv import load_dotenv
from supabase import create_client, Client

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.vector_store import VectorStore

load_dotenv()


def fetch_articles_from_supabase():
    """Fetch all articles from Supabase"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY are required")

    supabase: Client = create_client(supabase_url, supabase_key)

    print("Fetching articles from Supabase...")

    # Fetch all articles
    response = supabase.table('articles').select('mapc, ten, noi_dung, document_id').execute()

    articles = response.data
    
    # Normalize field names (noi_dung -> noidung for compatibility)
    for article in articles:
        if 'noi_dung' in article:
            article['noidung'] = article['noi_dung']
    
    print(f"Fetched {len(articles)} articles")

    return articles


def main():
    """Main function"""
    print("=" * 60)
    print("VN-Law-Mini - Vectorize Articles")
    print("=" * 60)

    # Get provider from env or use default
    provider = os.getenv('VECTOR_DB_PROVIDER', 'pinecone')
    print(f"\nUsing vector DB: {provider}")

    # Fetch articles
    try:
        articles = fetch_articles_from_supabase()
    except Exception as e:
        print(f"Error fetching articles: {e}")
        print("\nMake sure:")
        print("  1. Supabase credentials are set in .env")
        print("  2. Articles exist in database")
        sys.exit(1)

    if not articles:
        print("No articles found in database!")
        sys.exit(1)

    # Initialize vector store
    try:
        print(f"\nInitializing {provider} vector store...")
        vector_store = VectorStore(provider=provider)
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        print("\nMake sure:")
        if provider == 'pinecone':
            print("  1. PINECONE_API_KEY is set")
            print("  2. PINECONE_INDEX_NAME is set")
            print("  3. Index exists in Pinecone dashboard")
        else:
            print("  1. ChromaDB is configured")
        sys.exit(1)

    # Confirm before proceeding
    print(f"\nAbout to create embeddings for {len(articles)} articles")
    print("This may take a while (few minutes)...")
    confirm = input("\nContinue? (y/n): ")

    if confirm.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Create and upsert embeddings
    try:
        print("\nCreating embeddings and uploading...")
        count = vector_store.upsert_batch(articles)
        print(f"\nSuccess! Uploaded {count} embeddings to {provider}")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

    # Test search
    print("\n" + "=" * 60)
    print("Testing vector search...")
    print("=" * 60)

    test_query = "Phạm vi điều chỉnh của Bộ luật Dân sự là gì?"
    print(f"\nQuery: {test_query}")

    results = vector_store.search(test_query, top_k=3)

    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['ten']} (score: {result['score']:.3f})")
        print(f"   MAPC: {result['mapc']}")
        print(f"   Content: {result['noidung'][:150]}...")

    print("\nDone! Vector DB is ready for RAG.")


if __name__ == "__main__":
    main()
