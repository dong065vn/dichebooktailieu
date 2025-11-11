# 🔧 Hướng Dẫn Cấu Hình (Configuration Guide)

## 📋 Mục Lục
- [Cấu Hình Google Gemini](#google-gemini)
- [Cấu Hình OpenAI](#openai)
- [Cấu Hình Anthropic Claude](#anthropic-claude)
- [Cấu Hình Groq](#groq-nhanh--miễn-phí)
- [Cấu Hình DeepSeek](#deepseek-rẻ)
- [Cấu Hình Cohere](#cohere)
- [Chi Tiết Các Tham Số](#chi-tiết-các-tham-số)

---

## Google Gemini

### Bước 1: Lấy API Key

1. Truy cập: https://makersuite.google.com/app/apikey
2. Click "Get API Key" hoặc "Create API Key"
3. Chọn project hoặc tạo project mới
4. Copy API key (dạng: `AIza...`)

### Bước 2: Tạo File config.json

Tạo file `config.json` với nội dung:

```json
{
  "llm_provider": "google",
  "model": "gemini-1.5-pro",
  "api_key": "AIzaSy...",
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

### Bước 3: Sử Dụng

```bash
# Với config file
python cli.py input.txt output.txt --config config.json

# Hoặc trực tiếp với CLI
python cli.py input.txt output.txt --provider google --api-key AIzaSy... --model gemini-1.5-pro
```

### Models Gemini Khả Dụng

| Model | Context Window | Tốc Độ | Giá |
|-------|---------------|---------|-----|
| `gemini-1.5-pro` | 2M tokens | ⚡⚡⚡ | 💰💰 |
| `gemini-1.5-flash` | 1M tokens | ⚡⚡⚡⚡ | 💰 |
| `gemini-pro` | 32k tokens | ⚡⚡⚡ | 💰 |

**Khuyến nghị**: Dùng `gemini-1.5-flash` cho tốc độ và giá rẻ!

### Example với Environment Variable

```bash
export GOOGLE_API_KEY="AIzaSy..."
python cli.py input.txt output.txt --provider google --model gemini-1.5-flash
```

---

## OpenAI

### Bước 1: Lấy API Key

1. Truy cập: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy API key (dạng: `sk-...`)

### Bước 2: Config File

```json
{
  "llm_provider": "openai",
  "model": "gpt-4o",
  "api_key": "sk-...",
  "max_workers": 5,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

### Models OpenAI Khả Dụng

| Model | Context | Tốc Độ | Giá | Chất Lượng |
|-------|---------|---------|-----|-----------|
| `gpt-4o` | 128k | ⚡⚡⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ |
| `gpt-4-turbo` | 128k | ⚡⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ |
| `gpt-4` | 8k | ⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ |
| `gpt-3.5-turbo` | 16k | ⚡⚡⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ |

---

## Anthropic Claude

### Bước 1: Lấy API Key

1. Truy cập: https://console.anthropic.com/
2. Vào "API Keys"
3. Click "Create Key"
4. Copy API key (dạng: `sk-ant-...`)

### Bước 2: Config File

```json
{
  "llm_provider": "anthropic",
  "model": "claude-3-5-sonnet-20241022",
  "api_key": "sk-ant-...",
  "max_workers": 5,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

### Models Claude Khả Dụng

| Model | Context | Giá | Chất Lượng |
|-------|---------|-----|-----------|
| `claude-3-5-sonnet-20241022` | 200k | 💰💰💰 | ⭐⭐⭐⭐⭐ |
| `claude-3-opus-20240229` | 200k | 💰💰💰💰 | ⭐⭐⭐⭐⭐ |
| `claude-3-sonnet-20240229` | 200k | 💰💰 | ⭐⭐⭐⭐ |
| `claude-3-haiku-20240307` | 200k | 💰 | ⭐⭐⭐⭐ |

---

## Groq (Nhanh & Miễn Phí!)

### Bước 1: Lấy API Key

1. Truy cập: https://console.groq.com/
2. Tạo account (miễn phí)
3. Vào "API Keys"
4. Copy API key (dạng: `gsk_...`)

### Bước 2: Config File

```json
{
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "api_key": "gsk_...",
  "max_workers": 10,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

**Lưu ý**: Groq CỰC NHANH, có thể dùng `max_workers: 10` hoặc cao hơn!

### Models Groq Khả Dụng

| Model | Context | Tốc Độ | Giá |
|-------|---------|---------|-----|
| `llama-3.1-70b-versatile` | 128k | ⚡⚡⚡⚡⚡ | 💰 FREE |
| `llama-3.1-8b-instant` | 128k | ⚡⚡⚡⚡⚡ | 💰 FREE |
| `mixtral-8x7b-32768` | 32k | ⚡⚡⚡⚡⚡ | 💰 FREE |

**Khuyến nghị**: Groq là lựa chọn TỐT NHẤT cho tốc độ và miễn phí!

---

## DeepSeek (Rẻ)

### Bước 1: Lấy API Key

1. Truy cập: https://platform.deepseek.com/
2. Tạo account
3. Vào API Keys
4. Copy API key

### Bước 2: Config File

```json
{
  "llm_provider": "deepseek",
  "model": "deepseek-chat",
  "api_key": "sk-...",
  "max_workers": 5,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

---

## Cohere

### Config File

```json
{
  "llm_provider": "cohere",
  "model": "command-r-plus",
  "api_key": "YOUR_COHERE_API_KEY",
  "max_workers": 5,
  "temperature": 0.3,
  "max_tokens": 4000,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

---

## Chi Tiết Các Tham Số

### Tham Số Bắt Buộc

| Tham Số | Mô Tả | Ví Dụ |
|---------|-------|-------|
| `llm_provider` | Provider LLM | `"google"`, `"openai"`, `"anthropic"`, `"groq"` |
| `model` | Model name | `"gemini-1.5-pro"`, `"gpt-4o"` |
| `api_key` | API key của bạn | `"AIza..."`, `"sk-..."` |

### Tham Số Tùy Chọn

| Tham Số | Mô Tả | Mặc Định | Khuyến Nghị |
|---------|-------|----------|-------------|
| `max_workers` | Số threads dịch song song | `5` | 5-10 (Groq có thể 10-20) |
| `max_chunk_size` | Kích thước chunk tối đa (chars) | `3000` | 2000-5000 |
| `min_chunk_size` | Kích thước chunk tối thiểu (chars) | `500` | 300-1000 |
| `context_size` | Số chars context từ chunk trước | `300` | 200-500 |
| `temperature` | Độ "creative" (0-1) | `0.3` | 0.2-0.4 (thấp = nhất quán) |
| `max_tokens` | Số tokens output tối đa | `4000` | 2000-8000 |
| `source_lang` | Ngôn ngữ nguồn | `"english"` | `"english"`, `"chinese"`, `"russian"` |
| `target_lang` | Ngôn ngữ đích | `"vietnamese"` | `"vietnamese"` |
| `show_progress` | Hiển thị progress bar | `true` | `true` |

### Giải Thích Chi Tiết

#### `max_workers`
- **Nhỏ (1-3)**: Chậm nhưng ổn định, ít lỗi
- **Trung bình (5-7)**: Cân bằng tốc độ và ổn định
- **Lớn (10+)**: Nhanh nhưng có thể hit rate limits

#### `temperature`
- **0.0-0.3**: Dịch nhất quán, ít biến đổi (khuyến nghị cho sách)
- **0.4-0.7**: Cân bằng
- **0.8-1.0**: Sáng tạo hơn nhưng ít nhất quán

#### `max_chunk_size`
- **Nhỏ (1000-2000)**: Nhiều chunks, dịch nhanh hơn, context ít hơn
- **Trung bình (3000-4000)**: Cân bằng
- **Lớn (5000+)**: Ít chunks, context tốt hơn, chậm hơn

---

## 💡 Tips & Best Practices

### 1. Chọn Provider

**Cho Tốc Độ**: Groq (miễn phí!) > Gemini Flash > GPT-4o
**Cho Chất Lượng**: Claude Opus > GPT-4 > Claude Sonnet > Gemini Pro
**Cho Giá Rẻ**: Groq (free) > DeepSeek > Gemini Flash > GPT-3.5

### 2. Tối Ưu max_workers

```bash
# Test với workers khác nhau
python cli.py input.txt output1.txt --config config.json --max-workers 3
python cli.py input.txt output2.txt --config config.json --max-workers 7
python cli.py input.txt output3.txt --config config.json --max-workers 10
```

### 3. Sử Dụng Environment Variables (An Toàn Hơn)

```bash
# Không lưu API key trong file
export GOOGLE_API_KEY="AIza..."
python cli.py input.txt output.txt --provider google
```

### 4. Config cho Sách Dài

```json
{
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "api_key": "gsk_...",
  "max_workers": 15,
  "max_chunk_size": 4000,
  "context_size": 500,
  "temperature": 0.2
}
```

### 5. Config cho Sách Ngắn

```json
{
  "llm_provider": "google",
  "model": "gemini-1.5-flash",
  "api_key": "AIza...",
  "max_workers": 3,
  "max_chunk_size": 2000,
  "temperature": 0.3
}
```

---

## 🔒 Bảo Mật API Key

### KHÔNG NÊN:
```bash
# Không commit API key vào git
git add config.json  # ❌
```

### NÊN:
```bash
# Dùng environment variables
export GOOGLE_API_KEY="AIza..."

# Hoặc file .env (thêm vào .gitignore)
echo "GOOGLE_API_KEY=AIza..." > .env
echo ".env" >> .gitignore
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề với config, tạo issue trên GitHub với:
- Provider đang dùng
- Model đang dùng
- Error message
- File config.json (đã ẩn API key)
