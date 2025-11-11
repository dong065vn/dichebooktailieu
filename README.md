# 📚 Book Translator - Công Cụ Dịch Sách Thông Minh

Một extension/công cụ Python mạnh mẽ để dịch sách từ tiếng Anh, tiếng Trung, tiếng Nga sang tiếng Việt sử dụng các API LLM tiên tiến. Hệ thống chia đoạn và ghép văn bản thông minh giúp giữ nguyên mạch và cấu trúc của sách.

## ✨ Tính Năng Nổi Bật

### 🤖 Hỗ Trợ Nhiều LLM Providers
- **OpenAI** (GPT-4, GPT-4o, GPT-3.5)
- **Anthropic** (Claude 3.5 Sonnet, Opus, Haiku)
- **Google** (Gemini 1.5 Pro, Flash)
- **Cohere** (Command R+)
- **Groq** (Llama 3.1, Mixtral) - Cực nhanh!
- **DeepSeek** - Rẻ và mạnh

### 🧠 Intelligent Chunking System
- Tự động nhận diện chapter, section, paragraph
- Chia đoạn thông minh dựa trên cấu trúc văn bản
- Bảo toàn context giữa các đoạn để giữ mạch văn
- Tối ưu kích thước chunks cho translation

### ⚡ Parallel Processing
- Dịch nhiều chunks đồng thời
- Tăng tốc độ dịch lên gấp nhiều lần
- Progress tracking real-time
- Error handling và retry tự động

### 📄 Hỗ Trợ Nhiều Định Dạng
- **TXT** - Text files
- **PDF** - Portable Document Format
- **EPUB** - E-books
- **DOCX** - Microsoft Word

### 🌍 Ngôn Ngữ
- **Nguồn**: English, Chinese (中文), Russian (Русский)
- **Đích**: Vietnamese (Tiếng Việt)

## 🎨 Web UI - Giao Diện Đồ Họa (Mới!)

Bây giờ có **giao diện web hiện đại** - không cần dòng lệnh!

### 🚀 Chạy Web UI

```bash
# Gradio UI (Khuyến nghị - đẹp, dễ dùng)
python ui_gradio.py

# Hoặc Streamlit UI
streamlit run ui_streamlit.py

# Hoặc dùng launcher
./run_ui.sh        # Linux/Mac
run_ui.bat         # Windows
```

Mở trình duyệt: **http://localhost:7860** (Gradio) hoặc **http://localhost:8501** (Streamlit)

**Tính năng UI:**
- ✅ Drag & drop upload file
- ✅ Chọn provider qua dropdown
- ✅ Progress bar real-time
- ✅ Download file đã dịch
- ✅ Hiển thị statistics
- ✅ Responsive design (mobile-friendly)

Xem chi tiết: **[UI_GUIDE.md](UI_GUIDE.md)**

---

## 🚀 Cài Đặt

### Yêu Cầu
- Python 3.8+
- pip

### Cài Đặt Cơ Bản

```bash
# Clone repository
git clone https://github.com/yourusername/book-translator.git
cd book-translator

# Cài đặt dependencies (bao gồm UI)
pip install -r requirements.txt

# Hoặc cài đặt như package
pip install -e .
```

### Cài Đặt Dependencies Tùy Chọn

```bash
# Chỉ cài OpenAI
pip install openai

# Chỉ cài Anthropic
pip install anthropic

# Chỉ cài PDF support
pip install PyPDF2 pdfplumber

# Cài tất cả
pip install -r requirements.txt
```

## 📖 Sử Dụng

### 1. CLI (Command Line Interface)

#### Tạo Config File

```bash
python cli.py --create-config
```

Sửa file `config.json` với API key của bạn:

```json
{
  "llm_provider": "openai",
  "model": "gpt-4o",
  "api_key": "YOUR_API_KEY_HERE",
  "max_workers": 5,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

#### Dịch File

```bash
# Dịch file TXT
python cli.py input.txt output.txt --provider openai --api-key YOUR_KEY

