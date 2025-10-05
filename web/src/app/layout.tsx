import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'VN Law Advisor - Tư vấn pháp luật Việt Nam',
    description: 'Hệ thống tra cứu và hỏi đáp pháp luật Việt Nam sử dụng AI',
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="vi">
            <body className={inter.className}>{children}</body>
        </html>
    );
}
