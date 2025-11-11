# 🔋 Quota & Rate Limit Guide - Xử Lý Giới Hạn API

Hướng dẫn xử lý quota limits và rate limits khi dịch sách.

---

## ❓ Vấn Đề

Khi dùng API key FREE hoặc bị giới hạn, bạn có thể gặp:

### 1. Rate Limit (Giới hạn tốc độ)
```
Error: Rate limit exceeded
Error: Too many requests (429)
```
→ Quá nhiều requests trong thời gian ngắn

### 2. Quota Exceeded (Hết quota)
```
Error: Quota exceeded
Error: Insufficient quota
Error: Billing hard limit reached
```
→ Đã dùng hết quota tháng/ngày

### 3. Auth Error (Sai API key)
```
Error: Invalid API key (401)
Error: Unauthorized
```
→ API key sai hoặc hết hạn

---

## ✅ Giải Pháp

### 🚀 NEW: Hệ Thống Tự Động Xử Lý

Từ phiên bản mới, system TỰ ĐỘNG:

1. ✅ **Detect quota errors** - Nhận diện tự động
2. ✅ **Smart retry** - Retry với exponential backoff
3. ✅ **Skip failed chunks** - Không ghi error vào output
4. ✅ **Show suggestions** - Gợi ý cách fix
5. ✅ **Pause & resume** - Tạm dừng khi rate limit

### Cách Hoạt Động

```
┌─────────────────────────────────────────────┐
│  Dịch chunk → Error                         │
└─────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Detect error type:                         │
│  • Rate Limit → Pause & Retry               │
│  • Quota Exceeded → Stop & Suggest          │
│  • Auth Error → Stop & Fix                  │
└─────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Rate Limit:                                │
│  1. Pause 60s (exponential backoff)         │
│  2. Retry chunk                             │
│  3. Nếu vẫn fail → Pause 120s               │
│  4. Max 5 retries                           │
└─────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Quota Exceeded:                            │
│  1. Stop translation                        │
│  2. Show suggestions:                       │
│     • Đổi provider (Groq FREE!)             │
│     • Upgrade plan                          │
│     • Đợi quota reset                       │
└─────────────────────────────────────────────┘
```

---

## 🎯 Sử Dụng

### Option 1: CLI với Quota Handling (Mặc Định)

```bash
python cli.py input.txt output.txt \
  --provider google \
  --api-key AIza... \
  --max-workers 7
```

**Mặc định**:
- ✅ `skip_failed_chunks=True` - Skip chunks bị lỗi
- ✅ `handle_quota_errors=True` - Tự động xử lý quota
- ✅ `save_progress=True` - Save progress để resume

**Kết quả khi gặp lỗi**:
```
⚠️ Quota error detected: rate_limit
💡 Suggestions:
   🔧 Giảm max_workers xuống 3-5
   ⏰ Đợi vài phút rồi thử lại
   🔄 Đổi sang Groq (unlimited rate, FREE!)

⏳ Waiting 60s before retry...
⏳ Waiting... 30s remaining
⏳ Waiting... 10s remaining
✅ Resume translation!
✅ Retry thành công: chunk 15
```

### Option 2: Python API

```python
from book_translator import BookTranslator
from book_translator.llm_providers import GoogleProvider

provider = GoogleProvider(api_key="AIza...")

# Với quota handling (khuyến nghị)
translator = BookTranslator(
    llm_provider=provider,
    max_workers=5,
    skip_failed_chunks=True,      # Skip thay vì ghi error
    handle_quota_errors=True,     # Xử lý quota tự động
    save_progress=True            # Save để resume sau
)

# Dịch
result = translator.translate_text(text, "english")

# Check stats
stats = translator.get_stats()
print(f"Skipped chunks: {stats['skipped_chunks']}")
print(f"Quota errors: {stats['quota_errors']}")
```

### Option 3: UI (Tự Động)

Web UI tự động enable quota handling. Chỉ cần:

1. Upload file
2. Chọn provider
3. Dịch

Nếu gặp quota error, UI sẽ hiển thị:
```
⚠️ Rate Limit Detected!
Pausing 60s before retry...

💡 Suggestions:
• Giảm Max Workers xuống 5
• Đổi sang Groq (FREE, unlimited)
```

---

## 🔧 Configuration

### Tùy Chỉnh Quota Handling

```python
translator = BookTranslator(
    llm_provider=provider,
    max_workers=5,

    # Quota handling options
    skip_failed_chunks=True,      # True: Skip, False: Ghi error vào output
    handle_quota_errors=True,     # True: Auto handle, False: Throw error
    save_progress=True,           # True: Save progress, False: Không save
)
```

### Tùy Chỉnh Retry

```python
# Trong translator.py, QuotaHandler init:
from book_translator.core.quota_handler import QuotaHandler

quota_handler = QuotaHandler(
    max_quota_retries=5,       # Số lần retry tối đa
    quota_retry_delay=60       # Delay ban đầu (seconds)
)
# Exponential backoff: 60s → 120s → 240s → 480s → 960s
```

---

## 💡 Best Practices

### 1. Chọn Provider Phù Hợp

