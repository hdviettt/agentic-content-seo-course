# Hướng Dẫn Dành Cho Giảng Viên

Tài liệu này giúp bạn giảng dạy chương trình Agentic Content SEO một cách hiệu quả. Nội dung bao gồm khâu chuẩn bị, phân bổ thời gian, ghi chú từng bài học, và các lỗi thường gặp cần lưu ý.

## Tổng quan khóa học

- **20 bài học** chia thành 6 mô-đun
- **Đối tượng**: Nhân sự phi kỹ thuật (marketing, SEO, content) chưa có kinh nghiệm lập trình
- **Tổng thời lượng**: 12-14 giờ giảng dạy, lý tưởng nhất là chia thành 3 ngày
- **Mục tiêu**: Học viên hiểu cách pipeline tạo nội dung bằng AI hoạt động, có thể chạy và đọc code, đồng thời sử dụng Claude Code để mở rộng và chỉnh sửa hệ thống

## Trước khi giảng dạy

### Thiết lập phòng học

1. **Cài đặt Python 3.12+** trên mọi máy
2. **Cài sẵn tất cả package**: `python -m pip install -r requirements.txt`
3. **Phân phối API key** — tạo file `.env` dùng chung hoặc cấp key riêng cho từng học viên
4. **Thiết lập Airtable**: mỗi học viên cần `AIRTABLE_PAT` trong `.env`, sau đó chạy `python output/tools/airtable.py` để tạo các bảng
5. **Chạy thử toàn bộ pipeline** trên ít nhất một máy: chạy `python output/chat.py` và yêu cầu tạo bài viết thử — để xác nhận mọi API key và Airtable đều hoạt động
5. **Mở Jupyter** và kiểm tra notebook load được: `jupyter notebook lessons_vi/`

### Kế hoạch chi phí API

| Hoạt động | Chi phí ước tính mỗi học viên |
|----------|------------------------------|
| Mô-đun 1 (bài 1-4) | $0 (không gọi API) |
| Mô-đun 2 (bài 5-7) | $0 (không gọi API) |
| Mô-đun 3 (bài 8-12) | $0.75-1.50 (gọi Sonnet, mini pipeline) |
| Mô-đun 4 (bài 13-15) | $2-5 (Sonnet + Grok, full pipeline) |
| Mô-đun 5 (bài 16-18) | $0-3 (DB miễn phí, tạo bài viết tốn phí) |
| Mô-đun 6 (bài 19-20) | $0 (không gọi API) |
| **Tổng mỗi học viên** | **$3-10** |

Với lớp 10 người: ngân sách khoảng $30-100 chi phí API. Mô-đun 4 tốn kém nhất vì bài 15 chạy toàn bộ pipeline 4 agent.

**Mẹo kiểm soát chi phí:**
- Mô-đun 1, 2 và 6 hoàn toàn miễn phí — không gọi API
- Ở Mô-đun 3, yêu cầu học viên chỉ chạy mỗi cell demo một lần (không chạy lại)
- Ở bài 14, cell writer agent mất 1-2 phút và tốn khoảng $0.50-1 mỗi lần chạy. Nên cân nhắc demo trực tiếp thay vì để mọi học viên tự chạy
- Ở bài 15, mỗi lần chạy full pipeline tốn khoảng $1-3. Bạn có thể demo một lần rồi để học viên đọc kết quả
- Mô-đun 5 bài 17-18 không cần tạo bài viết mới — truy vấn trạng thái và lịch sử hoàn toàn miễn phí

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
| Sáng 2 | 10-11 | 75 phút | Structured output + chuỗi agent. Khái niệm khó hơn. |
| Chiều 1 | 12 | 50 phút | Mini pipeline. Bài học cầu nối then chốt. |
| Chiều 2 | 13-14 | 90 phút | Agent thực tế. So sánh với những gì đã xây ở Mô-đun 3. |

**Điểm kiểm tra**: Cuối Ngày 2, mọi học viên cần đã chạy thành công `agent.run()`, thấy pipeline 3 agent hoạt động, và hiểu nested schema.

### Ngày 3: Sản phẩm + Tổng kết (4-5 giờ)

