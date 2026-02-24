# Hướng dẫn dành cho giảng viên

Tài liệu này giúp bạn giảng dạy chương trình Agentic Content SEO một cách hiệu quả. Nội dung bao gồm khâu chuẩn bị, phân bổ thời gian, ghi chú từng bài học, và các lỗi thường gặp cần lưu ý.

## Tổng quan khóa học

- **21 bài học** chia thành 5 mô-đun
- **Đối tượng**: Nhân sự phi kỹ thuật (marketing, SEO, content) chưa có kinh nghiệm lập trình
- **Tổng thời lượng**: 12-14 giờ giảng dạy, lý tưởng nhất là chia thành 3 ngày
- **Mục tiêu**: Học viên hiểu cách hệ thống tạo nội dung bằng AI hoạt động, có thể chạy và đọc code, đồng thời sử dụng Claude Code để mở rộng và chỉnh sửa hệ thống

## Trước khi giảng dạy

### Thiết lập phòng học

1. **Cài đặt Python 3.12+** trên mọi máy
2. **Cài đặt Node.js 18+** cho phần frontend (giao diện web)
3. **Cài sẵn tất cả package**: `python -m pip install -r requirements.txt` và `cd output/frontend && npm install`
4. **Phân phối API key** — tạo file `.env` dùng chung hoặc cấp key riêng cho từng học viên
5. **Chạy thử ứng dụng web** trên ít nhất một máy: chạy `python output/backend/serve.py` và `cd output/frontend && npm run dev`, sau đó mở `http://localhost:5173` và gửi một prompt thử
6. **Mở Jupyter** và kiểm tra notebook load được: `jupyter notebook lessons_vi/`

### Kế hoạch chi phí API

| Hoạt động | Chi phí ước tính mỗi học viên |
|----------|------------------------------|
| Mô-đun 1 (bài 1-4) | $0 (không gọi API) |
| Mô-đun 2 (bài 5-7) | $0 (không gọi API) |
| Mô-đun 3 (bài 8-13) | $0.75-1.50 (gọi Sonnet, mini pipeline) |
| Mô-đun 4 (bài 14-17) | $2-5 (Sonnet agent, full team) |
| Mô-đun 5 (bài 18-21) | $0-3 (storage miễn phí, tạo bài viết tốn phí) |
| **Tổng mỗi học viên** | **$3-10** |

Với lớp 10 người: ngân sách khoảng $30-100 chi phí API.

**Mẹo kiểm soát chi phí:**
- Mô-đun 1 và 2 hoàn toàn miễn phí — không gọi API
- Bài 14 (Claude Code) và bài 21 (Mở rộng) cũng miễn phí (không chạy agent)
- Ở Mô-đun 3, yêu cầu học viên chỉ chạy mỗi cell demo một lần (không chạy lại)
- Ở bài 17 (xử lý hàng loạt), mỗi lần chạy team tốn khoảng $1-3. Nên cân nhắc demo một lần thay vì để mọi học viên tự chạy
- Mô-đun 5 bài 18-19 không cần tạo bài viết mới — truy vấn storage hoàn toàn miễn phí

### Kiến thức nền tảng của học viên

- Biết mở terminal
- Biết di chuyển giữa các thư mục trên máy tính
- Hiểu cơ bản SEO là gì (họ làm ở agency SEO nên điều này là đương nhiên)
- **Không yêu cầu kiến thức lập trình** — Mô-đun 1 dạy mọi thứ từ con số không

## Phân bổ thời gian gợi ý

### Ngày 1: Nền tảng (4-5 giờ)

| Phiên | Bài học | Thời lượng | Ghi chú |
|-------|---------|----------|-------|
| Sáng 1 | 01-02 | 90 phút | Cơ bản Python. Đi chậm. Cho học viên tự thử nghiệm. |
| Sáng 2 | 03-04 | 90 phút | Hàm + thiết lập. Kết thúc bằng kiểm tra thiết lập. |
| Chiều 1 | 05-06 | 90 phút | Cách LLM hoạt động + prompt. Lý thuyết nhưng rất quan trọng. |
| Chiều 2 | 07 | 40 phút | Model và cách chọn lựa. Kết thúc Mô-đun 2 với bài tập tính chi phí. |

**Điểm kiểm tra**: Cuối Ngày 1, mọi học viên cần hiểu token, prompt, và đánh đổi giữa các model, đồng thời đã thiết lập API key thành công.

### Ngày 2: Xây dựng (4-5 giờ)

