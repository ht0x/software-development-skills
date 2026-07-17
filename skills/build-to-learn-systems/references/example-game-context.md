<!--
WORKED EXAMPLE — a GAME-CLIENT course manifest (companion to
example-evergreen-context.md, which shows a BACKEND course).

Read this when the learner's course is game / client-side / offline-asset shaped, to
see how the same manifest structure adapts to a non-server domain. Note especially:

  * §A records DOMAIN, DEPTH LEVEL, and a REFERENCE SOURCE (this course rebuilds an
    existing open-source game, so every phase is grounded in real files).
  * §B's "scale" is not users/sec — for a game client it's fidelity, platform, and
    frame budget. Adapt the axis to the domain; don't force throughput metrics.
  * §C has NO ports, brokers, or datastores. A game client has none. Don't invent them.
  * §D points at the Roadmap document and marks the depth standard.
  * §F's canonical names are project/scene/namespace names — the game equivalent of
    service names and ports.

The body is in Vietnamese because that was the course's chosen language (Core rule 5);
the structure is what matters here, not the language.
-->

# GeoAdventures — Course Context File (v2)

> CÁCH DÙNG: Dán toàn bộ file này vào đầu mỗi phiên làm việc mới trước khi yêu cầu
> phase tiếp theo. Nó cung cấp vừa đủ ngữ cảnh để tiếp tục nhất quán mà tốn rất ít
> token. File được cập nhật sau mỗi phase — luôn dùng bản mới nhất.
>
> **Thay đổi v1 → v2:** thêm tài liệu Lộ trình chi tiết; nâng chuẩn biên soạn lên
> **Deep** (từ điển thuật ngữ, so sánh giải pháp, mổ xẻ code, sai lầm thường gặp);
> Phase 0 cần viết lại theo chuẩn mới.

## A. Bối cảnh dự án
- **Xây gì:** Dựng lại từ đầu game **Geographical Adventures** (bản gốc của Sebastian
  Lague) bằng Unity — game lái máy bay quanh quả địa cầu 3D dựng từ dữ liệu địa lý
  thật, thả gói hàng đến đúng các thành phố.
- **Domain:** **game client** → dùng playbook game trong `domain-playbooks.md`.
  (Không có server, không database, không port — đừng bịa ra.)
- **Bản chất:** Học-trước (learning-first). Một người học, trình độ **người mới** với
  Unity/game dev. Không ràng buộc thời gian/ngân sách.
- **"From scratch" allow/deny:**
  - *Cho phép:* Unity engine, gói Unity chính thức (Input System, TextMeshPro,
    Newtonsoft Json), thư viện tam giác hoá bên thứ ba (Phase 6).
  - *Tự viết lại:* thư viện tiện ích của tác giả gốc (`ComputeHelper`, `IcoSphere`,
    hàm toán) — viết lại phần cần khi tới nơi, không chép cả cục.
  - *Bản gốc chỉ để đối chiếu*, không fork/chép nguyên.
- **Ngôn ngữ tài liệu:** **Tiếng Việt** (khóa — Core rule 5).
- **Độ sâu:** **Deep** (~2000–2500 dòng/phase) — vì học viên mới với domain và hệ
  thống phức tạp. Xem §E.
- **Quy tắc Fact vs Inference:** luôn tách rõ "Sự thật kỹ thuật" và "Khuyến nghị/ý
  kiến của tôi".
- **Nguồn tham chiếu:** mã gốc tại `Assets/Scripts/**` + wiki tiếng Việt tại
  `docs/wiki/vi/`. **Đọc file thật trước khi viết mỗi phase — không dựa vào trí nhớ.**

## B. Quy mô mục tiêu (ràng buộc thiết kế)

<!-- Với game client, "scale" không phải users/giây. Đây là các trục thật sự ràng
     buộc thiết kế của domain này. -->

| Chỉ số | Bản học (MVP) | Bản đầy đủ |
|--------|---------------|------------|
| Độ phủ hệ thống | Đủ chạy được từng phase | Toàn bộ hệ thống game gốc (full fidelity) |
| Nền tảng đích | Chạy trong Editor | Build desktop (+ WebGL tùy chọn) |
| Ngân sách khung hình | 60 fps trên máy tầm trung | 60 fps |
| Thời gian nạp | — | Vài giây (nhờ bake trước) |
| Dữ liệu địa lý | Tập rút gọn khi cần | 241 quốc gia + 8000+ thành phố thật |

