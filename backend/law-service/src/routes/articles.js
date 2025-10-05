/**
 * Articles Routes
 *
 * API endpoints cho tra cứu điều luật
 */

import express from 'express';
import { supabase } from '../db/supabase.js';

const router = express.Router();

/**
 * GET /api/v1/articles/:mapc
 *
 * Lấy chi tiết điều luật theo mã pháp chế
 */
router.get('/:mapc', async (req, res) => {
    try {
        const { mapc } = req.params;

        const { data, error } = await supabase
            .from('articles')
            .select(
                `
        *,
        document:documents(id, ten, so_hieu, loai)
      `,
            )
            .eq('mapc', mapc)
            .single();

        if (error) {
            if (error.code === 'PGRST116') {
                return res.status(404).json({
                    success: false,
                    error: 'Article not found',
                });
            }
            throw error;
        }

        res.json({
            success: true,
            data,
        });
    } catch (error) {
        console.error('Error fetching article:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch article',
            message: error.message,
        });
    }
});

export default router;
