# Toàn bộ yêu cầu hạ tầng cho deploy lên Private Cloud (GreenNode)

> Tài liệu này chứa toàn bộ các thông số và tính toán chi tiết để triển khai hệ thống AI RAG + LLM (Arcee-VyLinh) trên private cloud GreenNode. Tài liệu được tổng hợp từ bản "VN Law Advisor Mini — Deployment Parameters" và các giả định hợp lý cho bài toán lên đến 1 triệu vectors.

---

## Mục lục

1. Tóm tắt nhanh (mục tiêu)
2. Cấu hình chi tiết theo component

   * LLM Service (Arcee-VyLinh)
   * RAG Service
   * ChromaDB (Vector DB)
   * Supabase / PostgreSQL
   * Frontend (Next.js)
   * Law Service (Node.js)
3. Sizing theo quy mô (conservative / moderate / ambitious / 1M vectors)

   * Giả định
   * Tính toán lưu trữ & RAM cho ChromaDB
   * Tính toán Postgres
   * LLM capacity per stage
4. Node pools, disks, network, IOPS, và phần cứng đề xuất (cụ thể)
5. High-availability, backup & DR (chính sách cụ thể)
6. Networking, Security, Secrets
7. Observability & Alerts (metrics + thresholds)
8. Autoscaling & resource orchestration (Kubernetes specifics)
9. Storage & backup concrete numbers
10. CI/CD, image registry, deployment strategy
11. Concrete checklist để bàn giao cho Greennode
12. Các lưu ý đặc thù / tối ưu hóa
13. Quick reference: recommended minimum hardware (production, moderate use)
14. Kết luận & hành động tiếp theo

---

# 1) Tóm tắt nhanh (mục tiêu)

* Deploy microservices: Frontend (Next.js), Law Service (Node.js), RAG Service (Python), LLM Service (Arcee-VyLinh), Self-host Supabase (Postgres), ChromaDB (vector DB).
* Mục tiêu: private cloud GreenNode, không cần tính tiền. Toàn bộ các thông số máy móc, storage, network, HA/DR, monitoring phải rõ ràng.
* Quy mô mục tiêu: phục vụ thử nghiệm → production, có thể mở rộng tới ~10k+ users đồng thời tổng cộng **1,000,000 vectors**.

---

# 2) Cấu hình chi tiết theo component

> Ghi chú: "requests" là tài nguyên tối thiểu để chạy; "limits" là mức tối đa khuyến nghị; "replicas" là số bản sao khởi đầu cho HA/scale.

## A. LLM Service — Arcee-VyLinh (core)

* **Phần mềm**: Python 3.8+, FastAPI/uvicorn, transformers, torch (GPU build), nvidia-container-toolkit.
* **Model**: 3B params, context 32K.

**Node / Pod (khuyến nghị tối thiểu để production nhỏ):**

* CPU: request 8 vCPU, limit 16 vCPU
* RAM: request 16 GiB, limit 32 GiB
* GPU: `1` GPU; **GPU memory >= 8GB (min)**, **16GB+ recommended**
* Storage (local NVMe): 50 GB (model + swap + logs). Model file ~7–10 GB.

**Container settings (k8s resource example):**

* requests: cpu=8, mem=16Gi
* limits: cpu=16, mem=32Gi, devices: nvidia.com/gpu=1
* readinessProbe: HTTP `/health` => 200
* livenessProbe: `/live`

**Concurrency & replicas**:

* Single GPU instance có thể phục vụ ~10–50 concurrent requests (tùy prompt length / batching).
* Start với `replicas = 1`; HPA dựa trên GPU util / queue length, scale tới `replicas = 3` khi cần.

**Monitoring:** GPU util, GPU memory, inference latency (p50/p95), request queue length, OOM events.

---

## B. RAG Service (Python)

* **Vai trò**: tính embedding, điều phối tìm kiếm vector, lắp prompt.
* **Per-pod**:

  * CPU: request 2 vCPU, limit 4 vCPU
  * RAM: request 2 GiB, limit 8 GiB (nếu tải embedding lên local: 8–12 GiB)
  * Storage: 10–20 GB
* **Replicas**: conservative 1–2; moderate 3–5
* **Network**: latency thấp tới ChromaDB & LLM service.

---

## C. ChromaDB (Vector DB)

* **Role**: lưu vectors (dim=768), ANN index (HNSW/FAISS...).
* **Deployment**: statefulset; start single instance, mở rộng theo shards.
* **Per-instance sizing (khởi tạo)**:

  * CPU: 4–8 vCPU
  * RAM: phụ thuộc trên số vectors (xem phần sizing)
  * Storage: NVMe SSD, provision IOPS
  * Disk size: persistent (xem phần Storage)
