# Hướng dẫn dành cho học viên

Chào mừng bạn đến với khoá học Agentic Content SEO. Tài liệu này cung cấp mọi thứ bạn cần biết trước khi mở notebook đầu tiên.

## Bạn sẽ xây dựng được gì

Sau 20 bài học, bạn sẽ hiểu cách một pipeline tạo nội dung SEO bằng AI hoạt động — từ khâu nghiên cứu chủ đề đến khi tạo ra một bài viết hoàn chỉnh. Bạn sẽ có khả năng chạy, chỉnh sửa, giải thích từng thành phần, và sử dụng các công cụ AI như Claude Code để mở rộng hệ thống.

## Yêu cầu trước khi bắt đầu

### Kỹ năng (không cần biết lập trình)

- Biết gõ lệnh trong terminal (copy-paste)
- Hiểu SEO ở mức cơ bản (keywords, thứ hạng, bài viết)
- Biết mở và tìm file trên máy tính

### Phần mềm

| Công cụ | Mục đích | Cách kiểm tra |
|---------|----------|----------------|
| Python 3.12+ | Chạy toàn bộ code | `python --version` trong terminal |
| Jupyter Notebook | Chạy các bài học | Cài qua requirements.txt |
| Trình soạn code | Để đọc code production sau này | Khuyên dùng VS Code |
| Git (tuỳ chọn) | Theo dõi thay đổi code | `git --version` |

### API key

| Key | Cần từ khi nào | Chi phí |
|-----|----------------|---------|
| `ANTHROPIC_API_KEY` | Mô-đun 3+ (từ bài 8) | Trả theo dùng. ~$0.50-2 mỗi bài viết |
| `XAI_API_KEY` | Mô-đun 4+ (từ bài 14) | Trả theo dùng. ~$0.50-1 mỗi bài viết |
| `FREEPIK_API_KEY` | Tuỳ chọn (làm giàu hình ảnh) | Có gói miễn phí |
| `DATA_FOR_SEO_API_KEY` | Tuỳ chọn (làm giàu hình ảnh) | Có bản dùng thử miễn phí |

Bạn KHÔNG cần API key nào cho Mô-đun 1-2 (bài 1-7).

## Thiết lập (chỉ cần làm một lần)

### Bước 1: Cài đặt các package

Mở terminal trong thư mục dự án và chạy:

```bash
python -m pip install -r requirements.txt
```

### Bước 2: Tạo file `.env`

Tạo file tên `.env` ở thư mục gốc của dự án (cùng thư mục với `README.md`):

```
ANTHROPIC_API_KEY=your_key_here
XAI_API_KEY=your_key_here
```

Hỏi giảng viên để lấy API key nếu bạn chưa có.

### Bước 3: Kiểm tra thiết lập

Mở terminal và chạy:

```bash
python -c "import agno; print('agno OK')"
python -c "import anthropic; print('anthropic OK')"
python -c "from dotenv import load_dotenv; load_dotenv(); import os; key=os.getenv('ANTHROPIC_API_KEY',''); print('API key found' if len(key)>5 else 'WARNING: API key not found -- check your .env file')"
```

Cả ba lệnh đều phải in ra OK / "API key found". Nếu không, hãy hỏi giảng viên trước khi tiếp tục.

### Bước 4: Mở Jupyter

```bash
jupyter notebook lessons_vi/
```

Bắt đầu với `01-python-co-ban/01_hello_python.ipynb`.

## Cấu trúc khoá học

### Mô-đun 1: Nền tảng Python (bài 1-4)

Không cần API key. Không cần internet. Thoải mái thử nghiệm.

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 01 | Biến, chuỗi, f-string | 30 phút |
| 02 | List, dictionary, vòng lặp | 45 phút |
| 03 | Hàm (function) | 45 phút |
| 04 | Package, .env, thiết lập môi trường | 30 phút |

Sau Mô-đun 1 bạn có thể: đọc code Python, hiểu biến/list/dict/function, và nắm được các package trong dự án liên kết với nhau ra sao.

### Mô-đun 2: Hiểu về AI (bài 5-7)

Không cần API key. Các bài học lý thuyết kết hợp bài tập Python.

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 05 | Cách LLM hoạt động (token, context, dự đoán) | 45 phút |
| 06 | Prompt và ngữ cảnh (system prompt vs user prompt) | 45 phút |
| 07 | Các model và cách lựa chọn (đánh đổi tốc độ/chi phí/chất lượng) | 40 phút |

