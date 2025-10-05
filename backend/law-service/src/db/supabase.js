/**
 * Supabase Client Configuration
 *
 * Kết nối đến Supabase PostgreSQL database
 */

import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment variables');
    process.exit(1);
}

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseKey);

// Test connection
export async function testConnection() {
    try {
        const { data, error } = await supabase.from('documents').select('id').limit(1);

        if (error) throw error;

        console.log('✓ Supabase connection successful');
        return true;
    } catch (error) {
        console.error('✗ Supabase connection failed:', error.message);
        return false;
    }
}