# Dịch file PDF từ tiếng Trung
python cli.py book.pdf book_vi.pdf --source-lang chinese --provider anthropic --api-key YOUR_KEY

# Dịch file EPUB với config file
python cli.py book.epub book_vi.epub --config config.json

# Dịch với Groq (nhanh và miễn phí!)
python cli.py input.txt output.txt --provider groq --api-key YOUR_GROQ_KEY

# Verbose mode
python cli.py input.txt output.txt --provider openai --api-key YOUR_KEY --verbose
```

#### Tùy Chọn CLI

```
positional arguments:
  input                 Input file path
  output                Output file path

optional arguments:
  --provider {openai,anthropic,google,cohere,groq,deepseek}
                        LLM provider to use
  --api-key API_KEY     API key for the provider
  --model MODEL         Model name
  --source-lang {english,chinese,russian}
                        Source language
  --target-lang TARGET_LANG
                        Target language
  --max-workers MAX_WORKERS
                        Number of parallel workers
  --max-chunk-size MAX_CHUNK_SIZE
                        Maximum chunk size in characters
  --min-chunk-size MIN_CHUNK_SIZE
                        Minimum chunk size in characters
  --config CONFIG       Path to config file (JSON)
  --verbose, -v         Verbose output
  --log-file LOG_FILE   Log file path
```

### 2. Python API

```python
from book_translator import BookTranslator
from book_translator.llm_providers import OpenAIProvider

# Khởi tạo provider
provider = OpenAIProvider(
    api_key="your-api-key",
    model="gpt-4o",
    temperature=0.3
)

# Khởi tạo translator
translator = BookTranslator(
    llm_provider=provider,
    max_workers=5,
    max_chunk_size=3000,
    show_progress=True
)

# Dịch file
translator.translate_file(
    input_file="input.txt",
    output_file="output.txt",
    source_lang="english",
    target_lang="vietnamese"
)

# Hoặc dịch text trực tiếp
translated_text = translator.translate_text(
    text="Your text here...",
    source_lang="english",
    target_lang="vietnamese"
)
```

### 3. Sử Dụng Các Provider Khác Nhau

#### OpenAI (GPT-4)
```python
from book_translator.llm_providers import OpenAIProvider

provider = OpenAIProvider(
    api_key="sk-...",
    model="gpt-4o"  # hoặc "gpt-4", "gpt-3.5-turbo"
)
```

#### Anthropic (Claude)
```python
from book_translator.llm_providers import AnthropicProvider

provider = AnthropicProvider(
    api_key="sk-ant-...",
    model="claude-3-5-sonnet-20241022"  # hoặc "claude-3-opus-20240229"
)
```

#### Google (Gemini)
```python
from book_translator.llm_providers import GoogleProvider

provider = GoogleProvider(
    api_key="AIza...",
    model="gemini-1.5-pro"
)
```

#### Groq (Cực Nhanh!)
```python
from book_translator.llm_providers import GroqProvider

provider = GroqProvider(
    api_key="gsk_...",
    model="llama-3.1-70b-versatile"
)
```

#### DeepSeek (Rẻ)
```python
from book_translator.llm_providers import DeepSeekProvider

provider = DeepSeekProvider(
    api_key="sk-...",
    model="deepseek-chat"
)
```

### 4. Advanced Usage

#### Custom Chunking Parameters

```python
translator = BookTranslator(
    llm_provider=provider,
    max_chunk_size=5000,  # Chunks lớn hơn
    min_chunk_size=1000,  # Chunks nhỏ nhất
    context_size=500,     # Context dài hơn
    max_workers=10        # Nhiều workers hơn
)
```

#### Progress Callback

```python
def progress_callback(chunk_id, total, translation):
    print(f"Translated chunk {chunk_id+1}/{total}")