| Phiên | Bài học | Thời lượng | Ghi chú |
|-------|---------|----------|-------|
| Sáng 1 | 15 | 45 phút | Full pipeline. Có thể demo một lần thay vì để tất cả học viên chạy. |
| Sáng 2 | 16 | 60 phút | Database. Thực hành Airtable API, an toàn và miễn phí. |
| Chiều 1 | 17-18 | 60 phút | Cách mọi thứ kết nối + chat. Demo trực tiếp. Cho học viên thử giao diện chat. |
| Chiều 2 | 19-20 | 90 phút | Cơ bản Claude Code + mở rộng sản phẩm. |
| Tổng kết | — | 30 phút | Duyệt qua toàn bộ cấu trúc thư mục `output/`. Hỏi đáp. |

## Ghi chú giảng dạy từng bài

### Bài học 01: Hello Python

- **Tốc độ**: Rất chậm. Đây là lần đầu tiên nhiều học viên viết code.
- **Khoảnh khắc quan trọng**: Khi `print("Hello!")` chạy thành công. Cho họ thời gian để cảm nhận.
- **Lỗi thường gặp**: Học viên gõ `Print` (chữ P hoa) — Python phân biệt hoa thường.
- **Bài tập**: Bài tập nhỏ cuối bài rất quan trọng. Đi vòng quanh lớp và hỗ trợ.
- **Mẹo demo**: Cho thấy khi thay đổi biến rồi chạy lại cell thì kết quả cập nhật. Điều này dạy mô hình tư duy "code chạy từ trên xuống dưới".

### Bài học 02: List và Dictionary

- **Tốc độ**: Trung bình. List khá trực quan, dict cần nhiều thời gian hơn.
- **Khoảnh khắc quan trọng**: Ví dụ cấu trúc lồng nhau (bài viết với các section). Dừng lại và vẽ trên bảng trắng.
- **Lỗi thường gặp**: Học viên nhầm `list[0]` (phần tử đầu) với `list[1]`. Nhấn mạnh đánh số từ 0.
- **Lỗi thường gặp**: Thiếu dấu phẩy trong dict gây ra `SyntaxError`. Hướng dẫn cách đọc thông báo lỗi.
- **Không có bài tập trong bài này** — có thể giao miệng: "Tạo một dict mô tả bài viết yêu thích của bạn, gồm title, author, và list 3 keyword."

### Bài học 03: Hàm (Function)

- **Tốc độ**: Chậm. Hàm là khái niệm khó nhất trong Mô-đun 1.
- **Khoảnh khắc quan trọng**: `format_seo_title()` — khi học viên thấy rằng một hàm có thể được gọi với nhiều input khác nhau và cho ra output khác nhau.
- **Lỗi thường gặp**: Lỗi thụt lề. Giải thích rằng Python dùng dấu cách (không phải tab) và code bên trong hàm phải được thụt lề.
- **Lỗi thường gặp**: Quên `return` — hàm chạy nhưng không trả về gì.
- **Bài tập**: Bài tập cuối bài được thiết kế tốt. Cho học viên tự vật lộn 5-10 phút trước khi chỉ lời giải.

**Lời giải bài tập** (để bạn tham khảo):
```python
def create_seo_title(keyword):
    return f"{keyword.title()} - The Complete A-to-Z Guide [{2026}]"

print(create_seo_title("content marketing"))
print(create_seo_title("link building"))
print(create_seo_title("technical seo"))
```

### Bài học 04: Thiết lập và Package

- **Tốc độ**: Nhanh phần lý thuyết, chậm phần thiết lập thực tế.
- **Khoảnh khắc quan trọng**: Khi `os.getenv("ANTHROPIC_API_KEY")` trả về key thực (đã che). Điều này kết nối file .env với code thực tế.
- **Quan trọng**: Kết thúc bài này bằng kiểm tra thiết lập. Yêu cầu mọi học viên chạy lệnh kiểm tra từ Hướng Dẫn Dành Cho Học Viên. Không chuyển sang Mô-đun 2 cho đến khi mọi người đều thiết lập thành công.
- **Bảo mật**: Nhấn mạnh không bao giờ commit `.env` lên git. Cho họ xem file `.gitignore`.

### Bài học 05: Cách LLM Hoạt Động (MỚI)

