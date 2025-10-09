"""
Simple Sync to Pinecone - Standalone version
Sync articles từ Supabase lên Pinecone
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment
load_dotenv()

print("="*70)
print("SYNC SUPABASE TO PINECONE")
print("="*70)

# Get credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX_NAME', 'law-advisor-mini')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\nERROR: Missing Supabase credentials")
    print("Please set in .env:")
    print("  SUPABASE_URL=...")
    print("  SUPABASE_SERVICE_KEY=...")
    sys.exit(1)

if not PINECONE_API_KEY:
    print("\nWARNING: PINECONE_API_KEY not found in .env")
    print("Please enter your Pinecone credentials:")
    print("(Get from: https://app.pinecone.io)")
    PINECONE_API_KEY = input("\nPinecone API Key: ").strip()
    
    if not PINECONE_API_KEY:
        print("ERROR: Pinecone API Key required")
        sys.exit(1)
    
    PINECONE_INDEX = input(f"Pinecone Index Name (default: {PINECONE_INDEX}): ").strip() or PINECONE_INDEX

print(f"\nConfiguration:")
print(f"  Supabase URL: {SUPABASE_URL[:30]}...")
print(f"  Pinecone Index: {PINECONE_INDEX}")

# Fetch articles from Supabase
print("\nFetching articles from Supabase...")
try:
    # Try with options parameter for newer SDK
    try:
        from supabase.client import ClientOptions
        supabase: Client = create_client(
            SUPABASE_URL, 
            SUPABASE_KEY,
            options=ClientOptions(
                auto_refresh_token=False,
                persist_session=False
            )
        )
    except:
        # Fallback for older SDK
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    response = supabase.table('articles').select('*, documents(*)').execute()
    articles = response.data
    print(f"  Found {len(articles)} articles")
except Exception as e:
    print(f"ERROR fetching from Supabase: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if not articles:
    print("ERROR: No articles found in Supabase")
    sys.exit(1)

# Prepare data for Pinecone
print("\nPreparing data...")
vectors_data = []

for art in articles:
    article_id = art.get('id')
    if not article_id:
        continue
    
    doc_info = art.get('documents', {}) or {}
    mapc = art.get('mapc', f"article-{article_id}")
    ten = art.get('ten', '')
    noi_dung = art.get('noi_dung', '')
    
    if not noi_dung or len(noi_dung) < 20:
        continue
    
    # Create metadata
    metadata = {
        'mapc': mapc,
        'ten': ten,
        'noidung': noi_dung[:500],  # First 500 chars for preview
        'article_id': article_id,
        'document_id': art.get('document_id'),
        'document_name': doc_info.get('ten', ''),
        'document_type': doc_info.get('loai', ''),
        'chuong': art.get('chuong', '') or '',
        'text': noi_dung,  # Full text for embedding
    }
    
    vectors_data.append(metadata)

print(f"  Prepared {len(vectors_data)} articles for embedding")

# Initialize Pinecone
print("\nInitializing Pinecone...")
try:
    from pinecone import Pinecone, ServerlessSpec
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists
    existing_indexes = pc.list_indexes().names()
    
    if PINECONE_INDEX not in existing_indexes:
        print(f"  Creating new index: {PINECONE_INDEX}")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=768,  # paraphrase-multilingual-mpnet-base-v2
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print("  Index created successfully")
    else:
        print(f"  Index {PINECONE_INDEX} already exists")
    
    index = pc.Index(PINECONE_INDEX)
    print("  Connected to index")
    
except Exception as e:
    print(f"ERROR: Failed to initialize Pinecone: {e}")
    print("\nTrying older Pinecone SDK version...")
    try:
        import pinecone
        pinecone.init(api_key=PINECONE_API_KEY, environment="gcp-starter")
        
        # Check existing indexes
        if PINECONE_INDEX not in pinecone.list_indexes():
            print(f"  Creating index: {PINECONE_INDEX}")
            pinecone.create_index(
                name=PINECONE_INDEX,
                dimension=768,
                metric='cosine'
            )
        
        index = pinecone.Index(PINECONE_INDEX)
        print("  Connected to index (legacy SDK)")
    except Exception as e2:
        print(f"ERROR: {e2}")
        sys.exit(1)

# Create embeddings
print("\nCreating embeddings...")
print("  Loading embedding model...")

try:
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    print("  Model loaded successfully")
    
except Exception as e:
    print(f"ERROR: Failed to load embedding model: {e}")
    print("\nPlease install required packages:")
    print("  pip install sentence-transformers")
    sys.exit(1)

# Process in batches
print("\nUploading to Pinecone...")
batch_size = 50
total_uploaded = 0

for i in range(0, len(vectors_data), batch_size):
    batch = vectors_data[i:i+batch_size]
    batch_num = (i // batch_size) + 1
    total_batches = (len(vectors_data) + batch_size - 1) // batch_size
    
    print(f"\n  Batch {batch_num}/{total_batches} ({len(batch)} items)...")
    
    try:
        # Create embeddings
        texts = [item['text'] for item in batch]
        embeddings = model.encode(texts, show_progress_bar=False)
        
        # Prepare vectors for Pinecone
        vectors = []
        for j, (item, embedding) in enumerate(zip(batch, embeddings)):
            vector_id = f"article-{item['article_id']}"
            
            # Remove 'text' from metadata (too large)
            metadata = {k: v for k, v in item.items() if k != 'text'}
            
            vectors.append({
                'id': vector_id,
                'values': embedding.tolist(),
                'metadata': metadata
            })
        
        # Upload to Pinecone
        index.upsert(vectors=vectors)
        total_uploaded += len(vectors)
        
        print(f"    Uploaded {len(vectors)} vectors")
        print(f"    Progress: {total_uploaded}/{len(vectors_data)} ({100*total_uploaded//len(vectors_data)}%)")
        
    except Exception as e:
        print(f"    ERROR in batch: {e}")

print(f"\n{'='*70}")
print(f"UPLOAD COMPLETE!")
print(f"  Successfully uploaded: {total_uploaded}/{len(vectors_data)} vectors")
print(f"  Success rate: {100*total_uploaded//len(vectors_data)}%")
print(f"{'='*70}")

# Test search
print("\nTesting search...")
try:
    test_query = "thanh lap doanh nghiep"
    print(f"  Query: '{test_query}'")
    
    query_embedding = model.encode([test_query])[0]
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=3,
        include_metadata=True
    )
    
    print(f"  Found {len(results['matches'])} results:")
    for i, match in enumerate(results['matches'], 1):
        score = match['score']
        title = match['metadata'].get('ten', 'Unknown')
        print(f"    {i}. {title[:50]}... (score: {score:.3f})")
    
except Exception as e:
    print(f"  Search test failed: {e}")

print(f"\n{'='*70}")
print("DONE! Pinecone is ready for RAG")
print(f"{'='*70}\n")