translated = translator.translate_text(
    text=long_text,
    source_lang="english",
    callback=progress_callback
)
```

#### Get Statistics

```python
translator.translate_file(input_file, output_file, "english")

stats = translator.get_stats()
print(f"Chunks: {stats['total_chunks']}")
print(f"Success: {stats['successful_chunks']}")
print(f"Speed: {stats['total_chars'] / (stats['end_time'] - stats['start_time'])} chars/sec")
```

## 🏗️ Kiến Trúc

```
book_translator/
├── core/
│   ├── chunker.py       # Intelligent text chunking
│   ├── merger.py        # Smart text merging
│   └── translator.py    # Main translation engine
├── llm_providers/
│   ├── base.py          # Base provider class
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   ├── google_provider.py
│   ├── cohere_provider.py
│   ├── groq_provider.py
│   └── deepseek_provider.py
├── formats/
│   ├── handler.py       # Main file handler
│   ├── txt_handler.py
│   ├── pdf_handler.py
│   ├── epub_handler.py
│   └── docx_handler.py
└── utils/
    ├── config.py        # Configuration management
    └── logger.py        # Logging setup
```

## 🎯 Workflow

1. **Đọc File**: Tự động detect format và đọc nội dung
2. **Chunking**: Chia văn bản thành các chunks thông minh
   - Nhận diện chapters, sections, paragraphs
   - Bảo toàn cấu trúc và formatting
   - Thêm context từ đoạn trước
3. **Translation**: Dịch song song nhiều chunks
   - Parallel processing với ThreadPoolExecutor
   - Progress tracking
   - Error handling và retry
4. **Merging**: Ghép các chunks đã dịch
   - Giữ nguyên cấu trúc gốc
   - Xử lý spacing và line breaks
   - Validation
5. **Ghi File**: Lưu kết quả với format tương ứng

## 🔧 Configuration

### Environment Variables

```bash
# API Keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export GROQ_API_KEY="gsk_..."

# Settings
export BOOK_TRANSLATOR_PROVIDER="openai"
export BOOK_TRANSLATOR_MODEL="gpt-4o"
export BOOK_TRANSLATOR_MAX_WORKERS="5"
```

### Config File (config.json)

```json
{
  "llm_provider": "openai",
  "model": "gpt-4o",
  "api_key": "YOUR_API_KEY",
  "max_workers": 5,
  "max_chunk_size": 3000,
  "min_chunk_size": 500,
  "context_size": 300,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese",
  "show_progress": true
}
```

## 📊 Performance

### Tốc Độ Dịch (ước tính)

| Provider | Model | Speed | Cost |
|----------|-------|-------|------|
| Groq | Llama 3.1 70B | ⚡⚡⚡⚡⚡ | 💰 Free |
| OpenAI | GPT-4o | ⚡⚡⚡⚡ | 💰💰 |
| Anthropic | Claude 3.5 Sonnet | ⚡⚡⚡⚡ | 💰💰💰 |
| Google | Gemini 1.5 Pro | ⚡⚡⚡ | 💰💰 |
| DeepSeek | DeepSeek Chat | ⚡⚡⚡ | 💰 |

### Ví Dụ Thực Tế

- **Sách 100,000 từ (500,000 chars)**
  - Với 5 workers: ~15-30 phút (tùy provider)
  - Với 10 workers: ~8-15 phút

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Tất cả các LLM providers
- Python open source community
- Contributors

## 📧 Support

Nếu bạn gặp vấn đề hoặc có câu hỏi, vui lòng tạo issue trên GitHub.

## 🔮 Roadmap

- [ ] Hỗ trợ thêm ngôn ngữ
- [ ] Web UI
- [ ] Batch processing
- [ ] Quality assessment
- [ ] Terminology management
- [ ] Translation memory
- [ ] More file formats (MOBI, AZW, etc.)

## ⭐ Star History

Nếu tool này hữu ích, đừng quên star repo nhé! ⭐

---

Made with ❤️ for the Vietnamese reading community
