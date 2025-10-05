'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { ragService, handleApiError, Citation } from '@/lib/api';

interface Message {
    id: string;
    type: 'user' | 'assistant';
    content: string;
    citations?: Citation[];
    timestamp: Date;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new message
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Handle send question
    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!input.trim() || loading) return;

        const question = input.trim();
        setInput('');

        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            type: 'user',
            content: question,
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);

        // Call RAG API
        setLoading(true);

        try {
            const response = await ragService.askQuestion(question);

            // Add assistant message
            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                type: 'assistant',
                content: response.answer,
                citations: response.citations,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (err) {
            const errorResponse = handleApiError(err);

            // Add error message
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                type: 'assistant',
                content: `Xin lỗi, đã xảy ra lỗi: ${
                    errorResponse.message || errorResponse.error
                }. Vui lòng thử lại sau.`,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    // Clear chat
    const handleClear = () => {
        if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử chat?')) {
            setMessages([]);
        }
    };

    // Example questions
    const exampleQuestions = [
        'Phạm vi điều chỉnh của Bộ luật Dân sự là gì?',
        'Điều kiện kết hôn theo pháp luật Việt Nam?',
        'Quy định về hợp đồng mua bán?',
        'Thủ tục ly hôn như thế nào?',
    ];

    const handleExampleClick = (question: string) => {
        setInput(question);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Header */}
            <header className="bg-white border-b shadow-sm">
                <div className="max-w-5xl mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <Link
                            href="/"
                            className="text-xl font-bold text-green-600 hover:text-green-700"
                        >
                            ← VN Law Advisor
                        </Link>
                        <div className="flex items-center gap-4">
                            <Link
                                href="/search"
                                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                Chuyển sang Tra cứu
                            </Link>
                            {messages.length > 0 && (
                                <button
                                    onClick={handleClear}
                                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                >
                                    Xóa chat
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            {/* Chat Container */}
            <div className="flex-1 max-w-5xl w-full mx-auto px-4 py-6 flex flex-col">
                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto mb-6 space-y-6">
                    {messages.length === 0 ? (
                        // Welcome Screen
                        <div className="text-center py-12">
                            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <svg
                                    className="w-10 h-10 text-green-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                                    />
                                </svg>
                            </div>
                            <h2 className="text-3xl font-bold text-gray-900 mb-3">
                                Hỏi đáp pháp luật với AI
                            </h2>
                            <p className="text-gray-600 mb-8">
                                Đặt câu hỏi bằng tiếng Việt tự nhiên, AI sẽ phân tích và trả lời
                            </p>

                            {/* Example Questions */}
                            <div className="max-w-2xl mx-auto">
                                <p className="text-sm text-gray-500 mb-4">Ví dụ các câu hỏi:</p>
                                <div className="grid md:grid-cols-2 gap-3">
                                    {exampleQuestions.map((question, index) => (
                                        <button
                                            key={index}
                                            onClick={() => handleExampleClick(question)}
                                            className="p-4 bg-white border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-md transition-all text-left text-sm text-gray-700"
                                        >
                                            {question}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        // Messages
                        messages.map((message) => (
                            <div
                                key={message.id}
                                className={`flex ${
                                    message.type === 'user' ? 'justify-end' : 'justify-start'
                                }`}
                            >
                                <div
                                    className={`max-w-3xl ${
                                        message.type === 'user'
                                            ? 'bg-green-600 text-white rounded-2xl rounded-tr-sm'
                                            : 'bg-white border border-gray-200 rounded-2xl rounded-tl-sm'
                                    } p-5 shadow-sm`}
                                >
                                    {/* Message Content */}
                                    <div
                                        className={`${
                                            message.type === 'assistant' ? 'text-gray-800' : ''
                                        } whitespace-pre-line`}
                                    >
                                        {message.content}
                                    </div>

                                    {/* Citations */}
                                    {message.citations && message.citations.length > 0 && (
                                        <div className="mt-4 pt-4 border-t border-gray-200">
                                            <p className="text-sm font-semibold text-gray-700 mb-3">
                                                Nguồn tham khảo ({message.citations.length}):
                                            </p>
                                            <div className="space-y-3">
                                                {message.citations.map((citation, index) => (
                                                    <div
                                                        key={index}
                                                        className="p-3 bg-gray-50 rounded-lg border border-gray-200"
                                                    >
                                                        <div className="flex items-start justify-between mb-2">
                                                            <p className="font-semibold text-sm text-gray-900">
                                                                {citation.ten}
                                                            </p>
                                                            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                                                                {(citation.score * 100).toFixed(0)}%
                                                            </span>
                                                        </div>
                                                        <p className="text-xs text-gray-600 line-clamp-2 mb-2">
                                                            {citation.noi_dung}
                                                        </p>
                                                        <p className="text-xs text-gray-500">
                                                            Mã: {citation.mapc}
                                                        </p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Timestamp */}
                                    <div
                                        className={`text-xs mt-2 ${
                                            message.type === 'user'
                                                ? 'text-green-100'
                                                : 'text-gray-400'
                                        }`}
                                    >
                                        {message.timestamp.toLocaleTimeString('vi-VN', {
                                            hour: '2-digit',
                                            minute: '2-digit',
                                        })}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}

                    {/* Loading Indicator */}
                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-5 shadow-sm">
                                <div className="flex items-center space-x-2">
                                    <div
                                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                                        style={{ animationDelay: '0ms' }}
                                    ></div>
                                    <div
                                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                                        style={{ animationDelay: '150ms' }}
                                    ></div>
                                    <div
                                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                                        style={{ animationDelay: '300ms' }}
                                    ></div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="bg-white border border-gray-200 rounded-xl shadow-lg p-4">
                    <form onSubmit={handleSend} className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Nhập câu hỏi của bạn về pháp luật..."
                            disabled={loading}
                            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-semibold flex items-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                        <circle
                                            className="opacity-25"
                                            cx="12"
                                            cy="12"
                                            r="10"
                                            stroke="currentColor"
                                            strokeWidth="4"
                                            fill="none"
                                        ></circle>
                                        <path
                                            className="opacity-75"
                                            fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                        ></path>
                                    </svg>
                                    Đang xử lý...
                                </>
                            ) : (
                                <>
                                    Gửi
                                    <svg
                                        className="w-5 h-5"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                                        />
                                    </svg>
                                </>
                            )}
                        </button>
                    </form>

                    <p className="text-xs text-gray-500 mt-3 text-center">
                        AI có thể mắc lỗi. Vui lòng kiểm tra thông tin quan trọng với chuyên gia
                        pháp lý.
                    </p>
                </div>
            </div>
        </div>
    );
}