- **Tốc độ**: Trung bình. Lý thuyết nhưng hấp dẫn.
- **Không gọi API** — hoàn toàn miễn phí. Học viên có thể thoải mái thử nghiệm.
- **Khoảnh khắc quan trọng**: (1) Bài tập ước tính token — giúp chi phí trở nên cụ thể. (2) Demo temperature — học viên thấy tính ngẫu nhiên ảnh hưởng đến output như thế nào.
- **Cần dạy**: Hallucination. Điều này cực kỳ quan trọng với đội ngũ SEO tạo nội dung. Nhấn mạnh: "Pipeline đặt bài viết ở trạng thái 'review', không phải 'published' — đây là thiết kế có chủ đích."
- **Kết nối**: Khi thảo luận về knowledge cutoff, giới thiệu trước Bài 09: "Đây chính xác là lý do chúng ta cho agent công cụ tìm kiếm DuckDuckGo."
- **Câu hỏi thường gặp**: "Nó thực sự hoạt động như vậy sao?" Trả lời: "Đây là phiên bản đơn giản hóa, nhưng ý tưởng cốt lõi là đúng — prediction, token, và context window là thật."

### Bài học 06: Prompt và Ngữ Cảnh (MỚI)

- **Tốc độ**: Trung bình-nhanh. Rất thực tiễn.
- **Không gọi API** — học viên xây dựng prompt dưới dạng chuỗi Python.
- **Khoảnh khắc quan trọng**: So sánh prompt tệ vs prompt tốt. Yêu cầu học viên diễn đạt TẠI SAO prompt tốt lại tốt hơn.
- **Cần dạy**: 4 thành phần (Role, Task, Constraints, Examples). Viết lên bảng. Học viên sẽ tham chiếu mô hình này trong mọi bài học sau.
- **Bài tập**: Học viên tạo prompt template riêng. Khuyến khích template cho công việc thực tế (meta description, tạo title, v.v.).
- **Kết nối với agent**: "Khi bạn thấy `instructions=[...]` trong mô-đun tiếp theo, giờ bạn đã biết đó chính LÀ system prompt."

### Bài học 07: Model và Cách Chọn Lựa (MỚI)

- **Tốc độ**: Trung bình. Bài tập tính chi phí rất thu hút.
- **Không gọi API** — lý thuyết kèm bài tập code.
- **Khoảnh khắc quan trọng**: Sơ đồ ràng buộc kiến trúc — khi học viên thấy rằng Grok không thể kết hợp tools + output_schema, và chính hạn chế duy nhất này đã định hình toàn bộ kiến trúc pipeline.
- **Cần dạy**: Embedding được giới thiệu ở mức khái niệm. Không đi sâu — chỉ gieo mầm cho việc học sau này.
- **Bài tập**: Bài tập chọn model rất phù hợp để thảo luận. Cho học viên tranh luận trước khi tiết lộ đáp án gợi ý.
- **Chuyển tiếp**: "Giờ bạn đã hiểu TẠI SAO mọi thứ hoạt động theo cách này. Ở Mô-đun 3, bạn sẽ XÂY DỰNG nó."

### Bài học 08: Agent Đầu Tiên

- **Tốc độ**: Trung bình. Code đơn giản nhưng khái niệm mới.
- **Khoảnh khắc quan trọng**: Phản hồi đầu tiên từ `agent.run()`. Học viên sẽ kinh ngạc khi 5 dòng code tạo ra một AI phản hồi thông minh.
- **Mẹo demo**: Chạy song song hai agent khác nhau (bullet point vs giải thích đơn giản). Điều này làm `instructions` trở nên cụ thể — cùng câu hỏi, hành vi khác nhau dựa trên instructions.
- **Kết nối với Mô-đun 2**: "Nhớ system prompt từ Bài 6 không? `instructions` CHÍNH LÀ system prompt."
- **Lỗi thường gặp**: Lỗi API key. Nếu `load_dotenv()` không tìm thấy file `.env`, agent sẽ lỗi âm thầm hoặc báo lỗi xác thực khó hiểu. Đảm bảo notebook của học viên tìm được file `.env` (nó phải ở thư mục gốc dự án, và Jupyter phải được khởi chạy từ thư mục gốc).
- **Bài tập**: Tạo agent với vai trò tùy chỉnh. Cho học viên chọn gì đó liên quan đến công việc thực tế — điều này tạo sự gắn kết cá nhân và dễ nhớ hơn.

### Bài học 09: Agent với Tools

