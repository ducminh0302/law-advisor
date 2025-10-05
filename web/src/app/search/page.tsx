'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { lawService, handleApiError, Document, Article } from '@/lib/api';

export default function SearchPage() {
    const [keyword, setKeyword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Search results
    const [documents, setDocuments] = useState<Document[]>([]);
    const [articles, setArticles] = useState<Article[]>([]);
    const [totalResults, setTotalResults] = useState(0);

    // Selected document for viewing articles
    const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
    const [documentArticles, setDocumentArticles] = useState<Article[]>([]);
    const [loadingArticles, setLoadingArticles] = useState(false);

    // Filters
    const [searchType, setSearchType] = useState<'both' | 'documents' | 'articles'>('both');

    // Handle search
    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!keyword.trim()) {
            setError('Vui lòng nhập từ khóa tìm kiếm');
            return;
        }

        setLoading(true);
        setError('');
        setDocuments([]);
        setArticles([]);
        setSelectedDocument(null);

        try {
            const response = await lawService.search({
                keyword: keyword.trim(),
                type: searchType,
                limit: 20,
            });

            setDocuments(response.results.documents || []);
            setArticles(response.results.articles || []);
            setTotalResults(response.total);
        } catch (err) {
            const errorResponse = handleApiError(err);
            setError(errorResponse.message || errorResponse.error);
        } finally {
            setLoading(false);
        }
    };

    // View document articles
    const viewDocumentArticles = async (doc: Document) => {
        setSelectedDocument(doc);
        setLoadingArticles(true);

        try {
            const response = await lawService.getDocumentArticles(doc.id);
            setDocumentArticles(response.data);
        } catch (err) {
            const errorResponse = handleApiError(err);
            setError(errorResponse.message || errorResponse.error);
        } finally {
            setLoadingArticles(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b shadow-sm sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <Link
                            href="/"
                            className="text-xl font-bold text-blue-600 hover:text-blue-700"
                        >
                            ← VN Law Advisor
                        </Link>
                        <Link
                            href="/chat"
                            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                        >
                            Chuyển sang Q&A
                        </Link>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Search Section */}
                <div className="bg-white rounded-xl shadow-md p-6 mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-6">Tra cứu Pháp điển</h1>

                    <form onSubmit={handleSearch} className="space-y-4">
                        {/* Search Input */}
                        <div className="flex gap-3">
                            <input
                                type="text"
                                value={keyword}
                                onChange={(e) => setKeyword(e.target.value)}
                                placeholder="Nhập từ khóa tìm kiếm (vd: dân sự, hợp đồng, thuế...)"
                                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-semibold"
                            >
                                {loading ? 'Đang tìm...' : 'Tìm kiếm'}
                            </button>
                        </div>

                        {/* Filter Tabs */}
                        <div className="flex gap-2">
                            <button
                                type="button"
                                onClick={() => setSearchType('both')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                                    searchType === 'both'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                            >
                                Tất cả
                            </button>
                            <button
                                type="button"
                                onClick={() => setSearchType('documents')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                                    searchType === 'documents'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                            >
                                Văn bản
                            </button>
                            <button
                                type="button"
                                onClick={() => setSearchType('articles')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                                    searchType === 'articles'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                            >
                                Điều khoản
                            </button>
                        </div>
                    </form>

                    {/* Error Message */}
                    {error && (
                        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                            {error}
                        </div>
                    )}
                </div>

                {/* Results Section */}
                {totalResults > 0 && (
                    <div className="mb-6">
                        <h2 className="text-lg font-semibold text-gray-700">
                            Tìm thấy <span className="text-blue-600">{totalResults}</span> kết quả
                        </h2>
                    </div>
                )}

                <div className="grid lg:grid-cols-2 gap-8">
                    {/* Left: Search Results */}
                    <div className="space-y-6">
                        {/* Documents */}
                        {documents.length > 0 && (
                            <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4">
                                    Văn bản ({documents.length})
                                </h3>
                                <div className="space-y-3">
                                    {documents.map((doc) => (
                                        <div
                                            key={doc.id}
                                            className="bg-white p-5 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                                            onClick={() => viewDocumentArticles(doc)}
                                        >
                                            <div className="flex items-start justify-between">
                                                <div className="flex-1">
                                                    <h4 className="font-semibold text-gray-900 mb-2">
                                                        {doc.ten}
                                                    </h4>
                                                    <div className="space-y-1 text-sm text-gray-600">
                                                        <p>
                                                            Số hiệu:{' '}
                                                            <span className="font-medium">
                                                                {doc.so_hieu}
                                                            </span>
                                                        </p>
                                                        <p>
                                                            Loại:{' '}
                                                            <span className="font-medium">
                                                                {doc.loai}
                                                            </span>
                                                        </p>
                                                        <p>
                                                            Trạng thái:{' '}
                                                            <span className="font-medium text-green-600">
                                                                {doc.trang_thai}
                                                            </span>
                                                        </p>
                                                    </div>
                                                </div>
                                                <button className="text-blue-600 hover:text-blue-700 ml-4">
                                                    <svg
                                                        className="w-6 h-6"
                                                        fill="none"
                                                        stroke="currentColor"
                                                        viewBox="0 0 24 24"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth={2}
                                                            d="M9 5l7 7-7 7"
                                                        />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Articles */}
                        {articles.length > 0 && (
                            <div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4">
                                    Điều khoản ({articles.length})
                                </h3>
                                <div className="space-y-3">
                                    {articles.map((article) => (
                                        <div
                                            key={article.id}
                                            className="bg-white p-5 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all"
                                        >
                                            <h4 className="font-semibold text-gray-900 mb-2">
                                                {article.ten}
                                            </h4>
                                            <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                                                {article.noi_dung}
                                            </p>
                                            <div className="flex items-center justify-between text-sm">
                                                <span className="text-gray-500">
                                                    Mã: {article.mapc}
                                                </span>
                                                {article.document && (
                                                    <span className="text-blue-600 font-medium">
                                                        {article.document.ten}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* No Results */}
                        {!loading && totalResults === 0 && keyword && (
                            <div className="bg-white p-12 rounded-lg text-center">
                                <svg
                                    className="w-16 h-16 text-gray-300 mx-auto mb-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                                    Không tìm thấy kết quả
                                </h3>
                                <p className="text-gray-500">
                                    Thử tìm với từ khóa khác hoặc chuyển sang Q&A để hỏi AI
                                </p>
                            </div>
                        )}
                    </div>

                    {/* Right: Document Detail */}
                    <div className="lg:sticky lg:top-24 lg:h-fit">
                        {selectedDocument ? (
                            <div className="bg-white rounded-lg border border-gray-200 shadow-md">
                                {/* Document Header */}
                                <div className="p-6 border-b bg-blue-50">
                                    <div className="flex items-start justify-between mb-4">
                                        <h3 className="text-xl font-bold text-gray-900 flex-1">
                                            {selectedDocument.ten}
                                        </h3>
                                        <button
                                            onClick={() => setSelectedDocument(null)}
                                            className="text-gray-400 hover:text-gray-600"
                                        >
                                            <svg
                                                className="w-6 h-6"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    strokeWidth={2}
                                                    d="M6 18L18 6M6 6l12 12"
                                                />
                                            </svg>
                                        </button>
                                    </div>
                                    <div className="space-y-2 text-sm text-gray-700">
                                        <p>
                                            <span className="font-semibold">Số hiệu:</span>{' '}
                                            {selectedDocument.so_hieu}
                                        </p>
                                        <p>
                                            <span className="font-semibold">Loại:</span>{' '}
                                            {selectedDocument.loai}
                                        </p>
                                        <p>
                                            <span className="font-semibold">Cơ quan:</span>{' '}
                                            {selectedDocument.co_quan_ban_hanh}
                                        </p>
                                        <p>
                                            <span className="font-semibold">Trạng thái:</span>{' '}
                                            <span className="text-green-600">
                                                {selectedDocument.trang_thai}
                                            </span>
                                        </p>
                                    </div>
                                </div>

                                {/* Articles List */}
                                <div className="p-6 max-h-[600px] overflow-y-auto">
                                    <h4 className="font-semibold text-gray-900 mb-4">
                                        Nội dung các điều
                                    </h4>

                                    {loadingArticles ? (
                                        <div className="text-center py-8">
                                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                                            <p className="text-gray-500 mt-4">Đang tải...</p>
                                        </div>
                                    ) : (
                                        <div className="space-y-4">
                                            {documentArticles.map((article) => (
                                                <div
                                                    key={article.id}
                                                    className="pb-4 border-b border-gray-100 last:border-0"
                                                >
                                                    <h5 className="font-semibold text-gray-900 mb-2">
                                                        {article.ten}
                                                    </h5>
                                                    <p className="text-sm text-gray-700 whitespace-pre-line">
                                                        {article.noi_dung}
                                                    </p>
                                                    {article.chuong && (
                                                        <p className="text-xs text-gray-500 mt-2">
                                                            {article.chuong}
                                                        </p>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ) : (
                            <div className="bg-white p-12 rounded-lg border border-gray-200 text-center">
                                <svg
                                    className="w-16 h-16 text-gray-300 mx-auto mb-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                    />
                                </svg>
                                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                                    Chưa chọn văn bản
                                </h3>
                                <p className="text-gray-500">
                                    Nhấp vào văn bản bên trái để xem chi tiết
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
