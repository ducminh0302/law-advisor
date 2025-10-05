# VN-Law-Mini - Frontend Web

Frontend web application cho hệ thống tư vấn pháp luật Việt Nam - VN-Law-Mini

---

## Features

### 🏠 Home Page

-   Landing page với 2 chức năng chính
-   Navigation đến Search và Chat
-   Giới thiệu tính năng

### 🔍 Search Page

-   Tìm kiếm văn bản pháp luật và điều khoản
-   Filter theo loại (văn bản/điều khoản/tất cả)
-   Xem chi tiết văn bản
-   Xem danh sách các điều trong văn bản
-   Responsive design

### 💬 Chat Page

-   Hỏi đáp với AI về pháp luật
-   Chat interface với history
-   Hiển thị citations (nguồn tham khảo)
-   Relevance score cho mỗi citation
-   Example questions
-   Clear chat history

---

## Tech Stack

-   **Next.js 14** - React framework với App Router
-   **TypeScript** - Type safety
-   **Tailwind CSS** - Styling
-   **Axios** - HTTP client
-   **React Hooks** - State management

---

## Setup Local

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Cập nhật API endpoints:

```env
# Local development
NEXT_PUBLIC_LAW_API=http://localhost:5000
NEXT_PUBLIC_RAG_API=http://localhost:5001
```

### 3. Start backend services

Trước khi chạy frontend, đảm bảo backend services đang chạy:

```bash
# Terminal 1: Law Service
cd ../backend/law-service
npm run dev

# Terminal 2: RAG Service
cd ../backend/rag-service
python app.py
```

### 4. Run development server

```bash
npm run dev
```

Application chạy tại: `http://localhost:3000`

---

## Project Structure

```
web/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Home page
│   │   ├── search/
│   │   │   └── page.tsx          # Search page
│   │   ├── chat/
│   │   │   └── page.tsx          # Chat page
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   │
│   └── lib/
│       └── api.ts                # API client & types
│
├── public/                       # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

---

## Pages Overview

### Home (`/`)

Landing page với 2 action cards:

-   **Tra cứu Pháp điển**: Link to `/search`
-   **Hỏi đáp Q&A**: Link to `/chat`

Features section giới thiệu ưu điểm của hệ thống.

### Search (`/search`)

**Left Panel**: Search results

-   Search bar với keyword input
-   Filter tabs (Tất cả / Văn bản / Điều khoản)
-   Display documents và articles
-   Click document để xem chi tiết

**Right Panel**: Document detail

-   Document metadata (số hiệu, loại, cơ quan...)
-   List các điều trong văn bản
-   Scroll trong panel (sticky)

### Chat (`/chat`)

**Chat Interface**:

-   User messages (green, right-aligned)
-   Assistant messages (white, left-aligned)
-   Citations hiển thị dưới assistant message
-   Relevance score cho mỗi citation

**Input Area**:

-   Text input với placeholder
-   Send button (disabled khi loading)
-   Disclaimer về AI

**Welcome Screen** (khi chưa có message):

-   Example questions
-   Click để fill vào input

---

## API Integration

### Law Service API

Base URL: `process.env.NEXT_PUBLIC_LAW_API`

Endpoints used:

-   `GET /api/v1/documents` - Get documents list
-   `GET /api/v1/documents/:id` - Get document detail
-   `GET /api/v1/documents/:id/articles` - Get document articles
-   `POST /api/v1/search` - Search

### RAG Service API

Base URL: `process.env.NEXT_PUBLIC_RAG_API`

Endpoints used:

-   `POST /api/v1/question` - Ask question

See `src/lib/api.ts` for full API client implementation.

---

## Styling

### Tailwind CSS

Utility-first CSS framework:

-   Responsive design với breakpoints (sm, md, lg, xl)
-   Custom colors trong `tailwind.config.ts`
-   Hover states và transitions
-   Dark mode support (optional)

### Color Scheme

-   **Primary** (Search): Blue (`blue-600`, `blue-700`)
-   **Secondary** (Chat): Green (`green-600`, `green-700`)
-   **Neutral**: Gray scales
-   **Error**: Red (`red-600`, `red-700`)

### Components

Reusable Tailwind classes:

-   Buttons: `px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700`
-   Cards: `bg-white rounded-xl shadow-md p-6`
-   Inputs: `px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500`

---

## Build & Deploy

### Build for Production

```bash
npm run build
```

Output: `.next/` directory

### Deploy to Vercel

#### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

#### Option 2: Vercel Dashboard

1. Connect GitHub repository
2. Import project
3. Set environment variables:
    - `NEXT_PUBLIC_LAW_API` (Law Service URL)
    - `NEXT_PUBLIC_RAG_API` (RAG Service URL)
4. Deploy

### Environment Variables (Production)

Sau khi deploy backend services lên Vercel, cập nhật URLs:

```env
NEXT_PUBLIC_LAW_API=https://your-law-service.vercel.app
NEXT_PUBLIC_RAG_API=https://your-rag-service.vercel.app
```

---

## Development

### Adding New Pages

1. Create new folder trong `src/app/`
2. Add `page.tsx` file
3. Next.js tự động tạo route

Example:

```
src/app/about/page.tsx → /about
```

### Adding API Endpoints

Update `src/lib/api.ts`:

```typescript
export const lawService = {
    // ... existing methods

    newMethod: async (params) => {
        const response = await lawApi.get('/new-endpoint', { params });
        return response.data;
    },
};
```

### TypeScript Types

All API types defined trong `src/lib/api.ts`:

-   `Document`
-   `Article`
-   `Citation`
-   `QuestionResponse`
-   etc.

---

## Testing

### Manual Testing Checklist

**Home Page**:

-   [ ] Buttons link to correct pages
-   [ ] Responsive on mobile

**Search Page**:

-   [ ] Search with keyword works
-   [ ] Filter tabs work (Tất cả/Văn bản/Điều khoản)
-   [ ] Click document shows detail
-   [ ] Articles load correctly
-   [ ] Error handling (no results, network error)

**Chat Page**:

-   [ ] Send message works
-   [ ] Loading indicator shows
-   [ ] Citations display correctly
-   [ ] Clear chat works
-   [ ] Example questions work
-   [ ] Error handling (network error, API error)

### Browser Compatibility

Tested on:

-   ✅ Chrome/Edge (latest)
-   ✅ Firefox (latest)
-   ✅ Safari (latest)

### Responsive Testing

Breakpoints:

-   Mobile: < 768px
-   Tablet: 768px - 1024px
-   Desktop: > 1024px

---

## Troubleshooting

### "Failed to fetch" errors

**Problem**: Cannot connect to backend APIs

**Solutions**:

1. Check backend services are running:
    ```bash
    curl http://localhost:5000/health
    curl http://localhost:5001/health
    ```
2. Verify `.env.local` has correct URLs
3. Check CORS settings trong backend

### Build errors

**Problem**: TypeScript errors during build

**Solutions**:

1. Run type check:
    ```bash
    npm run build
    ```
2. Fix type errors trong code
3. Update TypeScript types trong `src/lib/api.ts`

### Styling issues

**Problem**: Tailwind classes not working

**Solutions**:

1. Restart dev server:
    ```bash
    npm run dev
    ```
2. Check `tailwind.config.ts` content paths
3. Clear `.next/` cache:
    ```bash
    rm -rf .next && npm run dev
    ```

### Port already in use

**Problem**: Port 3000 is busy

**Solutions**:

```bash
# Use different port
PORT=3001 npm run dev