- **Tốc độ**: Trung bình.
- **Khoảnh khắc quan trọng**: So sánh agent có và không có tools. Chạy cả hai trực tiếp và thảo luận sự khác biệt.
- **Kết nối với Mô-đun 2**: "Ở Bài 5, chúng ta đã học về knowledge cutoff. Tools giải quyết vấn đề đó."
- **Lỗi thường gặp**: DuckDuckGo giới hạn tốc độ. Nếu quá nhiều học viên tìm kiếm cùng lúc, một số sẽ gặp lỗi. Giải pháp: phân chia lượt chạy hoặc chia lớp làm hai — nửa xem, nửa chạy.
- **Chi phí**: Mỗi `agent.run()` với DuckDuckGo tốn khoảng $0.02-0.05 (token Sonnet + tìm kiếm).
- **Bài tập**: Tìm kiếm thông tin về công ty mình bằng agent. Học viên kiểm tra kết quả có chính xác không — dạy cách đánh giá phản biện output của AI.

### Bài học 10: Structured Output

- **Tốc độ**: CHẬM. Đây là bài khó nhất trong Mô-đun 3.
- **Giới thiệu JSON**: Notebook có phần giải thích JSON. Nếu cần, minh họa thêm trên bảng trắng.
- **Khoảnh khắc quan trọng**: Khi `outline.title` trả về đúng chuỗi title, và `outline.sections[0]` trả về đúng section đầu tiên. Đây là khoảnh khắc nhận ra "tại sao structured output quan trọng".
- **Kết nối với Mô-đun 2**: "Ở Bài 6, chúng ta đã nói về việc chỉ định format output trong prompt. `output_schema` tự động hóa điều này và đảm bảo format."
- **Lỗi thường gặp**: Học viên nhầm `response.content` (đối tượng Pydantic) với chuỗi. Cho thấy `type(response.content)` trả về `ArticleOutline`, không phải `str`.
- **Bài tập**: Sửa schema để thêm field mới. Điều này dạy rằng schema không phải phép màu — bạn kiểm soát những gì agent trả về.

### Bài học 11: Chuỗi Agent (Chaining)

- **Tốc độ**: Trung bình. Khái niệm đơn giản nhưng mạnh mẽ.
- **Khoảnh khắc quan trọng**: Khi học viên thấy rằng `research.content` (output của Agent 1) được truyền trực tiếp vào `writer.run()` (input của Agent 2). f-string chính là "chất keo" kết nối.
- **Cần dạy**: Dừng lại ở sơ đồ pipeline và kết nối với những gì họ sẽ xây tiếp theo.
- **Bài tập**: Thêm agent thứ ba (Editor) vào chuỗi. Điều này trực tiếp giới thiệu trước mini pipeline ở Bài 12.

### Bài học 12: Xây Dựng Mini Pipeline (MỚI)

- **Tốc độ**: Trung bình-chậm. Đây là bài cầu nối then chốt.
- **Khoảnh khắc quan trọng**: Khi học viên truy cập `outline.sections[0].heading` và `outline.sections[0].key_points` — truy cập dữ liệu lồng nhau. Đây là kỹ năng cần thiết cho Mô-đun 4.
- **Cần dạy**: Xây dựng schema theo từng bước (SimpleOutline -> Section + DetailedOutline). Vẽ cấu trúc lồng nhau trên bảng.
- **Quan trọng**: Pattern `sys.path.insert` được giới thiệu ở đây. Giải thích ngắn gọn: "Dòng này cho Python biết tìm file code production ở đâu." Học viên sẽ gặp lại nó ở Mô-đun 4.
- **Chi phí**: Khoảng $0.20-0.40 cho cả ba agent. Mất 1-2 phút.
- **Bảng so sánh**: Dành thời gian cho bảng so sánh mini vs real pipeline. Điều này đặt kỳ vọng cho Mô-đun 4.

### Bài học 13: Agent Nghiên Cứu và Dàn Ý

- **Tốc độ**: Trung bình-chậm. Đây là code "sản phẩm thực" đầu tiên.
- **Quan trọng**: Phần "Có Gì Khác Biệt" từ chương trình cũ đã được thay thế — bài cầu nối (12) đã xử lý khoảng cách đó. Bài 13 mở đầu bằng cách kết nối với pattern mini pipeline mà học viên đã thực hành.
- **Khoảnh khắc quan trọng**: Schema `ContentOutline` đầy đủ với `OutlineSection` lồng nhau. Học viên nên nhận ra pattern từ Bài 12.
- **Chi phí**: Chạy cell này tốn khoảng $0.10-0.20 (Sonnet cho nghiên cứu + dàn ý).
- **Cần thời gian**: Cell chạy thử mất 30-60 giây. Báo trước cho học viên.