Sau Mô-đun 2 bạn có thể: giải thích cách LLM hoạt động, viết prompt hiệu quả, và hiểu vì sao các model khác nhau được chọn cho các tác vụ khác nhau.

### Mô-đun 3: Xây dựng Agent (bài 8-12)

Cần `ANTHROPIC_API_KEY`. Mỗi cell gọi agent tốn một khoản nhỏ (~$0.01-0.05).

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 08 | Tạo agent đầu tiên | 30 phút |
| 09 | Trang bị tools cho agent (tìm kiếm web) | 30 phút |
| 10 | Structured output (Pydantic) | 45 phút |
| 11 | Nối chuỗi agent thành pipeline | 30 phút |
| 12 | Xây mini pipeline (cầu nối sang production) | 50 phút |

Sau Mô-đun 3 bạn có thể: tạo agent AI, trang bị tools, bắt agent trả dữ liệu có cấu trúc, nối chuỗi chúng lại, và xây dựng một pipeline 3 agent hoàn chỉnh với nested schema.

### Mô-đun 4: Pipeline SEO thực tế (bài 13-15)

Cần `ANTHROPIC_API_KEY` + `XAI_API_KEY`. Chạy một pipeline đầy đủ tốn khoảng ~$1-3 tiền API.

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 13 | Agent Research + Outline (code thật) | 45 phút |
| 14 | Agent Writer + Image (code thật) | 45 phút |
| 15 | Chạy toàn bộ pipeline end-to-end | 30 phút |

Sau Mô-đun 4 bạn có thể: chạy pipeline tạo nội dung đầy đủ và hiểu từng agent đóng góp vai trò gì.

### Mô-đun 5: Sản phẩm hoàn chỉnh (bài 16-18)

Cần cả hai API key để tạo bài viết. Các lệnh xem trạng thái/lịch sử thì miễn phí.

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 16 | Database và SQL cơ bản | 45 phút |
| 17 | Giao diện dòng lệnh (CLI) | 20 phút |
| 18 | Giao diện chat (Agno Team) | 30 phút |

Sau Mô-đun 5 bạn có thể: sử dụng sản phẩm hoàn chỉnh qua CLI hoặc chat, và hiểu cách các thành phần kết nối với nhau.

### Mô-đun 6: Phát triển cùng AI (bài 19-20)

Không cần API key. Lý thuyết kết hợp hướng dẫn thực hành.

| Bài học | Chủ đề | Thời lượng |
|---------|--------|------------|
| 19 | Cơ bản về Claude Code (cài đặt, CLAUDE.md, quy trình làm việc) | 45 phút |
| 20 | Mở rộng sản phẩm (thêm agent kiểm duyệt nội dung) | 50 phút |

Sau Mô-đun 6 bạn có thể: sử dụng Claude Code để mở rộng và chỉnh sửa sản phẩm, kiểm chứng code do AI sinh ra bằng kiến thức từ tất cả bài học trước, và điều hướng AI xây tính năng cho mình.

## Bảng thuật ngữ chính

Các thuật ngữ này xuất hiện xuyên suốt khoá học. Quay lại đây bất cứ khi nào bạn gặp thuật ngữ lạ.

### Thuật ngữ Python

- **Variable (Biến)** — Một vùng chứa dữ liệu có tên. `name = "Viet"` tạo một biến tên `name`.
- **String (Chuỗi)** — Dữ liệu dạng văn bản, luôn nằm trong dấu nháy: `"hello"`.
- **List (Danh sách)** — Một tập hợp có thứ tự: `["a", "b", "c"]`. Truy cập phần tử theo vị trí: `list[0]`.
- **Dictionary / dict (Từ điển)** — Cặp key-value: `{"name": "Viet", "age": 20}`. Truy cập theo key: `dict["name"]`.
- **Function (Hàm)** — Khối code tái sử dụng. `def greet(name):` định nghĩa hàm, `greet("Viet")` gọi hàm.
- **Import** — Đưa code bên ngoài vào file của bạn: `from agno.agent import Agent`.
- **Package (Gói thư viện)** — Code có sẵn mà bạn cài đặt và import (ví dụ: `agno`, `anthropic`).

### Thuật ngữ định dạng dữ liệu

- **JSON** — Định dạng văn bản cho dữ liệu có cấu trúc. Trông giống dict và list trong Python:
  ```json
  {"title": "SEO Guide", "keywords": ["seo", "ranking"]}
  ```
  Được dùng khi các agent trao đổi dữ liệu. Bạn sẽ thấy `.model_dump_json()` — hàm chuyển đổi object Python sang văn bản JSON.

