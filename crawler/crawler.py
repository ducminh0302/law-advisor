"""
VN-Law-Mini Crawler
Crawl văn bản pháp luật từ vbpl.vn

Copyright (C) 2024 - Based on VN-Law-Advisor
Licensed under GNU GPL v3.0
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime
import re

class LawCrawler:
    """
    Simple crawler để crawl văn bản pháp luật từ vbpl.vn
    """

    def __init__(self, output_dir="./data"):
        self.base_url = "https://vbpl.vn"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.output_dir = output_dir

        # Tạo thư mục output nếu chưa có
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/documents", exist_ok=True)
        os.makedirs(f"{output_dir}/articles", exist_ok=True)

    def crawl_document_list(self, page=1, limit=20, loai="", keyword=""):
        """
        Crawl danh sách văn bản từ trang tìm kiếm

        Args:
            page: Trang số (default 1)
            limit: Số văn bản per page (default 20)
            loai: Loại văn bản (Luật, Nghị định, Thông tư...)
            keyword: Từ khóa tìm kiếm

        Returns:
            List of document IDs
        """
        print(f"Crawling page {page}...")

        # URL search với pagination
        search_url = f"{self.base_url}/pages/tim-kiem.aspx"
        params = {
            'Keyword': keyword,
            'LoaiVB': loai,
            'Page': page
        }

        try:
            response = self.session.get(search_url, params=params, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm các link văn bản
            doc_links = soup.select('a[href*="ItemID="]')
            doc_ids = []

            for link in doc_links[:limit]:
                href = link.get('href', '')
                match = re.search(r'ItemID=(\d+)', href)
                if match:
                    doc_id = match.group(1)
                    if doc_id not in doc_ids:
                        doc_ids.append(doc_id)

            print(f"Found {len(doc_ids)} documents")
            return doc_ids

        except Exception as e:
            print(f"Error crawling page {page}: {e}")
            return []

    def crawl_document_detail(self, doc_id):
        """
        Crawl chi tiết 1 văn bản

        Args:
            doc_id: ID của văn bản

        Returns:
            Dict chứa thông tin văn bản
        """
        print(f"  Crawling document ID: {doc_id}")

        url = f"{self.base_url}/TW/Pages/vbpq-toanvan.aspx?ItemID={doc_id}"

        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse metadata
            document = {
                'id': doc_id,
                'ten': '',
                'so_hieu': '',
                'loai': '',
                'ngay_ban_hanh': None,
                'ngay_hieu_luc': None,
                'trang_thai': 'Còn hiệu lực',
                'co_quan_ban_hanh': '',
                'nguoi_ky': '',
                'noi_dung': '',
                'crawled_at': datetime.now().isoformat()
            }

            # Lấy tiêu đề
            title_elem = soup.find('h1', class_='title')
            if title_elem:
                document['ten'] = title_elem.text.strip()

            # Lấy thông tin từ các div.row
            info_rows = soup.select('div.row div.col-md-6, div.row div.col-md-12')
            for row in info_rows:
                label = row.find('label')
                if not label:
                    continue

                label_text = label.text.strip().lower()
                value_elem = row.find('span') or row.find('p')
                value = value_elem.text.strip() if value_elem else ''

                if 'số hiệu' in label_text:
                    document['so_hieu'] = value
                elif 'loại văn bản' in label_text:
                    document['loai'] = value
                elif 'ngày ban hành' in label_text:
                    document['ngay_ban_hanh'] = self._parse_date(value)
                elif 'ngày hiệu lực' in label_text:
                    document['ngay_hieu_luc'] = self._parse_date(value)
                elif 'tình trạng' in label_text or 'trạng thái' in label_text:
                    document['trang_thai'] = value
                elif 'cơ quan ban hành' in label_text:
                    document['co_quan_ban_hanh'] = value
                elif 'người ký' in label_text:
                    document['nguoi_ky'] = value

            # Lấy nội dung toàn văn
            fulltext_div = soup.find('div', class_='fulltext')
            if fulltext_div:
                content_div = fulltext_div.find('div', recursive=False)
                if content_div:
                    document['noi_dung'] = content_div.get_text(separator='\n', strip=True)

            return document

        except Exception as e:
            print(f"  Error crawling document {doc_id}: {e}")
            return None

    def parse_articles(self, document):
        """
        Parse các điều luật từ nội dung văn bản

        Args:
            document: Dict văn bản đã crawl

        Returns:
            List of articles
        """
        articles = []
        content = document.get('noi_dung', '')

        if not content:
            return articles

        # Regex tìm các "Điều X."
        pattern = r'(Điều\s+\d+[a-z]?\.?)\s+(.*?)(?=\nĐiều\s+\d+|$)'
        matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)

        thu_tu = 0
        for match in matches:
            dieu_header = match.group(1).strip()
            dieu_content = match.group(2).strip()

            # Tách tên điều (phần sau "Điều X.")
            ten_match = re.match(r'(.*?)(?:\n|$)', dieu_content)
            ten = ten_match.group(1).strip() if ten_match else ''

            # Nội dung còn lại
            noidung = dieu_content[len(ten):].strip() if ten else dieu_content

            # Tạo mã pháp chế
            mapc = f"{document['so_hieu']}-{dieu_header.replace(' ', '-')}"

            article = {
                'mapc': mapc,
                'document_id': document['id'],
                'ten': f"{dieu_header} {ten}",
                'noi_dung': noidung,
                'chuong': '',  # TODO: parse chapter nếu cần
                'muc': '',     # TODO: parse section nếu cần
                'thu_tu': thu_tu
            }

            articles.append(article)
            thu_tu += 1

        return articles

    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved to {filepath}")

    def crawl_batch(self, doc_ids):
        """
        Crawl một batch văn bản

        Args:
            doc_ids: List of document IDs

        Returns:
            Tuple (documents, articles)
        """
        documents = []
        all_articles = []

        for i, doc_id in enumerate(doc_ids, 1):
            print(f"\n[{i}/{len(doc_ids)}] Processing document {doc_id}...")

            # Crawl document
            document = self.crawl_document_detail(doc_id)
            if not document:
                continue

            documents.append(document)

            # Parse articles
            articles = self.parse_articles(document)
            all_articles.extend(articles)

            print(f"  Extracted {len(articles)} articles")

            # Delay để tránh bị block
            time.sleep(1)

        return documents, all_articles

    def _parse_date(self, date_str):
        """Parse date string to ISO format"""
        if not date_str:
            return None

        # Try common formats
        formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except:
                continue

        return None


def main():
    """
    Main function để test crawler
    """
    print("VN-Law-Mini Crawler")
    print("=" * 50)

    crawler = LawCrawler(output_dir="./data")

    # Test: Crawl 5 văn bản đầu tiên
    print("\nStep 1: Get document list...")
    doc_ids = crawler.crawl_document_list(page=1, limit=5, keyword="")

    if not doc_ids:
        print("No documents found!")
        return

    print(f"\nStep 2: Crawl {len(doc_ids)} documents...")
    documents, articles = crawler.crawl_batch(doc_ids)

    print(f"\nStep 3: Save to JSON...")
    crawler.save_to_json(documents, 'documents.json')
    crawler.save_to_json(articles, 'articles.json')

    print(f"\nDONE!")
    print(f"  - Documents: {len(documents)}")
    print(f"  - Articles: {len(articles)}")
    print(f"  - Output: {crawler.output_dir}/")


if __name__ == "__main__":
    main()