### Bài học 14: Agent Viết Bài và Hình Ảnh

- **Tốc độ**: Trung bình.
- **Khoảnh khắc quan trọng**: Giải thích TẠI SAO dùng các model khác nhau. Học viên đã hiểu các đánh đổi từ Bài 7 — giờ họ thấy nó được áp dụng thực tế.
- **Hạn chế của Grok**: Học viên đã biết điều này từ Bài 7. Nhấn mạnh lại: "Nhớ bảng so sánh khả năng không? Đó là lý do writer dùng Grok."
- **Chi phí**: Cell writer tốn khoảng $0.50-1 mỗi lần chạy (Grok cho bài viết dài). Nên cân nhắc demo một lần thay vì để tất cả học viên chạy.
- **Agent hình ảnh**: Vì đa số học viên không có image API key, bài 14 chỉ trình bày khái niệm. Điều này hoàn toàn ổn.

### Bài học 15: Full Pipeline

- **Tốc độ**: Nhanh cho phần nội dung bài học. Chậm cho phần thảo luận "ngấm dần".
- **Khoảnh khắc giảng dạy then chốt**: Cho xem sơ đồ pipeline (queued -> researching -> ... -> review) và kết nối với mọi thứ đã học.
- **Chi phí**: Khoảng $1-3 mỗi lần chạy full pipeline. **Khuyến nghị mạnh mẽ nên demo một lần** thay vì để tất cả học viên chạy.
- **Sau khi chạy**: Dùng giao diện chat (`python output/chat.py`) để kiểm tra trạng thái bài viết. Sau đó mở file `.md` đã tạo. Điều này kết nối notebook với sản phẩm thực.
- **sys.path.insert**: Học viên đã thấy pattern này ở Bài 12. Chỉ cần lưu ý: "Cùng pattern như mini pipeline."

### Bài học 16: Database (Airtable)

- **Tốc độ**: Chậm. Khái niệm database hoàn toàn mới với đa số học viên.
- **An toàn để thử nghiệm**: Airtable có giao diện trực quan nên học viên có thể nhìn thấy dữ liệu ngay lập tức. Khuyến khích thử nghiệm.
- **Khoảnh khắc quan trọng**: Khi họ tạo bài viết và thấy nó xuất hiện trong Airtable. Kết nối: "Đây là những gì giao diện chat làm phía sau khi bạn yêu cầu tạo hoặc lọc bài viết."
- **Cần dạy**: Khái niệm record ID (chuỗi như "recABC123") và cách các field Airtable ánh xạ sang Python dict.
- **Nửa sau** sử dụng module `tools/airtable.py` thực. Điều này tạo bản ghi thực trong Airtable base của họ.

### Bài học 17: Cách Mọi Thứ Kết Nối

- **Tốc độ**: Nhanh. Đây là bài ngắn.
- **Thông điệp chính**: "Giao diện chat gọi cùng `pipeline.py` và `tools/airtable.py` mà bạn đã hiểu. Bài này cho thấy cách các thành phần kết nối với nhau."
- **Demo trực tiếp**: Duyệt qua cấu trúc dự án và cho thấy cách `chat.py` gọi `tools/workspace.py` rồi gọi `pipeline.py` rồi gọi `tools/airtable.py`.
- **Không tạo bài viết** trong lớp trừ khi muốn tốn phí API. Cho xem luồng hoạt động nhưng giải thích chi phí.

### Bài học 18: Giao Diện Chat

- **Tốc độ**: Trung bình.
- **Demo trực tiếp**: Chạy `python output/chat.py` trong terminal. Gõ tin nhắn và cho học viên xem quá trình phân công của team diễn ra trực tiếp.
- **Điểm giảng dạy chính**: Khái niệm Team — leader phân công cho các thành viên chuyên môn. Kết nối với quản lý trong thực tế.
- **Thực hành**: Cho học viên gọi trực tiếp `list_all_articles()` và `get_article_details()` trong notebook để hiểu các thành viên team thực sự làm gì.
- **Chuyển tiếp sang Mô-đun 6**: Dùng phần "Hoàn thành Mô-đun 5" để giới thiệu trước Claude Code. Tạo hứng thú: "Bạn đã hiểu toàn bộ hệ thống. Giờ bạn sẽ học cách mở rộng nó."

### Bài học 19: Cơ Bản Claude Code (MỚI)