* **Index/memory**: embedding float32 768 dims = 768*4 = 3,072 B (~3 KB) / vector. Index overhead ~2–5× raw.
* **Replication**: ít nhất 2 replicas cho production.
* **Network**: colocate Chroma với RAG (latency < 1 ms ideal).

---

## D. Supabase / PostgreSQL (Self-hosted)

* **Node**:

  * CPU: 4–8 vCPU start; scale tới 8–16 vCPU
  * RAM: 8–16 GiB start; 32 GiB cho workloads nặng
  * Storage: SSD (NVMe) start 50 GB
* **Connections**: limit ~120; dùng PgBouncer
* **HA**: primary + replica (hot standby)
* **Backups**: daily snapshot + WAL archiving

---

## E. Frontend (Next.js)

* **Deploy**: self-hosted hoặc CDN
* CPU: 1–2 vCPU per instance
* RAM: 1–2 GiB
* Storage: 10–20 GB
* SSR: autoscale theo load

---

## F. Law Service (Node.js)

* CPU: request 1 vCPU, limit 2–4 vCPU
* RAM: request 256–512 MiB, limit 1–2 GiB
* DB pool size: 10–20
* Replicas: >=2

---

# 3) Sizing theo quy mô (conservative / moderate / ambitious / 1M vectors)

## Giả định chung

* Embedding dim = 768, float32 => `3 KB` raw per vector.
* Index overhead factor: conservative = 3×, optimistic = 2×.

### Tính toán lưu trữ & RAM cho ChromaDB

* **Raw size per vector** = 768 * 4 bytes = 3,072 bytes ≈ 3 KB

|           Quy mô | Số vectors | Dung lượng raw | Index overhead 3× |           RAM recommended |
| ---------------: | ---------: | -------------: | ----------------: | ------------------------: |
| Hiện tại (ví dụ) |        857 |        ~2.6 MB |             ~8 MB |                  0.05 GiB |
|              10× |      8,570 |       ~25.7 MB |            ~77 MB |                   0.1 GiB |
|             100× |     85,700 |        ~257 MB |           ~770 MB |                   1–2 GiB |
|           1,000× |    857,000 |       ~2.57 GB |           ~7.7 GB |                 12–16 GiB |
|        1,000,000 |  1,000,000 |        ~3.0 GB |           ~9.0 GB | **12–20 GiB** recommended |

**Disk (persistent)**: cho 1M vectors nên reserve **≥ 50–200 GB** (index + metadata + room for snapshots/replicas).

### Postgres sizing (ước lượng)

* Với dữ liệu metadata và logs cho 1M vectors (metadata nhẹ): Postgres 8–16 GiB RAM đủ; cho OLTP/analytic nặng thì 32 GiB.

### LLM capacity per stage

* **Testing**: 1 GPU (8 GB) OK
* **Moderate (1k DAU)**: 1 GPU (16 GB) + 1–2 standby replicas
* **Ambitious (10k DAU)**: 2–4 GPUs across instances; use batching & model parallel if cần

---

# 4) Node pools, disks, network, IOPS, hardware recommendations (cụ thể)

## NodePools (k8s)

1. **GPU pool (LLM)**

   * Node: 16 vCPU, 64 GiB RAM, `1× GPU (16GB)`
   * Disk: 500 GB NVMe local
   * Count: start 1 -> scale to 3
2. **High-mem pool (Chroma/DB)**

   * Node: 8–16 vCPU, 64–128 GiB RAM
   * Disk: NVMe 1–2 TB
   * Count: 1–3
3. **General pool (apps)**

   * Node: 4–8 vCPU, 16–32 GiB RAM
   * Count: 2–5
4. **Small pool (frontends)**

   * Node: 2 vCPU, 4 GiB RAM

## Disk & IOPS

* **NVMe SSD** cho DB và Chroma
* IOPS:

  * Postgres: 5k–15k IOPS
  * Chroma: 3k–10k IOPS
* Tách volumes: OS / DB data / DB WAL / Chroma index / model files

## Network

* Private VLAN cho internal traffic
* **10 Gbps internal** recommended; nếu không được, 1–2 Gbps với colocated services.

## GPU classes

* **8 GB**: MIN cho test
* **16 GB**: RECOMMENDED cho 3B model
* **40+ GB** (A100/H100): cho production scale lớn

---

# 5) High-availability, backup & DR (concrete)

## Postgres

* Primary + 1 synchronous replica + 1 async cross-AZ (nếu có)
* Backups: full snapshot daily; WAL archiving (retain 7–14 days)
* RTO target: < 15 phút
* RPO target: ≤ 1 giờ (tune via WAL retention)

## ChromaDB

* Snapshot: daily full, hourly incremental (nếu ingestion cao)
* Replicas: ít nhất 2

## LLM model files

* Store model artifacts versioned on S3-compatible object store; local cache on nodes; backup khi update

