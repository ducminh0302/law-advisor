/**
 * Documents Routes
 *
 * API endpoints cho tra cứu văn bản pháp luật
 */

import express from 'express';
import { supabase } from '../db/supabase.js';

const router = express.Router();

/**
 * GET /api/v1/documents
 *
 * Lấy danh sách văn bản với pagination
 *
 * Query params:
 *   - page: số trang (default: 1)
 *   - limit: số văn bản per page (default: 20, max: 100)
 *   - loai: filter theo loại văn bản (optional)
 *   - trang_thai: filter theo trạng thái (optional)
 */
router.get('/', async (req, res) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const limit = Math.min(parseInt(req.query.limit) || 20, 100);
        const offset = (page - 1) * limit;

        const { loai, trang_thai } = req.query;

        // Build query
        let query = supabase
            .from('documents')
            .select(
                'id, ten, so_hieu, loai, ngay_ban_hanh, ngay_hieu_luc, trang_thai, co_quan_ban_hanh',
                { count: 'exact' },
            )
            .order('ngay_ban_hanh', { ascending: false })
            .range(offset, offset + limit - 1);

        // Apply filters
        if (loai) {
            query = query.eq('loai', loai);
        }
        if (trang_thai) {
            query = query.eq('trang_thai', trang_thai);
        }

        const { data, error, count } = await query;

        if (error) throw error;

        res.json({
            success: true,
            data,
            pagination: {
                page,
                limit,
                total: count,
                totalPages: Math.ceil(count / limit),
            },
        });
    } catch (error) {
        console.error('Error fetching documents:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch documents',
            message: error.message,
        });
    }
});

/**
 * GET /api/v1/documents/:id
 *
 * Lấy chi tiết 1 văn bản theo ID
 */
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;

        const { data, error } = await supabase.from('documents').select('*').eq('id', id).single();

        if (error) {
            if (error.code === 'PGRST116') {
                return res.status(404).json({
                    success: false,
                    error: 'Document not found',
                });
            }
            throw error;
        }

        // Get articles count
        const { count } = await supabase
            .from('articles')
            .select('id', { count: 'exact', head: true })
            .eq('document_id', id);

        res.json({
            success: true,
            data: {
                ...data,
                articles_count: count,
            },
        });
    } catch (error) {
        console.error('Error fetching document:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch document',
            message: error.message,
        });
    }
});

/**
 * GET /api/v1/documents/:id/articles
 *
 * Lấy tất cả điều luật của 1 văn bản
 */
router.get('/:id/articles', async (req, res) => {
    try {
        const { id } = req.params;

        // Check if document exists
        const { data: doc, error: docError } = await supabase
            .from('documents')
            .select('id, ten')
            .eq('id', id)
            .single();

        if (docError) {
            if (docError.code === 'PGRST116') {
                return res.status(404).json({
                    success: false,
                    error: 'Document not found',
                });
            }
            throw docError;
        }

        // Get articles
        const { data, error } = await supabase
            .from('articles')
            .select('id, mapc, ten, chuong, muc, thu_tu, noi_dung')
            .eq('document_id', id)
            .order('thu_tu', { ascending: true });

        if (error) throw error;

        res.json({
            success: true,
            document: doc,
            data,
        });
    } catch (error) {
        console.error('Error fetching articles:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch articles',
            message: error.message,
        });
    }
});

export default router;