| Phiên | Bài học | Thời lượng | Ghi chú |
|-------|---------|----------|-------|
| Sáng 1 | 08-09 | 60 phút | Agent đầu tiên. Khoảnh khắc "wow" khi agent phản hồi. |
| Sáng 2 | 10-11 | 75 phút | Structured output + gọi API. Khái niệm khó hơn. |
| Chiều 1 | 12-13 | 80 phút | Chaining + mini pipeline. Bài cầu nối then chốt. |
| Chiều 2 | 14-15 | 90 phút | Claude Code + Content Writer. Code production thực tế. |

**Điểm kiểm tra**: Cuối Ngày 2, mọi học viên cần đã chạy thành công `agent.run()`, thấy mini pipeline hoạt động, và hiểu Content Writer agent.

### Ngày 3: Sản phẩm + Tổng kết (4-5 giờ)

| Phiên | Bài học | Thời lượng | Ghi chú |
|-------|---------|----------|-------|
| Sáng 1 | 16-17 | 75 phút | Image Finder + Team & xử lý hàng loạt. |
| Sáng 2 | 18 | 45 phút | Local storage. Thực hành chu trình save/list/get/update. |
| Chiều 1 | 19-20 | 60 phút | Cách mọi thứ kết nối + giao diện web. Demo trực tiếp. |
| Chiều 2 | 21 | 60 phút | Mở rộng sản phẩm + vibecoding. |
| Tổng kết | — | 30 phút | Duyệt qua toàn bộ cấu trúc thư mục `output/`. Hỏi đáp. |

## Ghi chú giảng dạy từng bài

### Bài 01: Hello Python

- **Tốc độ**: Rất chậm. Đây là lần đầu tiên nhiều học viên viết code.
- **Khoảnh khắc quan trọng**: Khi `print("Hello!")` chạy thành công. Cho họ thời gian để cảm nhận.
- **Lỗi thường gặp**: Học viên gõ `Print` (chữ P hoa) — Python phân biệt hoa thường.

### Bài 02: List và dictionary

- **Tốc độ**: Trung bình. List khá trực quan, dict cần nhiều thời gian hơn.
- **Khoảnh khắc quan trọng**: Ví dụ cấu trúc lồng nhau. Dừng lại và vẽ trên bảng trắng.
- **Lỗi thường gặp**: Thiếu dấu phẩy trong dict gây ra `SyntaxError`.

### Bài 03: Hàm (function)

- **Tốc độ**: Chậm. Hàm là khái niệm khó nhất trong Mô-đun 1.
- **Lỗi thường gặp**: Lỗi thụt lề và quên `return`.

### Bài 04: Thiết lập và package

- **Quan trọng**: Kết thúc bài này bằng kiểm tra thiết lập. Yêu cầu mọi học viên chạy cell kiểm tra. Không chuyển sang Mô-đun 2 cho đến khi mọi người đều pass cả 3 bước kiểm tra.
- **Bảo mật**: Nhấn mạnh không bao giờ commit `.env` lên git.

### Bài 05-07: Hiểu về AI (Mô-đun 2)

- **Không gọi API** — hoàn toàn miễn phí. Học viên có thể thoải mái thử nghiệm.
- **Khoảnh khắc quan trọng**: Bài tập ước tính token (giúp chi phí trở nên cụ thể), demo temperature, đánh đổi giữa các model.
- **Cần dạy**: Hallucination — cực kỳ quan trọng với đội ngũ SEO tạo nội dung.

### Bài 08: Agent đầu tiên

- **Khoảnh khắc quan trọng**: Phản hồi đầu tiên từ `agent.run()`. Học viên sẽ kinh ngạc khi 5 dòng code tạo ra một AI agent.
- **Lỗi thường gặp**: Lỗi API key nếu `load_dotenv()` không tìm thấy file `.env`.

### Bài 09: Agent với tools

- **Khoảnh khắc quan trọng**: So sánh agent có và không có tools. Chạy cả hai trực tiếp.
- **Kết nối với Mô-đun 2**: "Ở Bài 5, chúng ta đã học về knowledge cutoff. Tools giải quyết vấn đề đó."
- **Chi phí**: Mỗi `agent.run()` với DataForSEO tốn khoảng $0.02-0.05.

### Bài 10: Structured output

- **Tốc độ**: CHẬM. Đây là bài khó nhất trong Mô-đun 3.
- **Khoảnh khắc quan trọng**: Khi `outline.title` trả về đúng chuỗi title. Đây là khoảnh khắc nhận ra "tại sao structured output quan trọng".

### Bài 11: Gọi API

- **Nội dung**: Cách agent giao tiếp với Claude ở tầng bên dưới (HTTP request, JSON payload).

### Bài 12-13: Chaining + mini pipeline