## DR

* Cross-region snapshot replication (nếu GreenNode hỗ trợ)
* Test restore quarterly

---

# 6) Networking, Security, Secrets

* Private network cho DB/Chroma/LLM/RAG. LB trong DMZ cho public ingress
* K8s Network Policies giới hạn pod-to-pod
* Secrets: HashiCorp Vault hoặc Kubernetes sealed-secrets; rotate quarterly
* API auth: JWT cho user endpoints; mTLS cho service-to-service
* TLS: terminate at LB; enforce TLS 1.2+
* RBAC k8s + audit logging

---

# 7) Observability & Alerts (metrics + thresholds)

**LLM**

* GPU util > 85% => alert
* GPU mem usage > 90% => alert
* inference latency p95 > 5s => warning
* request queue length > 10 => warning

**Chroma**

* query latency > 200 ms => warning
* memory usage > 80% => alert
* I/O wait > 20% => alert

**Postgres**

* replication lag > 5s => alert
* connections > 80% pool => warning
* slow queries > 1s => warning

**App**

* CPU > 80% for 5 min => scale
* 5xx rate > 2% => alert

**Tooling**

* Prometheus + Grafana
* Loki/ELK cho logs
* Alertmanager cho Slack/Email/PagerDuty

---

# 8) Autoscaling & resource orchestration (Kubernetes specifics)

**HPA examples**

* Law Service / RAG / Frontend: HPA CPU-based, target 60%, min 2 max 10
* LLM: CUSTOM metrics (GPU util or request queue). Rules:

  * scale up if GPU util > 80% (2 min) OR queue length > 10
  * scale down if GPU util < 30% & queue empty for 5 min
* Chroma: scale by nodes + reindex/shard (manual or operator)

**Pod resource recap**

* LLM pod: requests cpu=8 mem=16Gi; limits cpu=16 mem=32Gi; gpu=1
* Chroma pod: requests cpu=4 mem=16Gi (tune theo vectors)
* Postgres statefulset: requests cpu=4 mem=16Gi

---

# 9) Storage & backup concrete numbers

**Persistent volumes** (start / headroom for 1M vectors):

* LLM model: 50–100 GB fast NVMe
* Postgres data: start 100 GB NVMe (growable)
* Postgres WAL: 50 GB NVMe (separate)
* Chroma index/data: start 200 GB NVMe

**Snapshot schedule**

* Postgres: full snapshot daily @ 02:00
* WAL: continuous archive; retain 7 days
* Chroma: hourly incremental, daily full
* Model artifacts: store in object store when updated

---

# 10) CI/CD, image registry, deployment strategy

* Use internal registry (Harbor). Tag with semantic version + git sha
* CI: GitHub Actions / GitLab CI -> build images -> push -> deploy to staging -> manual promote to prod
* Deployment strategy: canary/blue-green for LLM updates (split traffic)
* IaC: Terraform for infra; Helm for k8s

---

# 11) Concrete checklist để bàn giao cho Greennode

1. Xác nhận GPU SKU (8GB/16GB/40GB) có sẵn. Chọn `16GB` min cho prod.
2. Tạo nodepools: GPU, high-mem, general, small
3. Provision NVMe volumes: model(100GB), DB data(100GB), DB WAL(50GB), Chroma(200GB)
4. Deploy k8s (>=1.26) + Nvidia device plugin
5. Install infra: ingress, cert-manager, prometheus/grafana, loki, pgbouncer
6. Deploy Postgres operator + replication + backups
7. Deploy Chroma statefulset + snapshots
8. Deploy LLM deployment with GPU resources (start 1 replica)
9. Configure secrets via Vault / sealed-secrets
10. Setup monitoring & alerts
11. Run load test (simulate RAG QPS & LLM concurrency)
12. DR test: snapshot restore quarterly

---

# 12) Các lưu ý đặc thù / tối ưu hóa

* **Batching**: batch inference tăng throughput
* **Prompt length**: 32K context tăng cost — chunk / truncate khi cần
* **Indexing**: chunk + metadata filter để giảm candidate set
* **Cold start**: giữ warm pool
* **Theo dõi thực tế**: tinh chỉnh replica & HPA dựa trên telemetry

---

# 13) Quick reference: recommended minimum hardware (production, moderate use)

* **1× LLM server (GPU)**: 16 vCPU, 64 GiB RAM, 1×GPU(16GB), 500GB NVMe
* **1× Chroma node**: 8 vCPU, 64 GiB RAM, 1 TB NVMe
* **1× Postgres primary**: 8 vCPU, 32 GiB RAM, 200 GB NVMe + WAL 50 GB
* **General app nodes (2)**: each 4 vCPU, 16 GiB RAM
* **Network**: private 10 Gbps internal recommended

