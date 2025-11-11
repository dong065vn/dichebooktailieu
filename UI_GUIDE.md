# 🎨 Web UI Guide - Hướng Dẫn Giao Diện Web

Book Translator có 2 giao diện web hiện đại: **Gradio** và **Streamlit**

---

## 🚀 Quick Start

### Cài Đặt

```bash
# Cài tất cả dependencies (bao gồm UI)
pip install -r requirements.txt

# Hoặc chỉ cài UI packages
pip install gradio streamlit
```

### Chạy Gradio UI (Khuyến Nghị)

```bash
python ui_gradio.py
```

Mở trình duyệt: http://localhost:7860

### Chạy Streamlit UI

```bash
streamlit run ui_streamlit.py
```

Mở trình duyệt: http://localhost:8501

---

## 🎯 So Sánh 2 UI

| Tính Năng | Gradio | Streamlit |
|-----------|--------|-----------|
| **Giao diện** | Modern, Clean | Professional |
| **Tốc độ** | ⚡⚡⚡ Nhanh | ⚡⚡ Khá nhanh |
| **Dễ dùng** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Tabs** | ✅ Có | ✅ Có |
| **Progress bar** | ✅ Có | ✅ Có |
| **File upload/download** | ✅ Có | ✅ Có |
| **Public sharing** | ✅ Dễ (1 click) | ⚠️ Cần config |
| **Khuyến nghị** | ⭐ Cho người dùng | Cho developers |

**Kết luận**: Dùng **Gradio** cho đơn giản và đẹp hơn!

---

## 📖 Hướng Dẫn Sử Dụng Gradio UI

### Giao Diện

```
┌─────────────────────────────────────────────────┐
│  📚 Book Translator - Dịch Sách Thông Minh      │
├─────────────────────────────────────────────────┤
│  [🔄 Dịch Sách] [📖 Hướng Dẫn] [ℹ️ About]      │
├──────────────────┬──────────────────────────────┤
│  📥 INPUT        │  ⚙️ SETTINGS                 │
│  • Upload file   │  • Provider selection        │
│  • Source lang   │  • API key                   │
│                  │  • Max workers               │
│                  │  • Temperature               │
│                  │  • Advanced settings         │
│                  │                              │
│                  │  [🚀 Bắt Đầu Dịch]          │
├──────────────────┴──────────────────────────────┤
│  📤 OUTPUT                                       │
│  • Status box                                   │
│  • Download button                              │
│  • Statistics                                   │
└─────────────────────────────────────────────────┘
```

### Các Bước

#### 1️⃣ Upload File

- Click vào **"Upload File"**
- Chọn file: TXT, PDF, EPUB, DOCX
- Thấy tên file → OK!

#### 2️⃣ Chọn Provider & API Key

**Provider Recommendations:**