- **Tốc độ**: Trung bình. Lý thuyết nhưng rất thực tiễn.
- **Không gọi API** — học viên đọc file dự án và viết prompt dưới dạng chuỗi.
- **Khoảnh khắc quan trọng**: Đọc file `CLAUDE.md` thực tế. Học viên nhận ra: "Đây là system prompt cho Claude Code, giống như `instructions` là system prompt cho agent."
- **Cần dạy**: Quy trình 5 bước (Tìm hiểu -> Lên kế hoạch -> Triển khai -> Xác minh -> Lặp lại). Kết nối với pattern pipeline.
- **Phần MCP**: Giữ ở mức khái niệm. Điểm mấu chốt là "MCP cho Claude Code quyền truy cập tài liệu, giống như đưa cho nó sách tham khảo."
- **Bài tập**: Học viên viết prompt Claude Code cho 3 kịch bản. Chấm điểm dựa trên tính cụ thể (đường dẫn file, vấn đề rõ ràng, ràng buộc).

### Bài học 20: Mở Rộng Sản Phẩm (MỚI)

- **Tốc độ**: Trung bình-chậm. Đây là bài tổng kết.
- **Không gọi API** — học viên truy vết những gì Claude Code sẽ thực hiện.
- **Khoảnh khắc quan trọng**: Checklist xác minh. Học viên áp dụng kiến thức từ TẤT CẢ các mô-đun để xác minh implementation của proofreading agent. Đây là khoảnh khắc "aha" — mọi thứ kết nối lại.
- **Cần dạy**: Hướng dẫn qua phần xác minh schema (Cell 7). Học viên thấy rằng Pydantic schema hoạt động mà không cần chạy agent nào — nó chỉ là Python thuần.
- **Bảng ý tưởng mở rộng**: Cho học viên thảo luận ý tưởng nào hấp dẫn họ. Một số có thể muốn thử với Claude Code sau khóa học.
- **Kết thúc**: Dành thời gian cho phần tổng kết khóa học. Cho học viên nhìn lại hành trình từ `print("Hello")` đến hiểu toàn bộ AI pipeline.

## Điểm kiểm tra — xác nhận học viên đang theo kịp

### Sau Mô-đun 1 (bài 4)

Yêu cầu học viên:
1. Tạo một biến, một list, và một dict
2. Viết một hàm nhận topic bài viết và trả về title đã format
3. Cho xem trạng thái API key (đã che) từ cell kiểm tra ở bài 4

Nếu học viên không làm được, họ cần thêm thời gian với Mô-đun 1 trước khi tiếp tục.

### Sau Mô-đun 2 (bài 7)

Yêu cầu học viên:
1. Giải thích bằng lời riêng: token là gì, context window là gì, knowledge cutoff là gì?
2. Viết một prompt có đủ 4 thành phần (Role, Task, Constraints, Examples) cho một tác vụ SEO
3. Giải thích tại sao writer agent dùng Grok thay vì Claude (ràng buộc khả năng của model)

Nếu học viên không giải thích được token và prompt, hãy quay lại Bài 5-6 trước khi chuyển sang Mô-đun 3.

### Sau Mô-đun 3 (bài 12)

Yêu cầu học viên:
1. Giải thích bằng lời riêng: agent là gì, tools là gì, structured output là gì?
2. Truy cập dữ liệu lồng nhau từ schema: "Làm sao lấy heading của section đầu tiên từ outline?"
3. Giải thích sự khác biệt giữa `list[str]` và `list[Section]`

### Sau Mô-đun 4 (bài 15)

Yêu cầu học viên:
1. Vẽ pipeline trên giấy: 4 agent, mỗi agent làm gì, dữ liệu nào truyền giữa chúng
2. Giải thích tại sao writer dùng Grok thay vì Claude (kết nối Bài 7 với Bài 14)
3. Mô tả điều gì xảy ra trong database ở mỗi bước pipeline

### Sau Mô-đun 5 (bài 18)

Yêu cầu học viên:
1. Dùng giao diện chat để kiểm tra trạng thái bài viết và giải thích kết quả
2. Giải thích cách giao diện chat phân công nhiệm vụ cho các thành viên team chuyên biệt
3. Kể tên 3 file trong `output/` và mô tả chức năng của mỗi file

### Sau Mô-đun 6 (bài 20)

