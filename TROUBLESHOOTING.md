# 🚨 Troubleshooting Guide - Giải Quyết Lỗi

## ❌ Lỗi: "Incorrect API key provided"

### Triệu Chứng
```
Error code: 401 - Incorrect API key provided: AIzaSyCG...
You can find your API key at https://platform.openai.com/account/api-keys
```

### Nguyên Nhân
Bạn đang dùng **sai provider** với **sai loại API key**:
- Provider: OpenAI (mặc định)
- API Key: Google (AIzaSy...)
- ❌ **Không khớp!**

### Cách Nhận Biết Loại API Key

| Provider | API Key Format | Ví Dụ |
|----------|---------------|--------|
| OpenAI | `sk-...` | `sk-proj-abc123...` |
| Anthropic | `sk-ant-...` | `sk-ant-api03-abc...` |
| **Google** | **`AIza...`** | **`AIzaSyC...`** ← Bạn đang dùng |
| Groq | `gsk_...` | `gsk_abc123...` |
| Cohere | `...` | Various formats |

### ✅ Giải Pháp

#### **Cách 1: Dùng Config File (Khuyến Nghị)**

Tạo file `config.json`:
```json
{
  "llm_provider": "google",
  "model": "gemini-1.5-flash",
  "api_key": "AIzaSyCG_YOUR_FULL_KEY_HERE",
  "max_workers": 7,
  "source_lang": "english",
  "target_lang": "vietnamese"
}
```

**QUAN TRỌNG**:
- `"llm_provider": "google"` ← PHẢI là "google"
- `"api_key": "AIza..."` ← Google API key của bạn

Chạy lại:
```bash
python cli.py input.txt output.txt --config config.json
```

#### **Cách 2: Dùng CLI Trực Tiếp**

```bash
python cli.py input.txt output.txt \
  --provider google \
  --api-key AIzaSyCG_YOUR_KEY \
  --model gemini-1.5-flash
```

**QUAN TRỌNG**: `--provider google` phải match với loại API key!

#### **Cách 3: Environment Variable**

```bash
export GOOGLE_API_KEY="AIzaSyCG_YOUR_KEY"
python cli.py input.txt output.txt --provider google
```

---

## 🔍 Debug: Kiểm Tra Provider Đang Dùng

### Check 1: Xem Log
Tìm dòng này trong log:
```
Using provider: google  ← Phải là "google", KHÔNG phải "openai"
```

### Check 2: Verify Config
```bash
cat config.json | grep llm_provider
# Kết quả phải là: "llm_provider": "google"
```

### Check 3: Test API Key

**Test Google API Key:**
```bash
# Install package nếu chưa có
pip install google-generativeai

# Test
python3 << 'EOF'
import google.generativeai as genai
genai.configure(api_key="AIzaSyCG_YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
print("✅ Google API key works!")
print(response.text)
EOF
```

**Test OpenAI API Key:**
```bash
pip install openai
python3 << 'EOF'
from openai import OpenAI
client = OpenAI(api_key="sk-YOUR_KEY")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print("✅ OpenAI API key works!")
print(response.choices[0].message.content)
EOF
```

---

## 🆘 Các Lỗi Khác

### Lỗi: "Module not found: google.generativeai"

**Nguyên nhân**: Chưa cài package

**Fix**:
```bash
pip install google-generativeai
```

### Lỗi: "Module not found: openai"

**Nguyên nhân**: Chưa cài package

**Fix**:
```bash
pip install openai
```

### Lỗi: "Rate limit exceeded"

**Nguyên nhân**: Quá nhiều requests

**Fix**:
```bash
# Giảm workers
python cli.py input.txt output.txt --config config.json --max-workers 3

# Hoặc đổi sang Groq (free, unlimited)
python cli.py input.txt output.txt --provider groq --api-key gsk_YOUR_KEY
```

### Lỗi: "Failed after 3 attempts"

**Nguyên nhân**: API key sai hoặc hết quota

**Check**:
1. Verify API key đúng
2. Check quota tại console của provider
3. Check internet connection

---

## 📋 Checklist Trước Khi Dịch

- [ ] Đã cài đúng packages: `pip install -r requirements.txt`
- [ ] API key **đúng loại** cho provider
- [ ] Config file có `llm_provider` match với API key
- [ ] Test API key với script ở trên
- [ ] Check internet connection

---

## 💡 Tips

### Biết Provider Nào Đang Chạy

Thêm `--verbose` để xem chi tiết:
```bash
python cli.py input.txt output.txt --config config.json --verbose
```

Output sẽ hiện:
```
Using provider: google  ← Confirm provider
Model: gemini-1.5-flash
```

### Provider Recommendations

| Trường Hợp | Provider | Lý Do |
|------------|----------|-------|
| Miễn phí | Groq | Free unlimited |
| Nhanh | Groq hoặc Gemini Flash | Tốc độ cao |
| Chất lượng | Claude 3.5 Sonnet | Dịch văn học tốt |
| Rẻ | Gemini Flash | $0.5/sách |

---

## 🔧 Ví Dụ Config Đúng

### Google Gemini
```json
{
  "llm_provider": "google",
  "model": "gemini-1.5-flash",
  "api_key": "AIza..."
}
```

### OpenAI
```json
{
  "llm_provider": "openai",
  "model": "gpt-4o",
  "api_key": "sk-..."
}
```

### Groq (Free!)
```json
{
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "api_key": "gsk_..."
}
```

---

## 📞 Vẫn Gặp Vấn Đề?

1. Check file `USAGE_GUIDE.md` - Troubleshooting section
2. Check file `CONFIG_GUIDE.md` - Provider setup
3. Run với `--verbose --log-file debug.log` để debug
4. Tạo issue trên GitHub với log file
