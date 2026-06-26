# EVERGREEN-COMMS — Course Context File (v2 · sau Phase 0)

> **CÁCH DÙNG:** Dán TOÀN BỘ file này vào đầu mỗi cuộc trò chuyện mới với Claude
> trước khi yêu cầu viết phase tiếp theo. Nó cấp đủ ngữ cảnh để Claude tiếp tục
> nhất quán mà tốn rất ít token. Sau mỗi phase, Claude sẽ giao bản cập nhật mới —
> luôn dùng bản mới nhất.
>
> **Thay đổi v1 → v2:** thêm 3 phase Auth (Node/TS) + 2 phase tính năng tin nhắn
> (reply/mention/reaction; receipts) + 1 phase Database performance & scaling.
> Lộ trình: 13 → **19 tài liệu** (Phase 0 → Phase 18). Thêm ADR-0004.

---

## A. Bối cảnh dự án
- Sản phẩm: hệ thống **chat (text / ảnh / voice message) + realtime voice** tích hợp vào
  game 2D farming **Evergreen Hollow** (Unity 2022 LTS).
- Tính chất: **vừa học vừa làm thật**, ưu tiên việc học. **Solo developer**, timeline ~12 tháng,
  ngân sách hạ tầng **$100–150/tháng**.
- Triết lý **"build from scratch"**.
  - ĐƯỢC PHÉP dùng: Opus codec, libsodium, các thành phần transport của WebRTC,
    LiteNetLib, database drivers, thư viện hash/JWT phổ thông (bcrypt/argon2, jose…).
  - KHÔNG dùng sản phẩm managed: Agora, Photon, Vivox, Twilio, Sendbird, Stream Chat,
    Auth0/Clerk/Firebase Auth (auth tự xây để học).
- Ngôn ngữ tài liệu: **tiếng Việt**.
- Quy tắc trình bày bắt buộc: luôn **tách FACT (sự thật kỹ thuật) vs INFERENCE
  (suy luận / khuyến nghị của Claude)**.

## B. Quy mô mục tiêu (ràng buộc thiết kế)
| Chỉ tiêu | MVP | Production |
|---|---|---|
| Users đồng thời | 100 | 500 |
| Voice đồng thời | 100 | 500 |
| Số người 1 client **nghe được** (proximity) | 7 | 15 |
| Latency voice mục tiêu | <150–200 ms | <150–200 ms |
| Availability | — | 99% |

> Chìa khóa để con số 500 khả thi: **proximity voice** — dù 500 người cùng map,
> mỗi client chỉ nhận & giải mã âm thanh của 7→15 người gần nhất. Tải tăng theo
> "số người gần" chứ không theo tổng số người.
>
> Ở quy mô 500: **một Postgres primary + Redis cache + index tốt là đủ**.
> Replication chủ yếu để **failover/HA** (mục tiêu 99%), KHÔNG để gánh tải.
> **Sharding KHÔNG triển khai** — chỉ dạy ở mức khái niệm (Phase 16).

