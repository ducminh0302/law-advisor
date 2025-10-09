# Phân Tích Yêu Cầu Hạ Tầng Cloud cho VN Law Advisor Mini trên Greennode Private Cloud

**Tác giả:** Manus AI
**Ngày:** 08/10/2025

## 1. Tổng quan

Báo cáo này trình bày chi tiết các yêu cầu về hạ tầng điện toán đám mây (cloud infrastructure) cần thiết để triển khai ứng dụng **VN Law Advisor Mini** trên nền tảng private cloud của Greennode. Toàn bộ các phân tích và đề xuất được xây dựng dựa trên tài liệu `DEPLOYMENT_PARAMETERS.md` do người dùng cung cấp. Các thông số kỹ thuật được tính toán để đáp ứng mức độ sử dụng **"Ambitious Usage (Mature Stage)"**, nhằm đảm bảo hệ thống có đủ khả năng mở rộng, duy trì hiệu năng cao và hoạt động ổn định trong dài hạn.

## 2. Phân tích chi tiết yêu cầu cho từng dịch vụ

Kiến trúc của VN Law Advisor Mini bao gồm nhiều microservices, mỗi dịch vụ có những yêu cầu riêng biệt về tài nguyên. Dưới đây là phân tích chi tiết cho từng thành phần, giả định tất cả đều được triển khai trên hạ tầng của Greennode.

### 2.1. Frontend Service (Next.js 14)

Frontend là giao diện người dùng chính của ứng dụng, được xây dựng bằng Next.js 14. Dịch vụ này sẽ xử lý việc hiển thị giao diện, tương tác người dùng và thực hiện Server-Side Rendering (SSR). Để đảm bảo tính sẵn sàng cao và khả năng chịu tải cho khoảng 200 người dùng đồng thời, chúng tôi đề xuất triển khai dịch vụ này dưới dạng container (Docker) với ít nhất hai (2) instances, được đặt sau một Load Balancer.

- **Công nghệ:** Next.js 14, TypeScript, TailwindCSS.
- **Yêu cầu tài nguyên (mỗi instance):**
    - **vCPU:** 2 cores (để tối ưu hóa cho SSR và xử lý yêu cầu nhanh chóng).
    - **RAM:** 2 GB.
    - **Storage:** ~1 GB (cho container image và các tài sản tĩnh).

### 2.2. Law Service (Node.js/Express)

Law Service chịu trách nhiệm xử lý các logic nghiệp vụ liên quan đến việc quản lý, truy xuất và cập nhật các văn bản pháp luật từ cơ sở dữ liệu. Đây là một dịch vụ I/O-intensive, do đó cần đảm bảo khả năng xử lý nhiều kết nối đồng thời tới cơ sở dữ liệu.

- **Công nghệ:** Node.js, Express.js.
- **Yêu cầu tài nguyên (mỗi instance):**
    - **vCPU:** 1 core.
    - **RAM:** 1 GB.
    - **Storage:** ~500 MB.
    - **Kiến nghị:** Tương tự Frontend, dịch vụ này nên được triển khai với hai (2) instances sau Load Balancer để tăng cường độ tin cậy.

### 2.3. RAG Service (Python/Flask)

RAG (Retrieval-Augmented Generation) Service là cầu nối giữa người dùng và mô hình ngôn ngữ lớn (LLM). Dịch vụ này thực hiện việc tìm kiếm thông tin trong cơ sở dữ liệu vector (vector search) và tạo ra các prompt chính xác cho LLM Service. Do phải tải model embedding vào bộ nhớ, dịch vụ này yêu cầu một lượng RAM tương đối lớn.

- **Công nghệ:** Python, Flask, Sentence-Transformers.
- **Yêu cầu tài nguyên (mỗi instance):**
    - **vCPU:** 2 cores (cho các tác vụ tính toán embedding).
    - **RAM:** 2 GB.
    - **Storage:** ~2 GB.
    - **Kiến nghị:** Triển khai hai (2) instances sau Load Balancer.

### 2.4. LLM Service (Arcee-VyLinh)

Đây là thành phần tiêu tốn nhiều tài nguyên nhất, thực hiện các tác vụ suy luận (inference) của mô hình ngôn ngữ Arcee-VyLinh 3 tỷ tham số. Để đạt được hiệu năng tối ưu và thời gian phản hồi thấp, việc sử dụng GPU là bắt buộc. Dịch vụ này nên được triển khai trên một máy ảo (VM) hoặc máy chủ vật lý riêng có GPU Passthrough.

