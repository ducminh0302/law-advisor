/**
 * API Client for VN-Law-Mini
 *
 * Handles communication with Law Service and RAG Service
 */

import axios, { AxiosInstance } from 'axios';

// API Base URLs
const LAW_API_URL = process.env.NEXT_PUBLIC_LAW_API || 'http://localhost:5000';
const RAG_API_URL = process.env.NEXT_PUBLIC_RAG_API || 'http://localhost:5001';

// Create axios instances
const lawApi: AxiosInstance = axios.create({
    baseURL: LAW_API_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

const ragApi: AxiosInstance = axios.create({
    baseURL: RAG_API_URL,
    timeout: 60000, // RAG may take longer
    headers: {
        'Content-Type': 'application/json',
    },
});

// Types
export interface Document {
    id: number;
    ten: string;
    so_hieu: string;
    loai: string;
    ngay_ban_hanh: string;
    ngay_hieu_luc: string;
    trang_thai: string;
    co_quan_ban_hanh: string;
    nguoi_ky?: string;
    noi_dung?: string;
    articles_count?: number;
}

export interface Article {
    id: number;
    mapc: string;
    ten: string;
    noi_dung: string;
    chuong?: string;
    muc?: string;
    thu_tu: number;
    document?: Partial<Document>;
}

export interface Pagination {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
}

export interface DocumentsResponse {
    success: boolean;
    data: Document[];
    pagination: Pagination;
}

export interface DocumentDetailResponse {
    success: boolean;
    data: Document;
}

export interface ArticlesResponse {
    success: boolean;
    document: Partial<Document>;
    data: Article[];
}

export interface ArticleDetailResponse {
    success: boolean;
    data: Article;
}

export interface SearchResponse {
    success: boolean;
    keyword: string;
    total: number;
    results: {
        documents: Document[];
        articles: Article[];
    };
}

export interface SuggestionsResponse {
    success: boolean;
    data: {
        loai: string[];
        co_quan_ban_hanh: string[];
        trang_thai: string[];
    };
}

export interface Citation {
    mapc: string;
    ten: string;
    noi_dung: string;
    score: number;
}

export interface QuestionResponse {
    success: boolean;
    question: string;
    answer: string;
    citations: Citation[];
}

export interface ErrorResponse {
    success: false;
    error: string;
    message?: string;
}

// Law Service APIs
export const lawService = {
    /**
     * Get list of documents with pagination
     */
    getDocuments: async (params?: {
        page?: number;
        limit?: number;
        loai?: string;
        trang_thai?: string;
    }): Promise<DocumentsResponse> => {
        const response = await lawApi.get('/api/v1/documents', { params });
        return response.data;
    },

    /**
     * Get document detail by ID
     */
    getDocument: async (id: number): Promise<DocumentDetailResponse> => {
        const response = await lawApi.get(`/api/v1/documents/${id}`);
        return response.data;
    },

    /**
     * Get articles of a document
     */
    getDocumentArticles: async (id: number): Promise<ArticlesResponse> => {
        const response = await lawApi.get(`/api/v1/documents/${id}/articles`);
        return response.data;
    },

    /**
     * Get article by MAPC (mã pháp chế)
     */
    getArticle: async (mapc: string): Promise<ArticleDetailResponse> => {
        const response = await lawApi.get(`/api/v1/articles/${mapc}`);
        return response.data;
    },

    /**
     * Search documents and articles
     */
    search: async (params: {
        keyword: string;
        type?: 'documents' | 'articles' | 'both';
        limit?: number;
    }): Promise<SearchResponse> => {
        const response = await lawApi.post('/api/v1/search', params);
        return response.data;
    },

    /**
     * Get search suggestions (filter options)
     */
    getSuggestions: async (): Promise<SuggestionsResponse> => {
        const response = await lawApi.get('/api/v1/search/suggestions');
        return response.data;
    },
};

// RAG Service APIs
export const ragService = {
    /**
     * Ask a question about Vietnamese law
     */
    askQuestion: async (question: string): Promise<QuestionResponse> => {
        const response = await ragApi.post('/api/v1/question', { question });
        return response.data;
    },

    /**
     * Health check
     */
    healthCheck: async (): Promise<{ status: string }> => {
        const response = await ragApi.get('/health');
        return response.data;
    },
};

// Error handler
export const handleApiError = (error: any): ErrorResponse => {
    if (axios.isAxiosError(error)) {
        if (error.response) {
            // Server responded with error status
            return {
                success: false,
                error: error.response.data?.error || 'Server error',
                message: error.response.data?.message || error.message,
            };
        } else if (error.request) {
            // Request made but no response
            return {
                success: false,
                error: 'No response from server',
                message: 'Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng.',
            };
        }
    }

    // Unknown error
    return {
        success: false,
        error: 'Unknown error',
        message: error.message || 'Đã xảy ra lỗi không xác định',
    };
};

export default {
    lawService,
    ragService,
    handleApiError,
};