- **Markdown** — Định dạng văn bản cho tài liệu có format. Các bài viết của chúng ta được viết bằng Markdown:
  ```markdown
  # Main Title        (H1 heading)
  ## Section           (H2 heading)
  **bold text**        (bold)
  - bullet point       (list item)
  ![alt](url)          (image)
  ```
  File có đuôi `.md` là file Markdown. Thư mục `content/` chứa các bài viết được tạo dưới dạng Markdown.

- **CSV** — Comma-separated values (giá trị phân cách bằng dấu phẩy). Định dạng bảng tính đơn giản:
  ```
  topic,keywords
  SEO Guide 2026,"seo,ranking"
  ```
  Dùng cho việc tạo bài viết hàng loạt (batch).

### Thuật ngữ AI/LLM

- **LLM (Large Language Model)** — Mô hình ngôn ngữ lớn. "Bộ não" AI dự đoán văn bản. Claude, GPT, và Grok đều là LLM.
- **Token** — Đơn vị xử lý của LLM (~¾ từ tiếng Anh). Chi phí API được tính theo token.
- **Context window (Cửa sổ ngữ cảnh)** — Kích thước tối đa đầu vào + đầu ra mà LLM xử lý được trong một lần. Claude Sonnet có 200K token.
- **Knowledge cutoff (Ngày cắt dữ liệu)** — Ngày kết thúc dữ liệu huấn luyện. LLM "mù" với mọi thông tin sau ngày này.
- **Temperature (Nhiệt độ)** — Điều chỉnh tính sáng tạo: 0 = tập trung/xác định, 1 = sáng tạo/đa dạng.
- **Hallucination (Ảo giác)** — Khi LLM sinh ra thông tin sai nhưng tự tin như thật. Luôn phải kiểm chứng.
- **Embedding** — Văn bản được chuyển thành số để nắm bắt ngữ nghĩa. Hỗ trợ tìm kiếm ngữ nghĩa và đo độ tương đồng.
- **Prompt** — Tất cả nội dung bạn gửi cho LLM. Prompt tốt hơn = kết quả tốt hơn.
- **System prompt** — Chỉ dẫn cố định định hình hành vi agent (phần `instructions` của agent).
- **Prompt engineering** — Kỹ năng viết prompt hiệu quả. Kỹ năng SEO thời đại mới.

### Thuật ngữ Agent

- **Agent** — Chương trình sử dụng model AI để suy nghĩ và hành động. Có tên, model, instructions, và tuỳ chọn tools.
- **Model** — Bộ não AI. Chúng ta dùng Claude Sonnet (nhanh, tốt với tools) và Grok-4 (viết tốt).
- **Instructions (Chỉ dẫn)** — Các hướng dẫn định hình cách agent hoạt động. Giống như mô tả công việc.
- **Tools (Công cụ)** — Khả năng bạn trao cho agent (tìm kiếm web, tìm ảnh, gọi API). Agent tự quyết khi nào sử dụng.
- **Structured output / output_schema** — Buộc agent trả dữ liệu theo định dạng cụ thể (không phải văn bản tự do).
- **Pipeline** — Nhiều agent chạy tuần tự, mỗi agent truyền kết quả cho agent tiếp theo.
- **Team (Đội nhóm)** — Nhiều agent phối hợp dưới sự điều phối của một leader phân công nhiệm vụ (dùng trong giao diện chat).

### Thuật ngữ phát triển phần mềm

- **Claude Code** — Trợ lý AI dạng CLI của Anthropic, đọc codebase và thực hiện thay đổi.
- **CLAUDE.md** — File chỉ dẫn cho Claude Code (giống `instructions` của agent).
- **MCP (Model Context Protocol)** — Kết nối Claude Code với các nguồn tài liệu bên ngoài.

### Thuật ngữ SEO (cho người chưa biết SEO)

- **SEO (Search Engine Optimization)** — Tối ưu hoá công cụ tìm kiếm. Làm cho trang web xếp hạng cao hơn trên Google.
- **Keywords (Từ khoá)** — Các từ/cụm từ mà người dùng tìm kiếm trên Google. Một bài viết nhắm đến các từ khoá cụ thể.
- **Meta description (Mô tả meta)** — Đoạn tóm tắt 1-2 câu hiển thị trên kết quả tìm kiếm Google (tối đa 160 ký tự).
- **On-page SEO (SEO on-page)** — Các tối ưu thực hiện trực tiếp trên trang web (tiêu đề, heading, nội dung, hình ảnh).
- **Backlinks (Liên kết ngược)** — Liên kết từ website khác trỏ về website của bạn. Một yếu tố xếp hạng quan trọng.