- **Công nghệ:** Python, FastAPI/Flask, Transformers, Torch.
- **Yêu cầu tài nguyên:**
    - **vCPU:** 8-16 cores.
    - **RAM:** 32 GB.
    - **GPU:** NVIDIA GPU với ít nhất 16 GB VRAM.
    - **Storage:** 30 GB (SSD) để chứa model, hệ điều hành và logs.
    - **Kiến nghị:** Cần áp dụng chiến lược "warm-up" để giữ model luôn sẵn sàng trong bộ nhớ, giảm thiểu độ trễ khi có yêu cầu đầu tiên.

### 2.5. Cơ sở dữ liệu

Cả hai cơ sở dữ liệu là Self-host Supabase (PostgreSQL) và ChromaDB (Vector Database) đều là các thành phần stateful, yêu cầu lưu trữ bền vững (persistent storage) và hiệu năng truy xuất cao. Chúng tôi đề xuất triển khai chúng dưới dạng container với persistent volume được cấp phát từ ổ cứng SSD.

- **Self-host Supabase (PostgreSQL):**
    - **vCPU:** 2 cores.
    - **RAM:** 4 GB.
    - **Storage:** 10 GB (SSD).
- **ChromaDB (Vector Database):**
    - **vCPU:** 2 cores.
    - **RAM:** 4 GB.
    - **Storage:** 10 GB (SSD).
- **Kiến nghị:** Cần thiết lập cơ chế sao lưu (backup) và phục hồi (restore) định kỳ cho cả hai cơ sở dữ liệu để đảm bảo an toàn dữ liệu.

## 3. Bảng tổng hợp yêu cầu hạ tầng

Dưới đây là bảng tổng hợp toàn bộ yêu cầu về tài nguyên hạ tầng để triển khai hệ thống VN Law Advisor Mini trên Greennode Private Cloud, hướng tới mức tải "Ambitious Usage".

| Dịch vụ                  | Số lượng Instances | vCPU (Tổng) | RAM (Tổng) | Storage (Tổng) | Ghi chú                                                    |
| ------------------------- | ------------------ | ----------- | ---------- | -------------- | ---------------------------------------------------------- |
| Frontend Service          | 2                  | 4           | 4 GB       | 2 GB           | Đặt sau Load Balancer                                      |
| Law Service               | 2                  | 2           | 2 GB       | 1 GB           | Đặt sau Load Balancer                                      |
| RAG Service               | 2                  | 4           | 4 GB       | 4 GB           | Đặt sau Load Balancer                                      |
| LLM Service               | 1                  | 16          | 32 GB      | 30 GB (SSD)    | Yêu cầu GPU NVIDIA với 16GB+ VRAM                        |
| Self-host Supabase (DB)   | 1                  | 2           | 4 GB       | 10 GB (SSD)    | Yêu cầu Persistent Volume, Backup/Restore                 |
| ChromaDB (Vector DB)      | 1                  | 2           | 4 GB       | 10 GB (SSD)    | Yêu cầu Persistent Volume, Backup/Restore                 |
| **Tổng cộng (Ước tính)**  | **9**              | **30**      | **50 GB**  | **57 GB**      | **Chưa bao gồm tài nguyên cho Load Balancer, hệ thống giám sát và các dịch vụ mạng khác.** |

## 4. Kiến trúc triển khai và các khuyến nghị khác

Để đảm bảo một hệ thống linh hoạt, dễ quản lý và có khả năng mở rộng, chúng tôi đề xuất các phương pháp triển khai sau:

- **Containerization:** Tất cả các dịch vụ nên được đóng gói thành các Docker container. Điều này giúp chuẩn hóa môi trường và đơn giản hóa quá trình triển khai.
- **Container Orchestration:** Sử dụng một nền tảng điều phối container như Kubernetes (nếu Greennode hỗ trợ) là lựa chọn lý tưởng để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container hóa. Nếu không, Docker Compose có thể là một giải pháp thay thế cho các môi trường đơn giản hơn.
- **Networking:** Thiết lập một mạng riêng ảo (Virtual Private Network - VPN) để các dịch vụ nội bộ có thể giao tiếp với nhau một cách an toàn. Chỉ nên public các cổng dịch vụ của Frontend và API Gateway (nếu có) ra ngoài Internet.
- **Load Balancing:** Sử dụng dịch vụ Load Balancer do Greennode cung cấp để phân phối lưu lượng truy cập một cách đồng đều đến các dịch vụ stateless (Frontend, Law, RAG), qua đó tăng cường khả năng chịu lỗi và hiệu suất.
- **Monitoring & Logging:** Triển khai một hệ thống giám sát và ghi log tập trung (ví dụ: Prometheus, Grafana, ELK Stack) là cực kỳ quan trọng. Hệ thống này sẽ giúp theo dõi tình trạng hoạt động, tài nguyên sử dụng (CPU, RAM, GPU), độ trễ và tỷ lệ lỗi của toàn bộ các dịch vụ, từ đó có những điều chỉnh kịp thời.

