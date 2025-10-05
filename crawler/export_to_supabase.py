"""
Export crawled data to Supabase

Đọc JSON files từ crawler và insert vào Supabase PostgreSQL
"""

import json
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for write access

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def load_json(filepath):
    """Load JSON file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def export_documents(documents):
    """
    Export documents to Supabase

    Args:
        documents: List of document dicts

    Returns:
        Dict mapping old doc_id (string) to new doc_id (int)
    """
    print(f"\n📤 Exporting {len(documents)} documents...")

    id_mapping = {}
    success_count = 0
    error_count = 0

    for doc in documents:
        try:
            # Prepare data for Supabase
            data = {
                'ten': doc.get('ten', ''),
                'loai': doc.get('loai', ''),
                'so_hieu': doc.get('so_hieu', ''),
                'ngay_ban_hanh': doc.get('ngay_ban_hanh'),
                'ngay_hieu_luc': doc.get('ngay_hieu_luc'),
                'trang_thai': doc.get('trang_thai', 'Còn hiệu lực'),
                'co_quan_ban_hanh': doc.get('co_quan_ban_hanh', ''),
                'nguoi_ky': doc.get('nguoi_ky', ''),
                'noi_dung': doc.get('noi_dung', ''),
                'ghi_chu': f"Crawled from vbpl.vn, ItemID={doc.get('id')}"
            }

            # Insert to Supabase
            result = supabase.table('documents').insert(data).execute()

            if result.data and len(result.data) > 0:
                new_id = result.data[0]['id']
                old_id = doc.get('id')
                id_mapping[old_id] = new_id
                success_count += 1
                print(f"  ✅ Document {old_id} → DB ID {new_id}: {doc.get('ten', '')[:50]}...")
            else:
                error_count += 1
                print(f"  ❌ Failed to insert document {doc.get('id')}")

        except Exception as e:
            error_count += 1
            print(f"  ❌ Error inserting document {doc.get('id')}: {e}")

    print(f"\n📊 Documents: {success_count} success, {error_count} errors")
    return id_mapping


def export_articles(articles, id_mapping):
    """
    Export articles to Supabase

    Args:
        articles: List of article dicts
        id_mapping: Dict mapping old doc_id to new doc_id

    Returns:
        Number of successful inserts
    """
    print(f"\n📤 Exporting {len(articles)} articles...")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for article in articles:
        old_doc_id = article.get('document_id')

        # Map old document_id to new Supabase ID
        if old_doc_id not in id_mapping:
            skipped_count += 1
            print(f"  ⚠️ Skipped article (document not found): {article.get('mapc')}")
            continue

        new_doc_id = id_mapping[old_doc_id]

        try:
            data = {
                'mapc': article.get('mapc', ''),
                'document_id': new_doc_id,
                'ten': article.get('ten', ''),
                'noi_dung': article.get('noi_dung', ''),
                'chuong': article.get('chuong', ''),
                'muc': article.get('muc', ''),
                'thu_tu': article.get('thu_tu', 0)
            }

            result = supabase.table('articles').insert(data).execute()

            if result.data and len(result.data) > 0:
                success_count += 1
                if success_count % 10 == 0:  # Print every 10 articles
                    print(f"  ✅ Inserted {success_count} articles...")
            else:
                error_count += 1

        except Exception as e:
            error_count += 1
            print(f"  ❌ Error inserting article {article.get('mapc')}: {e}")

    print(f"\n📊 Articles: {success_count} success, {error_count} errors, {skipped_count} skipped")
    return success_count


def verify_export():
    """Verify data in Supabase"""
    print(f"\n🔍 Verifying export...")

    try:
        # Count documents
        doc_result = supabase.table('documents').select('id', count='exact').execute()
        doc_count = doc_result.count if hasattr(doc_result, 'count') else len(doc_result.data)

        # Count articles
        article_result = supabase.table('articles').select('id', count='exact').execute()
        article_count = article_result.count if hasattr(article_result, 'count') else len(article_result.data)

        print(f"  📄 Total documents in DB: {doc_count}")
        print(f"  📋 Total articles in DB: {article_count}")

        return True
    except Exception as e:
        print(f"  ❌ Verification error: {e}")
        return False


def main():
    """Main function"""
    print("🚀 VN-Law-Mini Data Exporter")
    print("=" * 50)

    # Check connection
    print("\n🔗 Testing Supabase connection...")
    try:
        result = supabase.table('documents').select('id').limit(1).execute()
        print("  ✅ Connection successful!")
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        print("\n💡 Make sure:")
        print("  1. SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env")
        print("  2. Database schema has been created (run supabase-schema.sql)")
        sys.exit(1)

    # Load data
    data_dir = "./data"
    documents_file = f"{data_dir}/documents.json"
    articles_file = f"{data_dir}/articles.json"

    print(f"\n📂 Loading data from {data_dir}/...")
    documents = load_json(documents_file)
    articles = load_json(articles_file)

    if not documents:
        print("❌ No documents found! Run crawler.py first.")
        sys.exit(1)

    print(f"  ✅ Loaded {len(documents)} documents")
    print(f"  ✅ Loaded {len(articles)} articles")

    # Confirm before export
    print(f"\n⚠️  About to export to Supabase:")
    print(f"  - {len(documents)} documents")
    print(f"  - {len(articles)} articles")
    confirm = input("\nContinue? (y/n): ")

    if confirm.lower() != 'y':
        print("❌ Export cancelled.")
        sys.exit(0)

    # Export documents
    id_mapping = export_documents(documents)

    if not id_mapping:
        print("❌ No documents exported. Aborting.")
        sys.exit(1)

    # Export articles
    export_articles(articles, id_mapping)

    # Verify
    verify_export()

    print(f"\n✅ DONE! Data exported to Supabase.")


if __name__ == "__main__":
    main()