## Cách chạy từng cell

Trong Jupyter Notebook:
- **Shift + Enter** — Chạy cell hiện tại và chuyển sang cell tiếp theo
- **Ctrl + Enter** — Chạy cell hiện tại và giữ nguyên vị trí
- **Các cell chạy theo thứ tự** — Luôn chạy từ trên xuống dưới. Nếu bạn bỏ qua một cell, các cell sau có thể bị lỗi.

## Bí quyết học hiệu quả

1. **Chạy mọi cell**, kể cả khi bạn nghĩ mình đã hiểu. Nhìn kết quả đầu ra giúp xây dựng trực giác lập trình.
2. **Đọc thông báo lỗi** trước khi nhờ trợ giúp. Lỗi Python thường nói chính xác vấn đề là gì (sai tên biến, thiếu package, v.v.).
3. **Thoải mái thử nghiệm ở Mô-đun 1-2**. Thay đổi giá trị, phá vỡ mọi thứ, xem chuyện gì xảy ra. Không tốn tiền API.
4. **Cẩn thận chi phí API ở Mô-đun 3-5**. Mỗi lệnh `agent.run()` đều tốn tiền. Đừng chạy cell trong vòng lặp hay chạy lại không cần thiết.
5. **Đừng học thuộc cú pháp**. Tập trung hiểu *mỗi thành phần làm gì*. Cách viết cụ thể thì lúc nào cũng tra lại được.
6. **Mô-đun 2 là lý thuyết nhưng cực kỳ quan trọng**. Nó giải thích *vì sao* pipeline được thiết kế như vậy. Đừng bỏ qua.

## Sau khi hoàn thành tất cả 20 bài học

Giờ bạn đã hiểu toàn bộ hệ thống. Dưới đây là cách các bài học liên kết với các file production trong `output/`:

| Bài học | Xây dựng hướng tới | File production |
|---------|---------------------|-----------------|
| 05-07 | Hiểu LLM, prompt, lựa chọn model | (Định hình mọi quyết định thiết kế) |
| 08-09 | Tạo agent, tools | `output/agents/builders.py` |
| 10, 13 | Pydantic schema | `output/agents/schemas.py` |
| 11-12, 13-15 | Nối chuỗi agent, pipeline | `output/pipeline.py` |
| 16 | Tầng database | `output/db.py` |
| 17 | Giao diện CLI | `output/cli.py` |
| 18 | Giao diện chat, workspace tools | `output/chat.py`, `output/workspace_tools.py` |
| 19-20 | Phát triển cùng AI | `CLAUDE.md` (bản thiết kế cho Claude Code) |

Để bắt đầu sử dụng sản phẩm:

```bash
# Create an article
python output/cli.py create "Your topic here"

# Check status
python output/cli.py status

# Or use the chat interface
python output/chat.py
```

Để mở rộng sản phẩm, dùng Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
cd your-project-folder
claude
```

## Xử lý sự cố

| Vấn đề | Giải pháp |
|--------|-----------|
| `ModuleNotFoundError: No module named 'agno'` | Chạy `python -m pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'ddgs'` | Chạy `python -m pip install ddgs` |
| Lỗi API key / xác thực thất bại | Kiểm tra file `.env`. Đảm bảo không có dấu cách quanh `=` và không có dấu nháy quanh giá trị key. |
| Không tìm thấy lệnh `python` | Thử `python3`, hoặc kiểm tra Python đã được cài và nằm trong PATH chưa. |
| Jupyter không khởi động được | Chạy `python -m pip install jupyter` rồi `jupyter notebook lessons_vi/` |
| Cell chạy mãi không dừng (>2 phút) | Agent có thể đang chờ tìm kiếm web. Nhấn nút dừng (biểu tượng hình vuông) và thử lại. DuckDuckGo đôi khi bị giới hạn tần suất. |
| `Error: status -> error` khi tạo bài viết | Kiểm tra `python output/cli.py status --article <id>` để xem thông báo lỗi. Thường do vấn đề API key. |
| `sys.path.insert` không hoạt động | Đảm bảo bạn đang chạy notebook từ đúng thư mục. Jupyter cần được khởi chạy từ thư mục gốc dự án. |