> Chìa khóa khiến "dựng cả Trái Đất mà vẫn 60 fps" khả thi: **bake offline, nạp lúc
> chạy**. Việc nặng (sinh mesh địa hình, bản đồ tra cứu) làm **một lần** trong Editor
> rồi lưu ra file; game runtime chỉ nạp. Đây là ý tưởng tổ chức trung tâm của cả khóa.
>
> **KHÔNG làm** (over-engineering ở quy mô này): streaming terrain theo chunk,
> networking, hệ thống save phức tạp.

## C. Tech stack (đã khóa)

<!-- Không có mục datastore/broker/port — game client không có. -->

- **Engine:** Unity **2021.3.2f1** (LTS) — khớp `ProjectVersion.txt` bản gốc (ADR-0001).
- **Ngôn ngữ:** C# (+ HLSL cho compute shader từ Phase 5).
- **Render:** Built-in Render Pipeline (template 3D Core) — không URP/HDRP (ADR-0004).
- **Gói:** Input System (Phase 12), TextMeshPro (Phase 13), Newtonsoft Json (Phase 4).
- **VCS:** Git + `.gitignore` chuẩn Unity (ADR-0003).
- **IDE:** Rider / Visual Studio / VS Code (tùy học viên).

## D. Roadmap (đầy đủ 15 phase)

> **Lộ trình chi tiết:** `docs/course/phases/roadmap.{md,pdf}` — 21 trang. Mỗi phase
> có câu hỏi trung tâm, mục tiêu, khái niệm mới, thuật ngữ, sản phẩm bàn giao, phụ
> thuộc, độ khó (★), thời lượng, và file mã gốc đối chiếu. Có sơ đồ phụ thuộc và mô
> hình "4 chặng". **Nếu bảng dưới và tài liệu Lộ trình mâu thuẫn → dừng, đối chiếu lại.**

| # | Tên | Chặng | Trạng thái |
|---|-----|-------|-----------|
| — | **Lộ trình chi tiết** | — | ✅ DONE |
| 0 | Nền tảng & Môi trường | 1 | ⚠️ v1 xong — cần viết lại theo chuẩn Deep |
| 1 | Toán học địa lý & Kiểu dữ liệu | 1 | ⏳ |
| 2 | Máy trạng thái & Vòng đời game | 1 | ⏳ |
| 3 | Người chơi & Bay trên mặt cầu | 2 | ⏳ |
| 4 | Nạp dữ liệu thế giới (GeoJSON) | 2 | ⏳ |
| 5 | Sinh Terrain I — Compute & Lấy mẫu điểm | 3 | ⏳ |
| 6 | Sinh Terrain II — Tam giác hoá & Mesh | 3 | ⏳ |
| 7 | Sinh dữ liệu — Index quốc gia | 3 | ⏳ |
| 8 | Sinh dữ liệu — Đường viền & JFA | 3 | ⏳ |
| 9 | Tra cứu thế giới & Gói hàng | 3 | ⏳ |
| 10 | Hệ thống nhiệm vụ | 4 | ⏳ |
| 11 | Hệ Mặt Trời & Render | 4 | ⏳ |
| 12 | Input & Bản địa hóa | 4 | ⏳ |
| 13 | Giao diện, Menu & Địa cầu bản đồ | 4 | ⏳ |
| 14 | Hoàn thiện & Build | 4 | ⏳ |

## E. Quy ước biên soạn (không đổi qua các phase)
- **Định dạng:** PDF, dựng bằng `docs/course/tools/build_pdf.py` (venv tại
  `docs/course/tools/.venv`). Xem `docs/course/tools/HOW-TO-BUILD.md`.
- **Sơ đồ:** Mermaid. **Callout:** key/tip/warn/note.
- **ĐỘ SÂU: Deep** — mỗi phase bắt buộc có:
  1. **Từ điển thuật ngữ** (Anh → Việt → nghĩa đen → ví von → dùng ở đâu).
  2. **Bài toán & Giải pháp**: nêu bài toán → liệt kê mọi cách giải → bảng so sánh →
     chốt + vì sao.
  3. **Giải nghĩa jargon ngay lần đầu xuất hiện**.
  4. **Mổ xẻ code**: comment inline dày + phân tích từng dòng/khối bên dưới.
  5. **"Vì sao làm vậy"** cho mỗi bước hands-on.
  6. **Sai lầm thường gặp** + triệu chứng + cách sửa.
- **Cấu trúc phase:** Cover → Objectives → Từ điển → Theory → Bài toán & Giải pháp →
  Architecture/ADR → Hands-on (+ mổ xẻ) → Sai lầm thường gặp → Test/Deploy →
  SPEC/checklist → Summary/next.
