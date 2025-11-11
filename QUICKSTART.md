# 🚀 Quick Start Guide - Bắt Đầu Nhanh

Hướng dẫn nhanh để bắt đầu dịch sách trong 5 phút!

## ⚡ 3 Bước Đơn Giản

### 1️⃣ Cài Đặt (1 phút)

```bash
# Clone hoặc download project
cd dichebooktailieu

# Cài dependencies
pip install -r requirements.txt
```

### 2️⃣ Lấy API Key (2 phút)

Chọn 1 trong các provider sau:

#### 🎯 Groq (Khuyến Nghị - MIỄN PHÍ!)
1. Vào: https://console.groq.com/
2. Đăng ký (free)
3. Tạo API key
4. Copy key (dạng: `gsk_...`)

#### 🌟 Google Gemini (Rẻ)
1. Vào: https://makersuite.google.com/app/apikey
2. Tạo API key
3. Copy key (dạng: `AIza...`)

#### 💰 OpenAI (Chất Lượng Cao)
1. Vào: https://platform.openai.com/api-keys
2. Tạo API key
3. Copy key (dạng: `sk-...`)

### 3️⃣ Dịch Sách (2 phút)

```bash
# Cách 1: Trực tiếp với Groq (FREE!)
python cli.py input.txt output.txt \
  --provider groq \
  --api-key gsk_YOUR_KEY

# Cách 2: Với Google Gemini
python cli.py input.txt output.txt \
  --provider google \
  --api-key AIza_YOUR_KEY

# Cách 3: Với OpenAI
python cli.py input.txt output.txt \
  --provider openai \
  --api-key sk_YOUR_KEY
```

## 🎯 Ví Dụ Cụ Thể

### Dịch File TXT
```bash
python cli.py mybook.txt mybook_vietnamese.txt \
  --provider groq \
  --api-key gsk_YOUR_KEY
```

### Dịch File PDF
```bash
python cli.py ebook.pdf ebook_vietnamese.pdf \
  --provider groq \
  --api-key gsk_YOUR_KEY
```

### Dịch Từ Tiếng Trung
```bash
python cli.py chinese_book.txt vietnamese_book.txt \
  --provider groq \
  --api-key gsk_YOUR_KEY \
  --source-lang chinese
```

## 📋 Các File Format Hỗ Trợ

✅ TXT - Text files
✅ PDF - PDF documents
✅ EPUB - E-books
✅ DOCX - Word documents

## 🌍 Ngôn Ngữ Hỗ Trợ

**Từ**: English, Chinese (中文), Russian (Русский)
**Sang**: Vietnamese (Tiếng Việt)

## ⚙️ Dùng Config File (Khuyến Nghị)

Nếu dịch nhiều file:

```bash
# 1. Tạo config
python cli.py --create-config

# 2. Sửa config.json:
{
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "api_key": "gsk_YOUR_KEY",
  "max_workers": 10,
  "source_lang": "english",
  "target_lang": "vietnamese"
}

# 3. Dùng config
python cli.py book1.txt book1_vi.txt --config config.json
python cli.py book2.pdf book2_vi.pdf --config config.json
```

## 🔥 Provider Nào Tốt Nhất?

| Tiêu Chí | Provider | Lý Do |
|----------|----------|-------|
| **Miễn Phí** | Groq | 100% free, unlimited |
| **Nhanh Nhất** | Groq | Tốc độ xử lý cực cao |
| **Rẻ Nhất** | Gemini Flash | $0.50 cho 1 cuốn sách |
| **Chất Lượng** | Claude 3.5 | Dịch văn học tốt nhất |

**Khuyến nghị**: Bắt đầu với **Groq** vì FREE và nhanh!

## 🎓 Ví Dụ Với Các Provider

### Groq (Nhanh + Free)
```bash
python cli.py input.txt output.txt \
  --provider groq \
  --api-key gsk_... \
  --max-workers 15
```

### Gemini Flash (Nhanh + Rẻ)
```bash
python cli.py input.txt output.txt \
  --provider google \
  --api-key AIza... \
  --model gemini-1.5-flash \
  --max-workers 7
```

### OpenAI GPT-4o (Chất Lượng Cao)
```bash
python cli.py input.txt output.txt \
  --provider openai \
  --api-key sk-... \
  --model gpt-4o \
  --max-workers 5
```

## ❓ Gặp Vấn Đề?

### Lỗi: "API key is required"
```bash
# Đảm bảo có --api-key hoặc dùng config file
python cli.py input.txt output.txt --provider groq --api-key YOUR_KEY
```

### Lỗi: "Module not found"
```bash
# Cài lại dependencies
pip install -r requirements.txt
```

### Dịch Chậm?
```bash
# Dùng Groq hoặc tăng workers
python cli.py input.txt output.txt \
  --provider groq \
  --api-key YOUR_KEY \
  --max-workers 15
```

## 📚 Tài Liệu Đầy Đủ

- **USAGE_GUIDE.md**: Hướng dẫn chi tiết
- **CONFIG_GUIDE.md**: Cấu hình providers
- **README.md**: Tổng quan dự án

## 💡 Tips

1. ✅ Test với file nhỏ trước (1-2 trang)
2. ✅ Dùng Groq cho phần lớn trường hợp
3. ✅ Tăng `--max-workers` lên 15-20 với Groq
4. ✅ Dùng `--verbose` để xem progress chi tiết
5. ✅ Save API key vào environment variable:
   ```bash
   export GROQ_API_KEY="gsk_..."
   python cli.py input.txt output.txt --provider groq
   ```

---

**Bắt đầu ngay**: Chọn provider → Lấy API key → Chạy lệnh dịch! 🚀