| Provider | Rate Limit | Quota | Khuyến Nghị |
|----------|-----------|-------|-------------|
| **Groq** | Unlimited | FREE | ⭐⭐⭐⭐⭐ Dùng Groq! |
| Google Gemini | ~60 req/min | Free tier limited | ⭐⭐⭐ OK cho sách ngắn |
| OpenAI | ~60 req/min | Pay as you go | ⭐⭐⭐ Tốn tiền |
| Anthropic | ~50 req/min | Pay as you go | ⭐⭐⭐ Tốn tiền |

**Kết luận**: Dùng **Groq** để tránh mọi quota issues!

### 2. Điều Chỉnh Max Workers

```bash
# FREE APIs (Google, etc.) - Giảm workers
--max-workers 5

# Groq (unlimited) - Tăng workers
--max-workers 15

# Khi gặp rate limit - Giảm xuống
--max-workers 3
```

### 3. Monitor & Adjust

```python
# Check stats sau khi dịch
stats = translator.get_stats()

if stats['quota_errors'] > 0:
    print(f"⚠️ Có {stats['quota_errors']} quota errors")
    print("💡 Giảm max_workers hoặc đổi provider")

if stats['skipped_chunks'] > 0:
    print(f"⚠️ {stats['skipped_chunks']} chunks bị skip")
    print("📄 Output có thể thiếu nội dung")
```

---

## 🆘 Troubleshooting

### Vấn Đề 1: Rate Limit Liên Tục

**Triệu chứng**:
```
Rate limit exceeded
⏳ Waiting 60s...
Rate limit exceeded again
⏳ Waiting 120s...
```

**Giải pháp**:
```bash
# Option 1: Giảm workers
--max-workers 3

# Option 2: Đổi Groq
--provider groq --api-key gsk_...

# Option 3: Chạy từng file nhỏ
# Chia sách lớn thành nhiều file nhỏ
```

### Vấn Đề 2: Quota Exceeded

**Triệu chứng**:
```
❌ QUOTA EXCEEDED! Hết quota API.
```

**Giải pháp**:

**Tức thì**:
```bash
# Đổi sang Groq (FREE!)
python cli.py input.txt output.txt \
  --provider groq \
  --api-key gsk_YOUR_KEY \
  --max-workers 15
```

**Dài hạn**:
1. Upgrade plan của provider
2. Đợi quota reset (thường reset hàng tháng)
3. Dùng API key khác
4. Dùng Groq làm provider chính

### Vấn Đề 3: Output Thiếu Nội Dung

**Nguyên nhân**: Failed chunks bị skip

**Check**:
```python
stats = translator.get_stats()
print(f"Skipped: {stats['skipped_chunks']}/{stats['total_chunks']}")
```

**Giải pháp**:

**Option 1**: Dịch lại failed chunks
```python
# Set skip_failed_chunks=False để xem chunks nào fail
translator = BookTranslator(
    llm_provider=provider,
    skip_failed_chunks=False  # Ghi error vào output
)

# Dịch → Xem output → Tìm [TRANSLATION FAILED] → Dịch lại chunks đó
```

**Option 2**: Retry với provider khác
```python
# Chunks fail với Google → Thử Groq
# 1. Dịch với Google, save progress
# 2. Load progress
# 3. Dịch lại failed chunks với Groq
```

---

## 📊 Output Comparison

### OLD Behavior (Trước)

```
Chunk 1: Đoạn đầu tiên đã dịch...

[TRANSLATION FAILED: Rate limit exceeded]

Chunk 3: Đoạn thứ ba đã dịch...

[TRANSLATION FAILED: Quota exceeded]

Chunk 5: Đoạn thứ năm...
```

❌ Output có error messages, khó đọc

### NEW Behavior (Bây giờ)

```
Chunk 1: Đoạn đầu tiên đã dịch...

Chunk 3: Đoạn thứ ba đã dịch...

Chunk 5: Đoạn thứ năm...
```

✅ Output sạch, nhưng thiếu chunks 2 và 4

**Log riêng**:
```
⚠️ Skipping 2 failed chunks - Output sẽ thiếu 2 đoạn!
💡 Suggestions: Đổi provider hoặc giảm workers
```

---

## 🎯 Recommendations

### Sách Ngắn (<50 trang)
```bash
# Dùng bất kỳ provider nào
--provider google --max-workers 5
```

### Sách Trung Bình (50-200 trang)
```bash
# Dùng Groq hoặc giảm workers
--provider groq --max-workers 15
# hoặc
--provider google --max-workers 3
```

### Sách Dài (>200 trang)
```bash
# PHẢI dùng Groq (tránh quota)
--provider groq --max-workers 20
```

### Production Use
```python
# Always enable quota handling
translator = BookTranslator(
    llm_provider=provider,
    skip_failed_chunks=True,
    handle_quota_errors=True,
    save_progress=True
)

# Monitor stats
stats = translator.get_stats()
if stats['quota_errors'] > 5:
    # Alert hoặc switch provider
    pass
```

---

## 📚 More Info

- **TROUBLESHOOTING.md**: General troubleshooting
- **CONFIG_GUIDE.md**: Provider configuration
- **USAGE_GUIDE.md**: CLI usage guide

---

**Kết luận**: Dùng Groq để tránh mọi vấn đề về quota! 🚀
