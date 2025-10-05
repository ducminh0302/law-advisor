import Link from 'next/link';

export default function Home() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
            {/* Header */}
            <header className="py-6 px-4 border-b bg-white/80 backdrop-blur">
                <div className="max-w-6xl mx-auto">
                    <h1 className="text-2xl font-bold text-blue-600">VN Law Advisor</h1>
                    <p className="text-sm text-gray-600 mt-1">Tư vấn pháp luật Việt Nam với AI</p>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-6xl mx-auto px-4 py-16">
                {/* Hero Section */}
                <div className="text-center mb-16">
                    <h2 className="text-5xl font-bold text-gray-900 mb-4">
                        Tra cứu & Hỏi đáp
                        <br />
                        <span className="text-blue-600">Pháp luật Việt Nam</span>
                    </h2>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Hệ thống AI giúp bạn tra cứu văn bản pháp luật và giải đáp thắc mắc pháp lý
                        một cách nhanh chóng, chính xác
                    </p>
                </div>

                {/* Action Cards */}
                <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                    {/* Search Card */}
                    <Link
                        href="/search"
                        className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100"
                    >
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-blue-600/5 group-hover:from-blue-500/10 group-hover:to-blue-600/10 transition-colors" />

                        <div className="relative p-8">
                            {/* Icon */}
                            <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <svg
                                    className="w-8 h-8 text-blue-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </div>

                            {/* Content */}
                            <h3 className="text-2xl font-bold text-gray-900 mb-3">
                                Tra cứu Pháp điển
                            </h3>
                            <p className="text-gray-600 mb-6">
                                Tìm kiếm và tra cứu văn bản pháp luật, điều khoản theo từ khóa, loại
                                văn bản, cơ quan ban hành
                            </p>

                            {/* Features */}
                            <ul className="space-y-2 mb-6">
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-blue-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    Tìm kiếm nhanh chóng
                                </li>
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-blue-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    Xem chi tiết điều khoản
                                </li>
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-blue-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    Lọc theo loại & trạng thái
                                </li>
                            </ul>

                            {/* CTA */}
                            <div className="flex items-center text-blue-600 font-semibold group-hover:translate-x-2 transition-transform">
                                Bắt đầu tra cứu
                                <svg
                                    className="w-5 h-5 ml-2"
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
                            </div>
                        </div>
                    </Link>

                    {/* Chat Card */}
                    <Link
                        href="/chat"
                        className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100"
                    >
                        <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-600/5 group-hover:from-green-500/10 group-hover:to-emerald-600/10 transition-colors" />

                        <div className="relative p-8">
                            {/* Icon */}
                            <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <svg
                                    className="w-8 h-8 text-green-600"
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

                            {/* Content */}
                            <h3 className="text-2xl font-bold text-gray-900 mb-3">Hỏi đáp Q&A</h3>
                            <p className="text-gray-600 mb-6">
                                Đặt câu hỏi bằng ngôn ngữ tự nhiên, AI sẽ phân tích và trả lời dựa
                                trên văn bản pháp luật
                            </p>

                            {/* Features */}
                            <ul className="space-y-2 mb-6">
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-green-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    Hỏi bằng tiếng Việt tự nhiên
                                </li>
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-green-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    AI phân tích & giải đáp
                                </li>
                                <li className="flex items-center text-sm text-gray-600">
                                    <svg
                                        className="w-5 h-5 text-green-500 mr-2"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    Trích dẫn nguồn chính xác
                                </li>
                            </ul>

                            {/* CTA */}
                            <div className="flex items-center text-green-600 font-semibold group-hover:translate-x-2 transition-transform">
                                Bắt đầu hỏi đáp
                                <svg
                                    className="w-5 h-5 ml-2"
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
                            </div>
                        </div>
                    </Link>
                </div>

                {/* Features Section */}
                <div className="mt-24 text-center">
                    <h3 className="text-2xl font-bold text-gray-900 mb-12">
                        Tại sao chọn VN Law Advisor?
                    </h3>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <svg
                                    className="w-6 h-6 text-blue-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M13 10V3L4 14h7v7l9-11h-7z"
                                    />
                                </svg>
                            </div>
                            <h4 className="font-semibold text-gray-900 mb-2">Nhanh chóng</h4>
                            <p className="text-sm text-gray-600">
                                Tìm kiếm và nhận câu trả lời trong vài giây
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <svg
                                    className="w-6 h-6 text-green-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                            </div>
                            <h4 className="font-semibold text-gray-900 mb-2">Chính xác</h4>
                            <p className="text-sm text-gray-600">
                                Dữ liệu từ nguồn chính thống, trích dẫn rõ ràng
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <svg
                                    className="w-6 h-6 text-purple-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                                    />
                                </svg>
                            </div>
                            <h4 className="font-semibold text-gray-900 mb-2">Dễ sử dụng</h4>
                            <p className="text-sm text-gray-600">
                                Giao diện đơn giản, thân thiện với người dùng
                            </p>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="border-t bg-gray-50 py-8 mt-24">
                <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-600">
                    <p>VN Law Advisor - Hệ thống tư vấn pháp luật Việt Nam</p>
                    <p className="mt-2">Powered by AI • Made with ❤️ for Vietnamese Law Tech</p>
                </div>
            </footer>
        </div>
    );
}
