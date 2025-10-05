/**
 * Search Routes
 *
 * API endpoints cho tìm kiếm văn bản và điều luật
 */

import express from 'express';
import { supabase } from '../db/supabase.js';

const router = express.Router();

/**
 * POST /api/v1/search
 *
 * Tìm kiếm văn bản và điều luật theo keyword
 *
 * Body:
 *   - keyword: từ khóa tìm kiếm (required)
 *   - type: 'documents' | 'articles' | 'both' (default: 'both')
 *   - limit: số kết quả (default: 20, max: 50)
 */
router.post('/', async (req, res) => {
    try {
        const { keyword, type = 'both', limit = 20 } = req.body;

        if (!keyword || keyword.trim() === '') {
            return res.status(400).json({
                success: false,
                error: 'Keyword is required',
            });
        }

        const searchLimit = Math.min(parseInt(limit), 50);
        const results = {};

        // Search documents
        if (type === 'documents' || type === 'both') {
            const { data: docs, error: docsError } = await supabase
                .from('documents')
                .select('id, ten, so_hieu, loai, ngay_ban_hanh, trang_thai')
                .or(`ten.ilike.%${keyword}%,so_hieu.ilike.%${keyword}%,noi_dung.ilike.%${keyword}%`)
                .limit(searchLimit);

            if (docsError) throw docsError;

            results.documents = docs;
        }

        // Search articles
        if (type === 'articles' || type === 'both') {
            const { data: articles, error: articlesError } = await supabase
                .from('articles')
                .select(
                    `
          id,
          mapc,
          ten,
          noi_dung,
          chuong,
          document:documents(id, ten, so_hieu)
        `,
                )
                .or(`ten.ilike.%${keyword}%,noi_dung.ilike.%${keyword}%`)
                .limit(searchLimit);

            if (articlesError) throw articlesError;

            results.articles = articles;
        }

        // Calculate total
        const total = (results.documents?.length || 0) + (results.articles?.length || 0);

        res.json({
            success: true,
            keyword,
            total,
            results,
        });
    } catch (error) {
        console.error('Error searching:', error);
        res.status(500).json({
            success: false,
            error: 'Search failed',
            message: error.message,
        });
    }
});

/**
 * GET /api/v1/search/suggestions
 *
 * Lấy gợi ý loại văn bản, cơ quan ban hành để filter
 */
router.get('/suggestions', async (req, res) => {
    try {
        // Get unique loai
        const { data: loaiData, error: loaiError } = await supabase
            .from('documents')
            .select('loai')
            .not('loai', 'is', null);

        if (loaiError) throw loaiError;

        const loai = [...new Set(loaiData.map((d) => d.loai))].filter(Boolean);

        // Get unique co_quan_ban_hanh
        const { data: coquanData, error: coquanError } = await supabase
            .from('documents')
            .select('co_quan_ban_hanh')
            .not('co_quan_ban_hanh', 'is', null);

        if (coquanError) throw coquanError;

        const co_quan = [...new Set(coquanData.map((d) => d.co_quan_ban_hanh))].filter(Boolean);

        res.json({
            success: true,
            data: {
                loai,
                co_quan_ban_hanh: co_quan,
                trang_thai: ['Còn hiệu lực', 'Hết hiệu lực'],
            },
        });
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch suggestions',
            message: error.message,
        });
    }
});

export default router;