## C. Tech stack đã chốt
- **Chat & Voice (lõi realtime): .NET (C#), bản LTS hiện hành (.NET 10).**
  - Chat: **WebSocket** (trên TCP). Voice: **UDP tự xây** (tham khảo/để dành WebRTC),
    thư viện **LiteNetLib**.
- **Auth (service riêng): Node.js + TypeScript.** Phát hành & ký **JWT**; hash mật khẩu
  (**bcrypt** hoặc **argon2**). → Hệ thống là **polyglot** (đa ngôn ngữ).
- Dữ liệu: **PostgreSQL** (bền vững / quan hệ) + **Redis** (nóng / cache / pub-sub / revoke).
- Media: **AWS S3**. Message broker: **RabbitMQ**. Load balancer: **nginx**.
- Hạ tầng: **Docker**, self-hosted **DigitalOcean / Vultr**,
  single-region (MVP) → multi-region (production).

## D. Lộ trình 19 phase
| # | Tên | Trạng thái |
|---|---|---|
| 0 | Nền tảng & môi trường (.NET, Docker) | ✅ DONE |
| 1 | Global chat (text) MVP — emoji chạy sẵn (UTF-8); danh tính *tạm* có seam | ⏳ |
| 2 | Auth P1 — Node/TS & cấp token (register/login, hash, phát JWT) | ⏳ |
| 3 | Auth P2 — JWT chuyên sâu & chiến lược verify (HS256 vs RS256/ES256/EdDSA; local vs JWKS vs gọi Node) | ⏳ |
| 4 | Auth P3 — Refresh, revoke (Redis), hardening & tích hợp; .NET verify JWT ở WS handshake | ⏳ |
| 5 | Lưu trữ & lịch sử — PostgreSQL, retention; **index & query-opt (EXPLAIN, keyset)**; **partition bảng** | ⏳ |
| 6 | 1-1 & group chat — Redis pub/sub; giới thiệu cache-aside | ⏳ |
| 7 | Presence, offline, push — **+ typing indicator** | ⏳ |
| 8 | Tương tác tin nhắn — reply, @mention, emoji reaction | ⏳ |
| 9 | Delivery & read receipts (đã gửi / đã xem) | ⏳ |
| 10 | Media P1 — Ảnh (S3, presigned URL, nén) **+ custom emoji** | ⏳ |
| 11 | Media P2 — Voice message (Opus, 30s) | ⏳ |
| 12 | Blocking, muting & hardening chat (không rò receipt/mention cho người bị chặn) | ⏳ |
| 13 | Voice P1 — Nền tảng UDP transport (RTT, packet flow) | ⏳ |
| 14 | Voice P2 — Codec & signaling (Opus, jitter, MCU/SFU/Mesh) | ⏳ |
| 15 | Proximity voice & voice room (nghe 7→15 người gần) | ⏳ |
| 16 | **Database performance & scaling** — index nâng cao, partition sâu, replication/read-replica, tách read–write, **đồng bộ Redis↔PG**, connection pooling, **sharding (khái niệm)** | ⏳ |
| 17 | Production — App/infra scale & budget (nginx, vertical/horizontal, bandwidth/CPU) | ⏳ |
| 18 | Production — Multi-region & reliability (failover, giám sát) | ⏳ |

## E. Quy ước biên soạn (giữ nguyên qua mọi phase)
- Đầu ra: **PDF**. Pipeline: Markdown (+ khối ```mermaid```) → render SVG → HTML
  (có syntax highlight) → PDF. (Claude giữ engine `build_pdf.py` để dựng lại.)
- Sơ đồ: **Mermaid**.
- Cấu trúc mỗi phase: **Lý thuyết → Kiến trúc & ADR → Thực hành (code chạy được)
  → Test/Deploy → SPEC & Checklist nghiệm thu**.
- Độ dài mục tiêu: **~1000+ dòng nguồn** mỗi phase.
- Hộp callout: `key` (◆ Khái niệm cốt lõi), `tip` (✔ Mẹo/Best practice),
  `warn` (▲ Cẩn thận), `note` (ℹ Ghi chú).
- ADR theo mẫu: **Bối cảnh → Quyết định → Lựa chọn thay thế & so sánh → Hệ quả**.
- **Lược đồ tiến hoá bằng migration:** Phase 5 dựng `messages` có chừa chỗ; các bảng
  `reactions` / `receipts` và cột `reply_to` do **chính các phase tính năng** tạo ra.
- **Đồng bộ Redis↔Postgres:** giới thiệu cache-aside *trong ngữ cảnh* ở Phase 6/7,
  đào sâu (write-through, invalidation, nhất quán, nguồn sự thật) ở Phase 16.
- Workflow: **một phase một lần**. Viết xong phase N → chờ user nhắn
  **"đã xong Phase N"** mới viết phase N+1.

## F. Sổ tên gọi (CANONICAL — phase sau KHÔNG được mâu thuẫn)
- Repo: **evergreen-comms** (monorepo, đã `git init`).
  Thư mục: `src/`, `docs/adr/`, `docs/phases/`.
- **Chat/Voice backend:** **EvergreenBackend** (ASP.NET Core *minimal API*, .NET 10).
- **Auth service:** tên **`auth`**, **Node.js + TypeScript**, cổng **`4000`**
  (sẽ dựng ở Phase 2; *chưa* có trong `docker-compose.yml` của Phase 0).
- Dịch vụ trong `docker-compose.yml` (sau Phase 0):
  - `postgres` — image `postgres:17`, DB `evergreen`, user/pass `postgres`/`postgres`,
    cổng `5432`, volume `pgdata`, healthcheck `pg_isready`.
  - `redis` — image `redis:7`, cổng `6379`, healthcheck `redis-cli ping`.
  - `api` — build từ `./src/EvergreenBackend`, cổng `8080`,
    `depends_on … condition: service_healthy`.
  - *(Phase 2 thêm)* `auth` — Node/TS, cổng `4000`.
- **Sở hữu dữ liệu:** `auth` sở hữu `users` (+ bảng refresh token);
  chat (.NET) sở hữu `conversations`, `messages`, `reactions`, `receipts`.
  *DB riêng hay chung* → chốt ở Phase 2.
- **Hợp đồng JWT (khung — chốt chi tiết ở Phase 3):**
  claim `sub` = user_id, `iat`, `exp`, `jti` (cho revoke);
  **thuật toán ký để ngỏ, mặc định nghiêng RS256**;
  cách công khai public key (JWKS endpoint / file) chốt ở Phase 3.
  Chat (.NET) **chỉ verify** token; KHÔNG gọi sang `auth` mỗi request (trừ khi chọn
  hướng introspect — sẽ so sánh ở Phase 3).
- Kết nối: trong Docker dùng **host = tên dịch vụ** (`postgres`, `redis`, `auth`),
  **KHÔNG** dùng `localhost`. Chuỗi Redis có **`abortConnect=false`**.
  Cấu hình qua biến môi trường: `ConnectionStrings__Postgres`, `ConnectionStrings__Redis`.
- Driver / DI (.NET): `Npgsql` (`AddNpgsqlDataSource`),
  `StackExchange.Redis` (`AddSingleton<IConnectionMultiplexer>`).
- Endpoint đã có (api): `GET /` (chuỗi báo sống), `GET /health`
  (kiểm tra Postgres `SELECT 1` + Redis `PING`, trả `200` / `503`).

## F-bis. Sổ ADR
- **ADR-0001** — Chat/Voice dùng **.NET (C#)**; *ngoại lệ:* Auth là service Node/TS.
- **ADR-0002** — Lưu trữ: **PostgreSQL + Redis**.
- **ADR-0003** — Môi trường dev: **Docker Compose**.
- **ADR-0004 (mới, chi tiết ở Phase 2)** — **Auth là service riêng bằng Node.js + TypeScript;
  JWT là hợp đồng giữa hai stack.** (Việc *chọn thuật toán ký* HS256 vs RS256/EdDSA là một
  ADR riêng nằm trong Phase 3/4 — vì đó chính là phần cần so sánh sâu.)

## G. Tóm tắt & "điểm móc nối" từng phase
- **Phase 0 (DONE):** Dựng môi trường dev. Đã thiết lập:
  cấu trúc repo, `docker-compose.yml` (postgres + redis + api, có healthcheck &
  `depends_on service_healthy`, volume `pgdata`), project `EvergreenBackend` với
  endpoint `/health`, `Dockerfile` multi-stage, và 3 ADR (0001, 0002, 0003).
  Sơ đồ kiến trúc tổng & bảng thuật ngữ đã phản ánh đủ 19 phase + service auth.
  → **Mọi phase sau xây tiếp TRỰC TIẾP trên project `EvergreenBackend` +
  `docker-compose.yml` này.**
- **Vị trí các tính năng "học trong ngữ cảnh" (không có phase riêng):**
  emoji (UTF-8) → Phase 1; index + partition → Phase 5; cache-aside (giới thiệu) → Phase 6/7;
  typing indicator → Phase 7; custom emoji (upload ảnh) → Phase 10.
- **Móc nối cho các phase mới (khi viết tới):**
  - *Phase 2–4 (Auth):* sản ra `users`/refresh-token + endpoint cấp/refresh/revoke JWT;
    Phase 4 sửa **chỗ kiểm tra danh tính ở WS handshake của Phase 1** từ "tạm" sang verify JWT thật.
  - *Phase 8 (Tương tác tin nhắn):* tạo bảng `reactions`, cột `reply_to` trên `messages`,
    parse `@mention` → bắn push (dùng hạ tầng Phase 7).
  - *Phase 9 (Receipts):* trạng thái đã gửi/đã xem theo từng người; lưu ý write-amplification
    trong group (xử lý kỹ ở Phase 16).
  - *Phase 16 (DB scaling):* tối ưu mọi bảng đã có (index/partition), replication/read-replica,
    chốt mẫu đồng bộ Redis↔Postgres.
- *(Phase 1 → 18: điền tóm tắt "đã làm gì" + "cái mà phase sau phụ thuộc" sau khi hoàn thành mỗi phase.)*

## H. Nguồn sự thật (đọc khi cần độ chính xác)
- **Bản chính** = các **PDF** bạn đã tải về + **repo `evergreen-comms`**
  (code, ADR trong `docs/adr/`, PDF trong `docs/phases/`).
- Khi cần Claude dùng lại chi tiết chính xác (đoạn code, cấu hình cụ thể),
  **dán lại file/đoạn liên quan** vào chat (hoặc để Claude Code đọc repo) thay vì
  trông cậy trí nhớ của Claude.