# Or kill process on port 3000 (Windows)
npx kill-port 3000
```

---

## Performance Optimization

### Implemented

-   ✅ Server Components (where possible)
-   ✅ Client Components only when needed (`'use client'`)
-   ✅ Image optimization (Next.js Image component - ready to use)
-   ✅ Font optimization (next/font)
-   ✅ CSS minification (Tailwind)

### Future Improvements

-   [ ] Add loading skeletons
-   [ ] Implement caching (React Query / SWR)
-   [ ] Code splitting per route (automatic with Next.js)
-   [ ] Add PWA support
-   [ ] Optimize bundle size

---

## Accessibility

### Current Implementation

-   Semantic HTML
-   Keyboard navigation support
-   Focus states for interactive elements
-   Alt text for icons (SVG)

### Future Improvements

-   [ ] ARIA labels
-   [ ] Screen reader testing
-   [ ] Color contrast improvements
-   [ ] Skip to main content link

---

## Contributing

### Code Style

-   Use TypeScript strict mode
-   Follow Next.js best practices
-   Use Tailwind utilities over custom CSS
-   Keep components small and focused

### Commit Messages

Format: `type: description`

Types:

-   `feat:` New feature
-   `fix:` Bug fix
-   `style:` UI/styling changes
-   `refactor:` Code refactoring
-   `docs:` Documentation

---

## Related Documentation

-   [Main Project README](../README.md)
-   [Law Service API](../backend/law-service/README.md)
-   [RAG Service API](../backend/rag-service/README.md)
-   [Deployment Guide](../docs/00-QUICK-START.md)

---

## License

GPL-3.0

---

## Contact

For issues and questions:

-   Open issue on GitHub
-   Check [Project Progress](../PROJECT_PROGRESS.md)

---

**Made with ❤️ for Vietnamese Law Tech**