- **Bài cầu nối then chốt**: Các bài này kết nối agent đơn giản với pattern code production.
- **Pattern `sys.path.insert`** được giới thiệu ở đây. Giải thích ngắn gọn: "Dòng này cho Python biết tìm file code production ở đâu."

### Bài 14: Cơ bản Claude Code

- **Không gọi API** — học viên đọc file dự án và viết prompt dạng chuỗi.
- **Khoảnh khắc quan trọng**: Đọc file CLAUDE.md thật. "Đây là system prompt cho Claude Code."

### Bài 15: Content Writer

- **Code production đầu tiên**. Học viên xem Content Writer agent thực từ `output/backend/agents/content_writer.py`.
- **Nội dung**: DataForSEO search + storage tools phối hợp trong một agent.

### Bài 16: Image Finder và AIO Analyzer

- **Hai agent trong một bài** — Image Finder (tùy chọn, cần DataForSEO) và AIO Analyzer (phân tích Google AI Overview).
- **Pattern quan trọng**: Factory function (`build_image_finder()` trả về `None` nếu không có API key), pattern đọc-sửa-ghi (đọc bài viết → chèn hình → lưu).
- **Fallback an toàn**: Image Finder là tùy chọn. Không có DataForSEO key = team bỏ qua. Không có lỗi.
- **Chi phí**: $0 nếu không có DataForSEO key (chỉ đọc code production). ~$0.10 nếu chạy AIO analyzer.

### Bài 17: Team & xử lý hàng loạt

- **Khoảnh khắc quan trọng**: Tạo bài viết hàng loạt — nhiều bài song song.
- **Chi phí**: Khoảng $1-3 mỗi lần chạy. Nên cân nhắc demo một lần.

### Bài 18: Local file storage

- **An toàn để thử nghiệm**: Tạo/đọc/cập nhật bài viết trong `content/` hoàn toàn miễn phí.
- **Khoảnh khắc quan trọng**: Khi học viên thấy bài viết của mình xuất hiện dưới dạng file `.md`.

### Bài 19: Cách mọi thứ kết nối

- **Bài ngắn** — truy vết cách một yêu cầu (request) đi qua hệ thống.
- **Demo trực tiếp**: Duyệt qua cấu trúc dự án.

### Bài 20: Giao diện web

- **Demo trực tiếp**: Chạy ứng dụng web (hai terminal) và cho học viên xem streaming response.
- **Dạy vibecoding**: Cách Claude Code tạo `serve.py` từ team definition.

### Bài 21: Mở rộng sản phẩm

- **Bài tổng kết**. Học viên thiết kế agent mới (Proofreader) và truy vết qua tất cả các bước.
- **Không gọi API** — học viên lên kế hoạch và xác minh mà không cần chạy agent.
- **Phần vibecoding**: Cách Claude Code xây dựng React frontend.

## Điểm kiểm tra

### Sau Mô-đun 1 (bài 4)
Yêu cầu học viên: tạo một biến, một list, và một dict; viết một hàm; cho xem trạng thái API key từ cell kiểm tra ở bài 4.

### Sau Mô-đun 2 (bài 7)
Yêu cầu học viên: giải thích token, context window, knowledge cutoff; viết một prompt có đủ Role/Task/Constraints/Examples.

### Sau Mô-đun 3 (bài 13)
Yêu cầu học viên: giải thích agent, tools, structured output; truy cập dữ liệu lồng nhau từ schema; mô tả luồng hoạt động của mini pipeline.

### Sau Mô-đun 4 (bài 17)
Yêu cầu học viên: giải thích Content Writer làm gì; mô tả cách Team ủy thác nhiệm vụ (delegate); giải thích xử lý hàng loạt (batch processing).

### Sau Mô-đun 5 (bài 21)
Yêu cầu học viên: sử dụng giao diện web; giải thích cách các thành phần kết nối; kể tên 3 file trong `output/backend/` và mô tả chức năng của mỗi file.

## Sau khóa học: bước tiếp theo cho học viên

Sau khi hoàn thành khóa học, học viên có thể:

1. **Tùy chỉnh instructions của agent** — Sửa `output/backend/agents/content_writer.py` để thay đổi phong cách viết
2. **Thêm target keyword** — Cung cấp keyword khi tạo bài viết qua giao diện web
3. **Chạy tạo bài hàng loạt** — Yêu cầu team tạo nhiều bài viết cùng lúc
4. **Giám sát chất lượng output** — Review bài viết đã tạo trong `content/`

Cho học viên muốn đi sâu hơn (sử dụng Claude Code):
1. Thêm tool mới cho agent (ví dụ: Google Search Console API)
2. Thêm proofreading agent vào team
3. Thêm dịch thuật để tạo nội dung đa ngôn ngữ
4. Mở rộng frontend với tính năng mới
