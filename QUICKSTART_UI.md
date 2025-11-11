# 🚀 Quick Start - Web UI

Dịch sách trong **3 phút** với giao diện đồ họa!

---

## ⚡ Bước 1: Chạy UI (30 giây)

### Linux/Mac:
```bash
python ui_gradio.py
```

### Windows:
```bash
python ui_gradio.py
```

### Hoặc dùng launcher:
```bash
./run_ui.sh        # Linux/Mac
run_ui.bat         # Windows
```

➡️ Mở trình duyệt: **http://localhost:7860**

---

## 📱 Giao Diện

```
┌─────────────────────────────────────────────┐
│  📚 Book Translator                         │
├─────────────────────────────────────────────┤
│  [🔄 Dịch Sách] [📖 Hướng Dẫn] [ℹ️ About]  │
├─────────────────┬───────────────────────────┤
│ 📥 INPUT        │ ⚙️ SETTINGS               │
│                 │                           │
│ [Upload File]   │ Provider: Groq (FREE!)    │
│ ✅ book.pdf     │ API Key: [Enter key]      │
│                 │ Max Workers: 15           │
│ Source: English │ Temperature: 0.3          │
│                 │                           │
│                 │ [🚀 Bắt Đầu Dịch]        │
├─────────────────┴───────────────────────────┤
│ 📤 OUTPUT                                   │
│ ✅ Translation Complete!                    │
│ [📥 Download File]                          │
└─────────────────────────────────────────────┘
```

---

## 🎯 Bước 2: Lấy API Key (1 phút)

### Groq (Khuyến Nghị - FREE!)

1. Vào: **https://console.groq.com/**
2. Đăng ký (miễn phí)
3. Click **"Create API Key"**
4. Copy key (dạng: `gsk_...`)

### Google Gemini (Rẻ)

1. Vào: **https://makersuite.google.com/app/apikey**
2. Click **"Create API Key"**
3. Copy key (dạng: `AIza...`)

---

## 📖 Bước 3: Dịch Sách (1-30 phút)

### Trong UI:

1. **Upload File**
   - Click "Upload File"
   - Chọn sách: TXT, PDF, EPUB, DOCX

2. **Chọn Provider**
   - Dropdown: Chọn "Groq Llama (FREE & FAST!)"

3. **Nhập API Key**
   - Paste key vào ô "API Key"

4. **Cài Đặt** (optional)
   - Max Workers: 15 (Groq rất nhanh!)
   - Temperature: 0.3 (khuyến nghị)

5. **Dịch!**
   - Click **"🚀 Bắt Đầu Dịch"**
   - Xem progress bar
   - Đợi hoàn tất

6. **Download**
   - Click **"📥 Download File Đã Dịch"**

Done! 🎉

---

## 💡 Tips Nhanh

### Dịch Nhanh Nhất
```
Provider: Groq Llama (FREE!)
Max Workers: 20
```
→ Sách 100,000 từ: ~10-15 phút

### Dịch Chất Lượng Cao
```
Provider: Claude 3.5 Sonnet
Temperature: 0.2
Max Workers: 5
```
→ Văn học, tiểu thuyết

### Dịch Rẻ Nhất
```
Provider: Groq (FREE!)
# hoặc
Provider: Gemini Flash ($0.5/sách)
```

---

## 📊 Ví Dụ Thực Tế

### Sách 50 trang (~25,000 từ)

**Setup:**
- Provider: Groq Llama
- Max Workers: 15
- File: novel.pdf

**Kết quả:**
```
✅ Translation Complete!

📊 Statistics:
- Total chunks: 22
- Successful: 22
- Failed: 0
- Total characters: 125,430
- Duration: 5.2 minutes
- Speed: 402 chars/sec

📥 Download: novel_vi.pdf
```

---

## 🎬 Demo Screenshots

### 1. Upload File
![Upload](docs/images/upload.png)

### 2. Configure
![Configure](docs/images/configure.png)

### 3. Translate
![Progress](docs/images/progress.png)

### 4. Download
![Download](docs/images/download.png)

---

## ❓ Troubleshooting

### UI không mở?

**Check:**
```bash
# Port có đang dùng không?
lsof -i :7860

# Có lỗi gì?
python ui_gradio.py --verbose
```

### Upload file lỗi?

**Nguyên nhân**: File quá lớn hoặc format không đúng

**Fix**: Check format (TXT, PDF, EPUB, DOCX)

### Dịch chậm?

**Fix**:
1. Dùng Groq (nhanh nhất)
2. Tăng Max Workers lên 15-20
3. Giảm chunk size

### API key lỗi?

**Fix**:
1. Check format key đúng chưa
2. Verify còn quota
3. Thử key khác

---

## 🆚 CLI vs Web UI

| Tính Năng | CLI | Web UI |
|-----------|-----|--------|
| **Dễ dùng** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Nhanh** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Visual** | ❌ | ✅ |
| **Progress** | Text | Progress bar |
| **Upload** | Path | Drag & drop |
| **Download** | Path | 1 click |
| **Config** | File/Args | GUI |

**Kết luận**:
- **Web UI** ← Người dùng thông thường
- **CLI** ← Developers, automation

---

## 🚀 Next Steps

Sau khi dịch xong:

1. **Review**: Đọc qua bản dịch
2. **Edit**: Sửa nếu cần (dùng Word/Editor)
3. **Share**: Chia sẻ với bạn bè
4. **Feedback**: Report issues nếu có

---

## 📚 More Guides

- **UI_GUIDE.md**: Hướng dẫn chi tiết UI
- **USAGE_GUIDE.md**: CLI guide
- **CONFIG_GUIDE.md**: Configuration
- **TROUBLESHOOTING.md**: Fix lỗi

---

**Happy Translating! 📚✨**

Bắt đầu ngay: `python ui_gradio.py`