Yêu cầu học viên:
1. Mô tả quy trình phát triển AI 5 bước
2. Viết một prompt Claude Code để thêm tính năng đơn giản (ví dụ: thay đổi giọng văn của writer)
3. Cho một schema, xác minh: model được chọn đúng chưa? Có tuân theo pattern hiện tại không?

## Ghi chú chương trình

Các chủ đề sau được đề cập trong notebook. Hãy nhấn mạnh thêm bằng lời khi cần:

- **Token và context window** — Bài 05 giải thích các khái niệm này. Tham chiếu khi thảo luận chi phí API.
- **Prompt engineering** — Bài 06 đề cập kỹ lưỡng. Tham chiếu pattern 4 thành phần (Role, Task, Constraints, Examples) mỗi khi xem xét instructions của agent.
- **Đánh đổi giữa các model** — Bài 07 xây dựng khung quyết định. Tham chiếu ở Bài 13-14 khi học viên thấy cách chọn model thực tế.
- **JSON** — Bài 10 có phần giới thiệu JSON. Vẽ trên bảng trắng để minh họa thêm.
- **Markdown** — Bài 14 có phần giới thiệu Markdown. Cho xem file `.md` và bản render song song.
- **Xử lý lỗi (try/except)** — Bài 15 có giải thích đầy đủ. Hướng dẫn trên màn hình.
- **Cầu nối nested schema** — Bài 12 giới thiệu nested schema trước code production ở Bài 13. Điều này loại bỏ vách đứng độ phức tạp của chương trình cũ.
- **Cầu nối code production** — Bài 18 có phần "Đọc Code Production" ánh xạ bài học với các file trong `output/`.
- **Kiểm tra thiết lập** — Bài 04 kết thúc với cell kiểm tra 4 bước. Không chuyển bài cho đến khi tất cả học viên đều pass.
- **Cảnh báo chi phí** — Bài 08, 12, 13, 14, 15 có ghi chú chi phí trước các cell tốn kém.

## Điều chỉnh khóa học

### Workshop ngắn (nửa ngày, khoảng 4 giờ)

Bỏ qua Mô-đun 1 nếu học viên có bất kỳ nền tảng lập trình nào. Bắt đầu từ bài 5.

Tập trung vào: bài 5, 6 (lướt nhanh), 7, 8, 10, 11, 12 (lướt nhanh), 15 (demo).

Bỏ qua: bài 1-4, 9, 13, 14, 16, 17, 18, 19, 20.

### Workshop 2 ngày (khoảng 8-10 giờ)

Gộp Mô-đun 1-2 vào Ngày 1 (bỏ bài tập, chỉ demo). Gộp Mô-đun 3-5 vào Ngày 2 (demo pipeline và database). Bỏ Mô-đun 6 nhưng đề cập Claude Code trong phần tổng kết.

### Cho lập trình viên có kinh nghiệm

Bỏ hoàn toàn Mô-đun 1-2. Bắt đầu từ Mô-đun 3. Dành thêm thời gian review code — duyệt chi tiết qua các file trong `output/`. Mô-đun 6 vẫn có giá trị.

### Cho đội ngũ không phải SEO

Thay thuật ngữ chuyên ngành SEO bằng lĩnh vực của họ. Cấu trúc pipeline (nghiên cứu -> dàn ý -> viết -> bổ sung) áp dụng được cho mọi quy trình tạo nội dung.

## Sau khóa học: bước tiếp theo cho học viên

Sau khi hoàn thành khóa học, học viên có thể:

1. **Tùy chỉnh instructions của agent** — Sửa `output/agents/writer.py` để thay đổi phong cách viết, hoặc bất kỳ file agent nào trong `output/agents/` để điều chỉnh hành vi
2. **Thêm target keyword** — Cung cấp keyword khi tạo bài viết qua giao diện chat
3. **Chạy tạo bài hàng loạt** — Tạo file `topics.csv` và xử lý nhiều bài viết qua giao diện chat
4. **Giám sát chất lượng output** — Dùng giao diện chat để kiểm tra trạng thái và review bài viết đã tạo trong `content/`

Cho học viên muốn đi sâu hơn (sử dụng Claude Code):
1. Thêm tool mới cho agent (ví dụ: Google Search Console API)
2. Sửa pipeline để thêm bước proofreading
3. Thay đổi model của writer hoặc thử model khác cho từng agent
4. Thêm dịch thuật để tạo nội dung đa ngôn ngữ
5. Xây dựng web dashboard cho workspace