- **Độ dài:** ~2000–2500 dòng/phase. Vượt → **tách N-a/N-b, không cắt nội dung**.
- **Kỹ thuật viết file:** tài liệu lớn dựng bằng **nhiều bước Write→Edit nối tiếp**
  (Write một phát >800 dòng gây lỗi). Không dùng shell heredoc cho Markdown tiếng
  Việt (hỏng byte UTF-8).
- **Workflow:** Lộ trình duyệt trước → một phase mỗi lần → chờ "done with Phase N".

## F. Sổ tên chuẩn (canonical names — phase sau KHÔNG được mâu thuẫn)

<!-- Với game client, "canonical names" là tên project/scene/namespace/thư mục —
     tương đương service name + port của backend. -->

- **Tên project Unity:** `GeoAdventures-Build`
- **Bố cục:** `Assets/Scripts/{Types, Game, Generation}`, `Assets/Scenes`,
  `Assets/Data`, `Assets/Graphics`, `Assets/Plugins`
- **Scene:** `Sandbox.unity` (nháp Phase 0); `Game.unity` (chơi chính, build index 0
  — `GameController.ExitToMainMenu()` gọi `LoadScene(0)`)
- **Namespace:** không namespace cho lớp lõi; `GeoGame.*` cho vài hệ thống (theo gốc,
  ví dụ `GeoGame.Quest`); `TerrainGeneration.*` cho pipeline sinh dữ liệu
- **Quy ước C#:** class `PascalCase`, tên file trùng tên class
- **Phiên bản Unity:** 2021.3.x LTS (ghi số hiệu chính xác học viên đã cài)
- **Tài liệu:** `docs/course/phases/{roadmap,phaseN}.{md,pdf}`; ADR ở
  `docs/course/adr/`; manifest tại `Course-Context_GeoAdventures.md` (gốc dự án)

## F-bis. Sổ ADR
- **ADR-0001** — Unity 2021.3.2f1 (LTS) thay vì bản mới nhất (khớp mã gốc).
- **ADR-0002** — Cấu trúc thư mục gom-theo-tính-năng (theo gốc).
- **ADR-0003** — Git + `.gitignore` chuẩn Unity ngay từ Phase 0.
- **ADR-0004** — Built-in Render Pipeline thay vì URP/HDRP (khớp gốc, giảm biến số).

## G. Tóm tắt & móc nối từng phase
- **Lộ trình (DONE):** `roadmap.pdf` (21 trang). Lập: mô hình **4 chặng** (Nền móng
  0–2 / Game sống dậy 3–4 / **Xưởng GPU** 5–9 / Thành game thật 10–14), sơ đồ phụ
  thuộc, thang ★, ước lượng 85–140 giờ, quy trình học 8 bước.
  - *Phase sau phải nhất quán với:* tên phase, thứ tự, câu hỏi trung tâm, danh sách
    thuật ngữ, sản phẩm bàn giao đã công bố trong Lộ trình.
- **Phase 0 (v1 xong — cần viết lại chuẩn Deep):** môi trường (Unity 2021.3 LTS, IDE,
  Git), cấu trúc thư mục, cài gói, cột mốc "quả cầu quay + health check".
  - *Đã lập:* vốn từ Unity nền tảng (GameObject/Component/Transform/MonoBehaviour/
    Scene/Prefab/ScriptableObject), hệ trục toạ độ (Y lên, `Vector3`, world/local),
    vòng đời `Awake/Start/Update`, `Time.deltaTime`.
  - *Phase sau phụ thuộc:* project + cấu trúc thư mục (mọi phase), `Vector3`/Transform
    (Phase 1, 3), Prefab (Phase 9, 10), ScriptableObject (Phase 4).
- **Cross-cutting cần nhớ:** Input System cài sớm (cần restart Editor). Ý
  "`position.normalized` = hướng lên tại điểm trên cầu" báo trước ở Phase 0, dùng
  chính thức ở Phase 1 & 3. Phase 5–6 là ★★★★★ — dành thời gian.

## H. Nguồn sự thật
- **Bản dựng của học viên:** project `GeoAdventures-Build` (repo Git riêng) — sự thật
  về code thực tế đã xây.
- **Tài liệu khóa:** `docs/course/phases/*.pdf` + `*.md`.
- **Bản gốc đối chiếu:** `Assets/Scripts/**` + wiki `docs/wiki/vi/`.
- Khi cần chi tiết chính xác: **đọc file thật**, không dựa vào trí nhớ mô hình.