| Provider | Khi Nào Dùng | API Key Link |
|----------|--------------|--------------|
| **Groq Llama** ⭐ | Miễn phí, nhanh nhất | [Get Key](https://console.groq.com/) |
| **Gemini Flash** | Rẻ, nhanh | [Get Key](https://makersuite.google.com/app/apikey) |
| **GPT-4o** | Chất lượng cao | [Get Key](https://platform.openai.com/api-keys) |
| **Claude 3.5** | Văn học, tiểu thuyết | [Get Key](https://console.anthropic.com/) |

**Nhập API Key:**
- Click link "Get Key" → Lấy API key
- Paste vào ô "API Key"
- ⚠️ **Không share API key với người khác!**

#### 3️⃣ Cài Đặt

**Cài đặt cơ bản:**

```
Max Workers:
  Groq: 15-20     ← Nhanh, unlimited
  Others: 5-7     ← Tránh rate limit

Temperature: 0.3  ← Nhất quán (khuyến nghị)
```

**Cài đặt nâng cao** (Click "Cài đặt nâng cao"):
- Max Chunk Size: 3000 (mặc định)
- Min Chunk Size: 500 (mặc định)
- Context Size: 300 (mặc định)

💡 **Tip**: Dùng mặc định cho hầu hết trường hợp!

#### 4️⃣ Bắt Đầu Dịch

1. Click **"🚀 Bắt Đầu Dịch"**
2. Xem progress bar
3. Đợi hoàn tất (hiển thị thống kê)
4. Click **"📥 Download File Đã Dịch"**

---

## 💡 Tips & Tricks

### Tối Ưu Tốc Độ

```bash
# Dùng Groq với nhiều workers
Provider: Groq Llama (FREE & FAST!)
Max Workers: 20
Model: llama-3.1-70b-versatile
```

**Kết quả**: Sách 100,000 từ → ~10-15 phút

### Tối Ưu Chất Lượng

```bash
# Dùng Claude với temperature thấp
Provider: Anthropic Claude 3.5 Sonnet
Max Workers: 5
Temperature: 0.2
```

**Kết quả**: Dịch văn học chất lượng cao nhất

### Tối Ưu Chi Phí

```bash
# Dùng Groq (FREE!) hoặc Gemini Flash
Provider: Groq Llama (FREE!)
# Hoặc
Provider: Google Gemini Flash (Rẻ)
```

**Kết quả**: $0 (Groq) hoặc ~$0.5/sách (Gemini)

---

## 🎨 Gradio Features

### 1. Tabs

**Tab 1: 🔄 Dịch Sách**
- Upload file
- Configure settings
- Translate
- Download

**Tab 2: 📖 Hướng Dẫn**
- Quick start guide
- Provider comparison
- Tips & tricks

**Tab 3: ℹ️ About**
- Project info
- Technical stack
- Performance stats

### 2. Real-time Progress

```
Translating chunk 23/50 ████████▌░░░░░░░░ 46%
```

### 3. Statistics Display

```
✅ Translation Complete!

📊 Statistics:
- Total chunks: 50
- Successful: 50
- Failed: 0
- Total characters: 150,000
- Duration: 180.5 seconds
- Speed: 831 chars/sec
```

### 4. Auto API Key Help

Khi chọn provider, UI tự động hiển thị:
- Link lấy API key
- Format của API key
- Hướng dẫn

---

## 🔧 Advanced Usage

### Public Sharing (Gradio)

Muốn chia sẻ UI với người khác?

**Option 1: Local Network**
```python
# Trong ui_gradio.py, dòng cuối:
demo.launch(
    server_name="0.0.0.0",  # Allow external access
    share=False
)
```

Truy cập từ máy khác: `http://YOUR_IP:7860`

**Option 2: Public Link (Gradio Share)**
```python
demo.launch(
    share=True  # Tạo public link (gradio.live)
)
```

Gradio sẽ tạo link public: `https://xxxxx.gradio.live`

⚠️ **Lưu ý**: Link public hết hạn sau 72 giờ

### Custom Port

```python
# Gradio
demo.launch(server_port=8080)

# Streamlit
streamlit run ui_streamlit.py --server.port 8080
```

### Disable Queue

Nếu chỉ 1 người dùng:

```python
demo.launch(
    enable_queue=False  # Tắt queue
)
```

---

## 📱 Responsive Design

UI tự động responsive:

**Desktop (>1200px)**:
```
┌─────────────┬─────────────┐
│   INPUT     │  SETTINGS   │
│             │             │
└─────────────┴─────────────┘
```

**Mobile (<768px)**:
```
┌─────────────┐
│   INPUT     │
└─────────────┘
┌─────────────┐
│  SETTINGS   │
└─────────────┘
```

---

## 🐛 Troubleshooting UI

### Lỗi: "Address already in use"

**Nguyên nhân**: Port 7860 đang được dùng

**Fix**:
```bash
# Tìm process đang dùng port
lsof -i :7860

# Kill process
kill -9 <PID>

# Hoặc đổi port
python ui_gradio.py --server-port 7861
```

### Lỗi: "Module not found: gradio"

**Fix**:
```bash
pip install gradio
```

### Lỗi: Upload file không hoạt động

**Nguyên nhân**: File quá lớn

**Fix**: Tăng max file size
```python
# Trong ui_gradio.py
input_file = gr.File(
    ...,
    file_count="single",
    max_file_size="100MB"  # Tăng lên
)
```

### UI chạy chậm

**Fix**:
1. Tắt queue: `enable_queue=False`
2. Giảm max_workers
3. Dùng model nhanh hơn (Groq)

---

## 🎯 Best Practices

### 1. Security

❌ **KHÔNG**:
- Commit API key vào code
- Share API key
- Expose API key qua public link

✅ **NÊN**:
- Nhập API key mỗi lần dùng
- Dùng environment variables
- Enable authentication nếu public

### 2. Performance

✅ **Optimize**:
```python
# Dùng caching
@st.cache_data  # Streamlit
# hoặc
gr.Interface(..., cache_examples=True)  # Gradio
```

### 3. User Experience

✅ **Tốt**:
- Clear error messages
- Progress indicators
- Help text cho mọi field
- Example files

---

## 📊 Monitoring

### View Logs

```bash
# Gradio
tail -f gradio.log

# Streamlit
streamlit run ui_streamlit.py --logger.level=debug
```

### Performance Metrics

UI tự động track:
- Translation time
- Chunks processed
- Success/failure rate
- Characters per second

---

## 🚀 Deployment

### Deploy to Hugging Face Spaces (FREE!)

```bash
# 1. Tạo account: huggingface.co
# 2. Create new Space
# 3. Upload files:
#    - ui_gradio.py
#    - requirements.txt
#    - book_translator/
# 4. Space tự động deploy!
```

**Kết quả**: Public URL miễn phí!

### Deploy to Streamlit Cloud (FREE!)

```bash
# 1. Tạo account: streamlit.io
# 2. Connect GitHub repo
# 3. Select ui_streamlit.py
# 4. Deploy!
```

---

## 💬 Support

**Có vấn đề với UI?**

1. Check console logs
2. Check browser console (F12)
3. See TROUBLESHOOTING.md
4. Create GitHub issue

---

## 📚 More Resources

- **Gradio Docs**: https://gradio.app/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Examples**: See `examples/` folder
- **Advanced**: See source code comments

---

**Enjoy translating! 📚✨**
