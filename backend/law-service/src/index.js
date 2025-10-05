/**
 * VN-Law-Mini - Law Service
 *
 * API service for Vietnamese legal documents lookup
 */

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { testConnection } from './db/supabase.js';
import documentsRouter from './routes/documents.js';
import articlesRouter from './routes/articles.js';
import searchRouter from './routes/search.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Health check
app.get('/', (req, res) => {
    res.json({
        service: 'VN-Law-Mini Law Service',
        version: '1.0.0',
        status: 'running',
        endpoints: {
            documents: '/api/v1/documents',
            articles: '/api/v1/articles',
            search: '/api/v1/search',
        },
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API Routes
app.use('/api/v1/documents', documentsRouter);
app.use('/api/v1/articles', articlesRouter);
app.use('/api/v1/search', searchRouter);

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Route not found',
        path: req.path,
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: err.message,
    });
});

// Start server
async function startServer() {
    try {
        // Test database connection (optional - skip if DB not ready)
        console.log('Testing Supabase connection...');
        const connected = await testConnection();

        if (!connected) {
            console.warn('⚠️  Supabase connection failed. Service will run but APIs may not work.');
            console.warn(
                '⚠️  Make sure to setup Supabase database first (see docs/01-SETUP-SUPABASE.md)',
            );
            // Don't exit - allow service to start anyway
        }

        // Start listening
        app.listen(PORT, () => {
            console.log('');
            console.log('='.repeat(50));
            console.log('🚀 VN-Law-Mini Law Service');
            console.log('='.repeat(50));
            console.log(`Server running on http://localhost:${PORT}`);
            console.log(`Health check: http://localhost:${PORT}/health`);
            console.log(`API docs: http://localhost:${PORT}/`);
            console.log('');
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
}

startServer();
