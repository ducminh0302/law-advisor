"""
Import Manual Documents from TXT Files

Script này xử lý các file văn bản hành chính (PDF đã convert sang TXT)
từ folder "crawl thu cong" và import vào Supabase.

Tự động nhận diện:
- Loại văn bản (Công văn, Quyết định, Nghị quyết, Kế hoạch, Thông báo, etc.)
- Số hiệu văn bản
- Ngày ban hành
- Cơ quan ban hành
- Người ký
"""

import os
import re
import json
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
from pathlib import Path

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


class ManualDocumentParser:
    """Parse văn bản hành chính từ file TXT"""
    
    def __init__(self):
        # Patterns để nhận diện loại văn bản
        self.doc_type_patterns = {
            'Công văn': [r'CÔNG VĂN', r'Số:\s*\d+[/-]?CV', r'CV/', r'V/v'],
            'Quyết định': [r'QUYẾT ĐỊNH', r'Số:\s*\d+[/-]?QĐ', r'QĐ/'],
            'Nghị quyết': [r'NGHỊ QUYẾT', r'NQ/', r'Số:\s*\d+[/-]?NQ'],
            'Kế hoạch': [r'KẾ HOẠCH', r'KH/', r'Kế hoạch'],
            'Thông báo': [r'THÔNG BÁO', r'TB/', r'Thông báo số'],
            'Báo cáo': [r'BÁO CÁO', r'BC/', r'Báo cáo'],
            'Hướng dẫn': [r'HƯỚNG DẪN', r'HD/', r'Hướng dẫn'],
            'Thể lệ': [r'THỂ LỆ', r'Thể lệ'],
            'Chương trình': [r'CHƯƠNG TRÌNH', r'Chương trình'],
            'Điều lệ': [r'ĐIỀU LỆ', r'Điều lệ']
        }
        
        # Patterns cơ quan ban hành
        self.co_quan_patterns = [
            r'BAN CHẤP HÀNH TRUNG ƯƠNG',
            r'ĐOÀN TNCS HỒ CHÍ MINH',
            r'TRUNG ƯƠNG ĐOÀN',
            r'BỘ.*',
            r'UBND.*',
            r'CHÍNH PHỦ'
        ]
    
    def parse_file(self, filepath):
        """
        Parse một file txt và trích xuất metadata
        
        Returns:
            Dict chứa thông tin văn bản
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(filepath)
            
            # Extract metadata
            doc_info = {
                'filename': filename,
                'ten': self._extract_title(content, filename),
                'loai': self._detect_doc_type(content, filename),
                'so_hieu': self._extract_so_hieu(content),
                'ngay_ban_hanh': self._extract_date(content),
                'co_quan_ban_hanh': self._extract_co_quan(content),
                'nguoi_ky': self._extract_nguoi_ky(content),
                'noi_dung': content.strip(),
                'trang_thai': 'Còn hiệu lực',
                'ghi_chu': f'Import từ file: {filename}'
            }
            
            return doc_info
            
        except Exception as e:
            print(f"  ❌ Error parsing {filepath}: {e}")
            return None
    
    def _extract_title(self, content, filename):
        """Trích xuất tiêu đề văn bản"""
        lines = content.split('\n')
        
        # Tìm tiêu đề từ pattern "V/v" hoặc "Về"
        for i, line in enumerate(lines):
            line = line.strip()
            if re.search(r'^["""]?V/v\s+', line, re.IGNORECASE):
                title = line.strip('"\'')
                # Xóa "V/v" ở đầu
                title = re.sub(r'^V/v\s+', '', title, flags=re.IGNORECASE)
                return title
            
            # Nếu có pattern loại văn bản ở trên, lấy dòng tiếp theo
            if re.search(r'(CÔNG VĂN|QUYẾT ĐỊNH|NGHỊ QUYẾT|KẾ HOẠCH|THÔNG BÁO)', line, re.IGNORECASE):
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip().strip('"\'')
                    if next_line and len(next_line) > 5:
                        return next_line
        
        # Fallback: Sử dụng filename
        title = filename.replace('.txt', '')
        # Xóa số thứ tự ở đầu
        title = re.sub(r'^\d+[.\-\s]*', '', title)
        return title
    
    def _detect_doc_type(self, content, filename):
        """Nhận diện loại văn bản"""
        # Tìm trong content
        for doc_type, patterns in self.doc_type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return doc_type
        
        # Tìm trong filename
        for doc_type, patterns in self.doc_type_patterns.items():
            for pattern in patterns:
                pattern_simple = pattern.replace(r'\s*', ' ').replace(r'\d+', '').replace('[/-]?', '')
                if pattern_simple in filename.upper():
                    return doc_type
        
        return 'Văn bản hành chính'
    
    def _extract_so_hieu(self, content):
        """Trích xuất số hiệu văn bản"""
        # Pattern: Số: 123/CV-TWĐ
        patterns = [
            r'Số:\s*(\d+[/-]?[A-Z]{2,}[/-][A-Z\u00C0-\u1EF9\d]+)',
            r'Số:\s*(\d+[A-Z]{2}[/-][A-Z\u00C0-\u1EF9\d/]+)',
            r'số\s+(\d+[/-][A-Z]{2,}[/-][A-Z\u00C0-\u1EF9\d/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_date(self, content):
        """Trích xuất ngày ban hành"""
        # Pattern: Hà Nội, ngày 29 tháng 8 năm 2022
        patterns = [
            r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'ngày\s+(\d{1,2})-(\d{1,2})-(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    if 'tháng' in pattern:
                        day, month, year = match.groups()
                    else:
                        day, month, year = match.groups()
                    
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj.strftime('%Y-%m-%d')
                except:
                    continue
        
        return None
    
    def _extract_co_quan(self, content):
        """Trích xuất cơ quan ban hành"""
        lines = content.split('\n')[:10]  # Chỉ xem 10 dòng đầu
        
        for line in lines:
            for pattern in self.co_quan_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return line.strip()
        
        return None
    
    def _extract_nguoi_ky(self, content):
        """Trích xuất người ký"""
        # Tìm ở cuối văn bản
        lines = content.split('\n')
        
        # Tìm pattern "BÍ THƯ" hoặc "CHỦ TỊCH" etc.
        for i in range(len(lines) - 1, max(0, len(lines) - 20), -1):
            line = lines[i].strip()
            
            # Nếu tìm thấy chức vụ
            if re.search(r'(BÍ THƯ|CHỦ TỊCH|GIÁM ĐỐC|TRƯỞNG BAN|PHÓ)', line, re.IGNORECASE):
                # Lấy tên ở dòng tiếp theo
                if i + 1 < len(lines):
                    ten = lines[i + 1].strip()
                    if ten and len(ten) < 50 and not re.search(r'(Nơi nhận|TM\.|ĐOÀN)', ten):
                        return ten
        
        return None


def import_documents(folder_path, limit=None, dry_run=False):
    """
    Import tất cả file txt từ folder vào Supabase
    
    Args:
        folder_path: Đường dẫn folder chứa file txt
        limit: Giới hạn số file (để test), None = tất cả
        dry_run: Nếu True, chỉ parse không insert vào DB
    """
    parser = ManualDocumentParser()
    
    # Lấy danh sách file
    txt_files = list(Path(folder_path).glob('*.txt'))
    
    if limit:
        txt_files = txt_files[:limit]
    
    print(f"\n📂 Found {len(txt_files)} TXT files")
    print(f"{'🔍 DRY RUN MODE - No database changes' if dry_run else '💾 IMPORT MODE'}")
    print("=" * 70)
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    results = []
    
    for i, filepath in enumerate(txt_files, 1):
        print(f"\n[{i}/{len(txt_files)}] Processing: {filepath.name}")
        
        # Parse file
        doc_info = parser.parse_file(filepath)
        
        if not doc_info:
            error_count += 1
            continue
        
        # Display parsed info
        print(f"  📄 Tiêu đề: {doc_info['ten'][:60]}...")
        print(f"  📋 Loại: {doc_info['loai']}")
        print(f"  🔢 Số hiệu: {doc_info['so_hieu'] or 'N/A'}")
        print(f"  📅 Ngày: {doc_info['ngay_ban_hanh'] or 'N/A'}")
        print(f"  🏢 Cơ quan: {doc_info['co_quan_ban_hanh'][:50] if doc_info['co_quan_ban_hanh'] else 'N/A'}")
        print(f"  ✍️ Người ký: {doc_info['nguoi_ky'] or 'N/A'}")
        
        results.append(doc_info)
        
        # Insert vào DB nếu không phải dry run
        if not dry_run:
            try:
                data = {
                    'ten': doc_info['ten'],
                    'loai': doc_info['loai'],
                    'so_hieu': doc_info['so_hieu'],
                    'ngay_ban_hanh': doc_info['ngay_ban_hanh'],
                    'ngay_hieu_luc': doc_info['ngay_ban_hanh'],  # Mặc định = ngày ban hành
                    'trang_thai': doc_info['trang_thai'],
                    'co_quan_ban_hanh': doc_info['co_quan_ban_hanh'],
                    'nguoi_ky': doc_info['nguoi_ky'],
                    'noi_dung': doc_info['noi_dung'],
                    'ghi_chu': doc_info['ghi_chu']
                }
                
                result = supabase.table('documents').insert(data).execute()
                
                if result.data and len(result.data) > 0:
                    new_id = result.data[0]['id']
                    success_count += 1
                    print(f"  ✅ Inserted to DB with ID: {new_id}")
                else:
                    error_count += 1
                    print(f"  ❌ Failed to insert")
                    
            except Exception as e:
                error_count += 1
                print(f"  ❌ Error inserting: {e}")
        else:
            success_count += 1
            print(f"  ✅ Parsed successfully (dry run)")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 SUMMARY:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  📁 Total: {len(txt_files)}")
    
    if dry_run:
        print(f"\n💡 This was a DRY RUN. No data was inserted to database.")
        print(f"   Run again with dry_run=False to actually import.")
    
    return results


def test_connection():
    """Test Supabase connection"""
    print("🔌 Testing Supabase connection...")
    try:
        result = supabase.table('documents').select('id').limit(1).execute()
        print(f"✅ Connection successful! Found {len(result.data)} document(s)")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def main():
    """Main function"""
    print("=" * 70)
    print("📥 IMPORT MANUAL DOCUMENTS FROM TXT FILES")
    print("=" * 70)
    
    # Test connection
    if not test_connection():
        return
    
    # Đường dẫn folder
    folder_path = Path(__file__).parent.parent / "crawl thu cong"
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Chạy với limit=3 và dry_run=True để test trước
    print("\n" + "=" * 70)
    print("STEP 1: DRY RUN with 3 files (test parsing)")
    print("=" * 70)
    results = import_documents(folder_path, limit=3, dry_run=True)
    
    if results:
        # Hỏi người dùng có muốn import hết không
        print("\n" + "=" * 70)
        response = input("\n✨ Parsing looks good! Import ALL files to database? (y/N): ")
        
        if response.lower() == 'y':
            print("\n" + "=" * 70)
            print("STEP 2: IMPORTING ALL FILES")
            print("=" * 70)
            import_documents(folder_path, limit=None, dry_run=False)
        else:
            print("\n⏭️  Skipped full import. Run script again when ready.")
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
