# 📘 Hướng Dẫn Sử Dụng Chi Tiết (Usage Guide)

## 📋 Mục Lục
- [Cấu Trúc Lệnh CLI](#cấu-trúc-lệnh-cli)
- [Quy Trình Hoạt Động](#quy-trình-hoạt-động)
- [Các Cách Sử Dụng](#các-cách-sử-dụng)
- [Ví Dụ Chi Tiết](#ví-dụ-chi-tiết)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Cấu Trúc Lệnh CLI

### Cú Pháp Cơ Bản

```bash
python cli.py <input_file> <output_file> [OPTIONS]
```

### Các Thành Phần

```
┌─────────────┬──────────────┬─────────────┬───────────────┐
│   Script    │  Input File  │ Output File │    Options    │
└─────────────┴──────────────┴─────────────┴───────────────┘
  python cli.py  input.txt     output.txt    --provider ...
```

### Tham Số Bắt Buộc

| Tham Số | Vị Trí | Mô Tả | Ví Dụ |
|---------|--------|-------|-------|
| `input_file` | 1 | File nguồn cần dịch | `book.pdf`, `novel.txt` |
| `output_file` | 2 | File đích lưu bản dịch | `book_vi.pdf`, `novel_vi.txt` |

### Tham Số Tùy Chọn (Options)

#### 🤖 Provider & Model

```bash
--provider {openai,anthropic,google,cohere,groq,deepseek}
    LLM provider sử dụng
    Mặc định: openai

--api-key YOUR_API_KEY
    API key cho provider
    Bắt buộc nếu không dùng config file hoặc env variable

--model MODEL_NAME
    Tên model cụ thể
    Mặc định: tùy provider
```

#### 🌍 Ngôn Ngữ

```bash
--source-lang {english,chinese,russian}
    Ngôn ngữ nguồn
    Mặc định: english

--target-lang LANGUAGE
    Ngôn ngữ đích
    Mặc định: vietnamese
```

#### ⚙️ Xử Lý

```bash
--max-workers NUMBER
    Số luồng dịch song song
    Mặc định: 5
    Khuyến nghị: 3-10

--max-chunk-size NUMBER
    Kích thước chunk tối đa (chars)
    Mặc định: 3000
    Khuyến nghị: 2000-5000

--min-chunk-size NUMBER
    Kích thước chunk tối thiểu (chars)
    Mặc định: 500
    Khuyến nghị: 300-1000
```

#### 📝 Config & Logging

```bash
--config CONFIG_FILE
    Đường dẫn file cấu hình JSON
    Ví dụ: --config config.json

--verbose, -v
    Hiển thị log chi tiết
    Hữu ích cho debugging

--log-file LOG_PATH
    Lưu log ra file
    Ví dụ: --log-file translation.log
```

#### 🛠️ Utilities

```bash
--create-config
    Tạo file config mẫu
    python cli.py --create-config
```

---

## 🔄 Quy Trình Hoạt Động

### Sơ Đồ Tổng Quan

```
┌─────────────────────────────────────────────────────────────┐
│                    BẮT ĐẦU DỊCH SÁCH                        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BƯỚC 1: ĐỌC FILE                                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │ • Tự động detect format (TXT/PDF/EPUB/DOCX)       │    │
│  │ • Đọc nội dung với encoding phù hợp                │    │
│  │ • Chuyển đổi sang text thuần                      │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BƯỚC 2: CHIA ĐOẠN THÔNG MINH (Intelligent Chunking)        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Phát hiện cấu trúc:                             │    │
│  │    • Chapters (Chapter 1, Chương 1, 第一章)       │    │
│  │    • Sections (headings, titles)                   │    │
│  │    • Paragraphs (double line breaks)               │    │
│  │                                                     │    │
│  │ 2. Tạo split points theo thứ tự ưu tiên:          │    │
│  │    Priority 1: Chapters                            │    │
│  │    Priority 2: Sections                            │    │
│  │    Priority 3: Paragraphs                          │    │
│  │    Priority 4: Line breaks                         │    │
│  │                                                     │    │
│  │ 3. Chia chunks:                                    │    │
│  │    • Kích thước: min_chunk_size ↔ max_chunk_size │    │
│  │    • Không cắt ngang chapters/sections             │    │
│  │    • Ưu tiên paragraph boundaries                  │    │
│  │                                                     │    │
│  │ 4. Thêm context:                                   │    │
│  │    • Mỗi chunk nhận context từ chunk trước        │    │
│  │    • Giúp LLM hiểu ngữ cảnh, giữ mạch văn        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  📊 Kết quả: 150,000 chars → 50 chunks × ~3000 chars       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BƯỚC 3: DỊCH SONG SONG (Parallel Translation)              │
│  ┌────────────────────────────────────────────────────┐    │
│  │        ThreadPoolExecutor (5 workers)              │    │
│  │                                                     │    │
│  │  Worker 1  →  [Chunk 1] → LLM API → [Dịch 1]     │    │
│  │  Worker 2  →  [Chunk 2] → LLM API → [Dịch 2]     │    │
│  │  Worker 3  →  [Chunk 3] → LLM API → [Dịch 3]     │    │
│  │  Worker 4  →  [Chunk 4] → LLM API → [Dịch 4]     │    │
│  │  Worker 5  →  [Chunk 5] → LLM API → [Dịch 5]     │    │
│  │                                                     │    │
│  │  Mỗi worker:                                       │    │
│  │  1. Lấy chunk từ queue                            │    │
│  │  2. Tạo translation prompt với context            │    │
│  │  3. Gọi LLM API                                   │    │
│  │  4. Nhận kết quả                                  │    │
│  │  5. Lưu translation                               │    │
│  │  6. Update progress bar                           │    │
│  │  7. Lặp lại cho chunk tiếp theo                  │    │
│  │                                                     │    │
│  │  ⚡ Tốc độ: 5x nhanh hơn dịch tuần tự            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  🔄 Error Handling:                                         │
│  • Retry tự động nếu API fail                              │
│  • Max 3 retries với exponential backoff                    │
│  • Log errors để debug                                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BƯỚC 4: GHÉP ĐOẠN THÔNG MINH (Smart Merging)              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Clean translations:                             │    │
│  │    • Xóa LLM artifacts ("Here is translation...")  │    │
│  │    • Xóa markdown code blocks nếu có              │    │
│  │    • Trim whitespace                               │    │
│  │                                                     │    │
│  │ 2. Determine spacing:                              │    │
│  │    • Chapters: 3 line breaks                       │    │
│  │    • Sections: 2 line breaks                       │    │
│  │    • Paragraphs: 2 line breaks                     │    │
│  │    • Normal text: 1 line break                     │    │
│  │                                                     │    │
│  │ 3. Merge chunks:                                   │    │
│  │    [Dịch 1] + spacing + [Dịch 2] + spacing + ...  │    │
│  │                                                     │    │
│  │ 4. Final cleanup:                                  │    │
│  │    • Remove excessive line breaks (>3)             │    │
│  │    • Remove trailing spaces                        │    │
│  │    • Ensure single newline at end                  │    │
│  │                                                     │    │
│  │ 5. Validation:                                     │    │
│  │    • Check length ratio (0.5x - 2x original)      │    │
│  │    • Check line breaks preservation                │    │
│  │    • Verify has content                            │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  BƯỚC 5: GHI FILE                                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │ • Detect output format từ extension                │    │
│  │ • Convert text về format phù hợp                   │    │
│  │ • Ghi file với encoding UTF-8                      │    │
│  │ • Bảo toàn formatting của format đó                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  ✅ HOÀN TẤT - HIỂN THỊ THỐNG KÊ                           │
│  • Total chunks: 50                                         │
│  • Successful: 50                                           │
│  • Failed: 0                                                │
│  • Duration: 180 seconds                                    │
│  • Speed: 833 chars/sec                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎓 Các Cách Sử Dụng

### Cách 1: Với Config File (Khuyến Nghị)

**Ưu điểm**: Gọn, an toàn, dễ quản lý nhiều config

```bash
# Bước 1: Tạo config
python cli.py --create-config

# Bước 2: Sửa config.json với API key của bạn

# Bước 3: Dịch
python cli.py input.pdf output.pdf --config config.json
```

### Cách 2: Trực Tiếp CLI

**Ưu điểm**: Linh hoạt, override nhanh

```bash
python cli.py input.txt output.txt \
  --provider google \
  --api-key AIzaSy... \
  --model gemini-1.5-flash \
  --source-lang english \
  --max-workers 7
```

### Cách 3: Environment Variables (An Toàn Nhất)

**Ưu điểm**: Không lưu API key trong file, an toàn

```bash
# Setup (1 lần)
export GOOGLE_API_KEY="AIzaSy..."

# Sử dụng (nhiều lần)
python cli.py input.txt output.txt --provider google
python cli.py book1.pdf book1_vi.pdf --provider google
python cli.py book2.epub book2_vi.epub --provider google
```

### Cách 4: Kết Hợp (Linh Hoạt Nhất)

```bash
# Config file cho settings mặc định
# CLI options để override khi cần

python cli.py input.txt output.txt \
  --config config.json \
  --max-workers 10 \
  --verbose
```

---

## 💡 Ví Dụ Chi Tiết

### Ví Dụ 1: Dịch Sách Tiếng Anh → Tiếng Việt (Cơ Bản)

```bash
# Với OpenAI GPT-4o
python cli.py english_book.txt vietnamese_book.txt \
  --provider openai \
  --api-key sk-... \
  --model gpt-4o

# Output sẽ hiện:
# Translating english_book.txt -> vietnamese_book.txt
# Language: english -> vietnamese
# Step 1: Chunking text...
# Chunk statistics: {'total_chunks': 45, 'avg_length': 2800, ...}
# Step 2: Translating 45 chunks with 5 workers...
# Translating chunks: 100%|████████| 45/45 [03:24<00:00, 4.53s/chunk]
# Step 3: Merging translations...
# ==================================================
# TRANSLATION COMPLETE!
# Total chunks: 45
# Successful: 45
# Failed: 0
# Duration: 204.52 seconds
# Speed: 735.67 chars/sec
# Output: vietnamese_book.txt
# ==================================================
```

### Ví Dụ 2: Dịch PDF Tiếng Trung → Tiếng Việt

```bash
# Với Google Gemini Flash (nhanh + rẻ)
python cli.py chinese_novel.pdf vietnamese_novel.pdf \
  --provider google \
  --api-key AIzaSy... \
  --model gemini-1.5-flash \
  --source-lang chinese \
  --max-workers 7

# PDF sẽ được:
# 1. Đọc và extract text
# 2. Dịch từng chunk
# 3. Tạo lại PDF với văn bản tiếng Việt
```

### Ví Dụ 3: Dịch EPUB với Groq (Nhanh Nhất)

```bash
# Groq miễn phí và cực nhanh!
python cli.py fantasy_novel.epub fantasy_novel_vi.epub \
  --provider groq \
  --api-key gsk_... \
  --model llama-3.1-70b-versatile \
  --max-workers 15

# Với Groq có thể dùng nhiều workers (15-20)
# vì API cực nhanh
```

### Ví Dụ 4: Dịch với Config File

```bash
# 1. Tạo config
cat > config.json << EOF
{
  "llm_provider": "google",
  "model": "gemini-1.5-pro",
  "api_key": "AIzaSy...",
  "max_workers": 5,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
EOF

# 2. Dịch nhiều file
python cli.py book1.txt book1_vi.txt --config config.json
python cli.py book2.pdf book2_vi.pdf --config config.json
python cli.py book3.epub book3_vi.epub --config config.json
```

### Ví Dụ 5: Dịch Sách Dài (100+ trang)

```bash
# Optimize cho sách dài
python cli.py long_novel.txt long_novel_vi.txt \
  --provider groq \
  --api-key gsk_... \
  --max-workers 15 \
  --max-chunk-size 4000 \
  --context-size 500 \
  --verbose \
  --log-file translation.log

# Settings này:
# • max-workers 15: Dịch 15 chunks cùng lúc
# • max-chunk-size 4000: Chunks lớn hơn (ít chunks hơn)
# • context-size 500: Context dài hơn (mạch văn tốt hơn)
# • verbose: Xem chi tiết quá trình
# • log-file: Lưu log để review sau
```

### Ví Dụ 6: Dịch với Claude (Chất Lượng Cao)

```bash
# Claude 3.5 Sonnet - chất lượng tốt nhất
python cli.py literary_work.txt literary_work_vi.txt \
  --provider anthropic \
  --api-key sk-ant-... \
  --model claude-3-5-sonnet-20241022 \
  --temperature 0.2 \
  --max-workers 5

# Temperature 0.2: Dịch nhất quán, ít biến đổi
# Phù hợp cho văn học, sách chuyên môn
```

### Ví Dụ 7: Dịch Sách Tiếng Nga

```bash
python cli.py russian_book.txt vietnamese_book.txt \
  --provider openai \
  --api-key sk-... \
  --source-lang russian \
  --model gpt-4o
```

### Ví Dụ 8: Batch Processing (Dịch Nhiều File)

```bash
# Script để dịch tất cả file .txt trong thư mục

#!/bin/bash
for file in books/*.txt; do
    output="translated/$(basename "$file" .txt)_vi.txt"
    echo "Translating $file -> $output"
    python cli.py "$file" "$output" --config config.json
done
```

### Ví Dụ 9: Dịch với Custom Chunking

```bash
# Sách có chapters dài → chunks lớn
python cli.py textbook.pdf textbook_vi.pdf \
  --config config.json \
  --max-chunk-size 5000 \
  --min-chunk-size 1000

# Sách có đoạn ngắn → chunks nhỏ
python cli.py poetry.txt poetry_vi.txt \
  --config config.json \
  --max-chunk-size 1500 \
  --min-chunk-size 300
```

### Ví Dụ 10: Debug Mode

```bash
# Khi gặp lỗi, dùng verbose để debug
python cli.py problem_book.txt output.txt \
  --config config.json \
  --verbose \
  --log-file debug.log

# Xem log
cat debug.log
```

---

## 🔍 Chi Tiết Từng Bước

### Bước 1: Đọc File

```python
# Hệ thống tự động:
1. Detect format từ extension (.txt, .pdf, .epub, .docx)
2. Chọn handler phù hợp
3. Đọc nội dung:
   - TXT: Thử nhiều encodings (utf-8, gb2312, big5, ...)
   - PDF: Dùng pdfplumber hoặc PyPDF2
   - EPUB: Parse HTML, extract text
   - DOCX: Đọc paragraphs và tables
4. Chuyển về text thuần
```

### Bước 2: Chunking

```python
# Ví dụ văn bản:
"""
Chapter 1: Introduction

This is the first paragraph.
It contains important information.

This is the second paragraph.
More details here.

Chapter 2: Details

Content of chapter 2.
"""

# Được chia thành chunks:
Chunk 0 (Chapter):
  text: "Chapter 1: Introduction\n\nThis is the first paragraph..."
  type: "chapter"
  context: ""

Chunk 1 (Paragraph):
  text: "This is the second paragraph.\nMore details here."
  type: "paragraph"
  context: "...first paragraph. It contains important information."

Chunk 2 (Chapter):
  text: "Chapter 2: Details\n\nContent of chapter 2."
  type: "chapter"
  context: "...More details here."
```

### Bước 3: Translation

```python
# Mỗi chunk được dịch với prompt:
"""
Bạn là một dịch giả chuyên nghiệp. Nhiệm vụ của bạn là dịch văn bản từ tiếng Anh sang tiếng Việt.

YÊU CẦU QUAN TRỌNG:
1. GIỮ NGUYÊN CẤU TRÚC: Bảo toàn hoàn toàn định dạng, xuống dòng, khoảng trắng
2. DUY TRÌ MẠCH VĂN: Đảm bảo văn phong tự nhiên, liền mạch với ngữ cảnh
3. CHÍNH XÁC NỘI DUNG: Dịch sát nghĩa, không bỏ sót thông tin

ĐOẠN TRƯỚC ĐÓ (để hiểu ngữ cảnh):
...first paragraph. It contains important information.

VĂN BẢN CẦN DỊCH:
This is the second paragraph.
More details here.

BẢN DỊCH TIẾNG VIỆT:
"""

# LLM trả về:
"""
Đây là đoạn thứ hai.
Nhiều chi tiết hơn ở đây.
"""
```

### Bước 4: Merging

```python
# Ghép các bản dịch:
result = []

# Chunk 0 (Chapter)
result.append("Chương 1: Giới Thiệu")
result.append("\n\n")  # Chapter spacing
result.append("Đây là đoạn đầu tiên...")

# Chunk 1 (Paragraph)
result.append("\n\n")  # Paragraph spacing
result.append("Đây là đoạn thứ hai...")

# Chunk 2 (Chapter)
result.append("\n\n\n")  # Chapter spacing (3 breaks)
result.append("Chương 2: Chi Tiết...")

final_text = ''.join(result)
```

### Bước 5: Ghi File

```python
# Tùy format output:
- TXT: Ghi trực tiếp với UTF-8
- PDF: Tạo PDF mới với reportlab
- EPUB: Tạo EPUB với ebooklib, convert text → HTML
- DOCX: Tạo DOCX với python-docx, split thành paragraphs
```

---

## 🎛️ Tùy Chỉnh Nâng Cao

### Tối Ưu Cho Từng Loại Sách

#### Sách Văn Học
```bash
# Cần chất lượng cao, mạch văn tốt
python cli.py novel.txt novel_vi.txt \
  --provider anthropic \
  --model claude-3-5-sonnet-20241022 \
  --temperature 0.2 \
  --max-chunk-size 3000 \
  --context-size 500 \
  --max-workers 5
```

#### Sách Kỹ Thuật
```bash
# Cần chính xác, có thể nhanh hơn
python cli.py technical.pdf technical_vi.pdf \
  --provider groq \
  --model llama-3.1-70b-versatile \
  --temperature 0.1 \
  --max-workers 10
```

#### Truyện Ngắn
```bash
# Chunks nhỏ, xử lý nhanh
python cli.py short_story.txt short_story_vi.txt \
  --provider google \
  --model gemini-1.5-flash \
  --max-chunk-size 2000 \
  --min-chunk-size 500 \
  --max-workers 7
```

#### Giáo Trình Dài
```bash
# Chunks lớn, context dài, nhiều workers
python cli.py textbook.pdf textbook_vi.pdf \
  --provider groq \
  --max-chunk-size 5000 \
  --context-size 800 \
  --max-workers 15 \
  --verbose
```

---

## 🐛 Troubleshooting

### Lỗi Thường Gặp

#### 1. "API key is required"
```bash
# Giải pháp 1: Dùng --api-key
python cli.py input.txt output.txt --provider google --api-key AIza...

# Giải pháp 2: Dùng env variable
export GOOGLE_API_KEY="AIza..."
python cli.py input.txt output.txt --provider google

# Giải pháp 3: Dùng config file
# Sửa api_key trong config.json
python cli.py input.txt output.txt --config config.json
```

#### 2. "Rate limit exceeded"
```bash
# Giảm số workers
python cli.py input.txt output.txt --config config.json --max-workers 3

# Hoặc đổi provider khác (Groq không limit)
python cli.py input.txt output.txt --provider groq --api-key gsk_...
```

#### 3. "Failed to translate chunk X"
```bash
# Dùng verbose để xem lỗi chi tiết
python cli.py input.txt output.txt --config config.json --verbose

# Hệ thống sẽ tự retry 3 lần
# Nếu vẫn fail, chunk đó sẽ có [TRANSLATION FAILED]
```

#### 4. "File format not supported"
```bash
# Check extension
# Supported: .txt, .pdf, .epub, .docx, .doc

# Nếu file không có extension, specify format:
python cli.py input output.txt  # Sẽ treat input là .txt
```

#### 5. "Translation too slow"
```bash
# Giải pháp 1: Dùng provider nhanh hơn (Groq)
python cli.py input.txt output.txt --provider groq --api-key gsk_...

# Giải pháp 2: Tăng workers
python cli.py input.txt output.txt --config config.json --max-workers 10

# Giải pháp 3: Dùng chunks lớn hơn (ít API calls)
python cli.py input.txt output.txt --config config.json --max-chunk-size 5000
```

---

## 📊 Monitoring & Progress

### Progress Bar
```
Translating chunks: 45%|████▌     | 23/50 [01:45<02:05, 4.32s/chunk]
                    ↑    ↑         ↑  ↑    ↑     ↑
                    %  visual   done/total  ETA  speed
```

### Verbose Output
```bash
python cli.py input.txt output.txt --config config.json --verbose

# Sẽ hiện:
# 2024-01-15 10:30:45 - book_translator - INFO - Starting translation...
# 2024-01-15 10:30:45 - book_translator - INFO - Using provider: google
# 2024-01-15 10:30:45 - book_translator - INFO - Step 1: Chunking text...
# 2024-01-15 10:30:46 - book_translator - INFO - Chunk statistics: {...}
# 2024-01-15 10:30:46 - book_translator - INFO - Step 2: Translating...
# ...
```

### Log File
```bash
python cli.py input.txt output.txt --config config.json --log-file translation.log

# Review log
tail -f translation.log
grep ERROR translation.log
grep "chunk" translation.log
```

---

## 💰 Chi Phí Ước Tính

### Sách 100,000 Từ (~500,000 Chars)

| Provider | Model | Thời Gian | Chi Phí |
|----------|-------|-----------|---------|
| Groq | Llama 3.1 70B | 10-15 min | **FREE** ⭐ |
| Google | Gemini 1.5 Flash | 15-20 min | ~$0.50 |
| OpenAI | GPT-4o | 20-30 min | ~$3-5 |
| Anthropic | Claude 3.5 Sonnet | 20-30 min | ~$5-7 |

**Khuyến nghị**: Dùng Groq cho phần lớn trường hợp!

---

## ✅ Checklist Trước Khi Dịch

- [ ] Đã cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Đã có API key cho provider
- [ ] Đã test với file nhỏ trước
- [ ] Đã check encoding của file input (UTF-8 tốt nhất)
- [ ] Đã chuẩn bị đủ dung lượng cho file output
- [ ] Đã backup file gốc (nếu cần)

---

## 🚀 Tips Pro

1. **Test nhỏ trước**: Dịch 1-2 trang để check chất lượng
2. **Dùng Groq**: Nhanh + miễn phí cho hầu hết trường hợp
3. **Tăng workers cho Groq**: 15-20 workers vẫn OK
4. **Giảm workers cho paid APIs**: 3-5 workers để tránh rate limit
5. **Save config**: Tạo nhiều config cho các use cases khác nhau
6. **Monitor log**: Dùng --verbose và --log-file khi dịch sách dài
7. **Batch processing**: Dịch nhiều sách cùng lúc với script

---

Xem thêm:
- **CONFIG_GUIDE.md**: Chi tiết về cấu hình
- **README.md**: Tổng quan và tính năng
- **examples/example_usage.py**: Code examples
