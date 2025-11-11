# 🔧 Windows Installation Fix - Pydantic Core Error

Giải pháp cho lỗi: `Building wheel for pydantic-core failed`

---

## ❌ Lỗi

```
error: can't find Rust compiler
note: this package requires Rust >=1.56.0
```

**Nguyên nhân**: pydantic-core cần Rust compiler trên Windows

---

## ✅ Giải Pháp (Chọn 1 trong 4)

### 🚀 Solution 1: Dùng Pre-built Wheels (Khuyến Nghị - Nhanh Nhất!)

```bash
# Upgrade pip trước
python -m pip install --upgrade pip

# Cài với pre-built wheels
pip install --only-binary :all: pydantic pydantic-core

# Sau đó cài requirements
pip install -r requirements.txt
```

✅ **Ưu điểm**: Không cần Rust, cài đặt nhanh
❌ **Nhược điểm**: Cần Python 3.8+

---

### 🔨 Solution 2: Cài Microsoft C++ Build Tools

**Bước 1**: Download Microsoft C++ Build Tools
- Link: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Tải file: vs_BuildTools.exe (~4MB)

**Bước 2**: Chạy installer
- Chọn: "Desktop development with C++"
- Install (~6GB)

**Bước 3**: Restart terminal và cài lại
```bash
pip install -r requirements.txt
```

✅ **Ưu điểm**: Giải quyết mọi compilation issue
❌ **Nhược điểm**: Tốn thời gian và dung lượng (~6GB)

---

### 📦 Solution 3: Dùng Anaconda (Khuyến Nghị cho Người Mới)

**Bước 1**: Download Anaconda
- Link: https://www.anaconda.com/download
- Chọn Windows version

**Bước 2**: Tạo environment mới
```bash
conda create -n book-translator python=3.11
conda activate book-translator
```

**Bước 3**: Cài dependencies
```bash
# Anaconda có sẵn pre-compiled packages
pip install -r requirements.txt
```

✅ **Ưu điểm**: Đơn giản, ổn định, có GUI
❌ **Nhược điểm**: Tải về ~600MB

---

### 🔄 Solution 4: Downgrade Dependencies

Dùng version cũ hơn không cần Rust:

**Bước 1**: Tạo file `requirements-windows.txt`
```txt
# Core
anthropic==0.25.0
openai==1.14.0
google-generativeai==0.4.1
cohere==5.1.0
groq==0.5.0

# Pydantic - version cũ không cần Rust
pydantic==1.10.13
pydantic-core==2.10.1  # Hoặc bỏ qua, dùng pydantic 1.x

# Other dependencies
python-docx==1.1.0
PyPDF2==3.0.1
ebooklib==0.18
beautifulsoup4==4.12.3
requests==2.31.0
tqdm==4.66.2
colorama==0.4.6
python-dotenv==1.0.1
gradio==4.19.2
streamlit==1.31.1
pillow==10.2.0
```

**Bước 2**: Cài đặt
```bash
pip install -r requirements-windows.txt
```

✅ **Ưu điểm**: Nhanh, không cần thêm tools
❌ **Nhược điểm**: Dùng version cũ hơn

---

## 🎯 Quick Start (Recommended)

Cách nhanh nhất cho Windows:

```bash
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. Cài pre-built wheels
pip install --only-binary :all: pydantic pydantic-core anthropic openai google-generativeai cohere groq

# 3. Cài UI frameworks
pip install gradio streamlit

# 4. Cài file handlers
pip install python-docx PyPDF2 ebooklib beautifulsoup4

# 5. Cài utilities
pip install requests tqdm colorama python-dotenv pillow

# 6. Test
python cli.py --help
```

Nếu thành công → Bỏ qua mọi lỗi và bắt đầu dịch! 🎉

---

## ✅ Verify Installation

```bash
# Test imports
python -c "from book_translator import BookTranslator; print('✅ OK!')"

# Test CLI
python cli.py --help

# Test UI
python ui_gradio.py
```

Nếu tất cả chạy được → Installation thành công!

---

## 🆘 Vẫn Lỗi?

### Lỗi: "No module named 'book_translator'"

**Fix**:
```bash
# Ở thư mục gốc project (có file cli.py)
set PYTHONPATH=%CD%  # Windows CMD
# hoặc
$env:PYTHONPATH = $PWD  # PowerShell
```

### Lỗi: "Python not found"

**Fix**:
1. Download Python từ https://www.python.org/downloads/
2. Check "Add Python to PATH" khi install
3. Restart terminal

### Lỗi khác

**Option 1**: Dùng Anaconda (Solution 3)
**Option 2**: Dùng requirements-windows.txt (Solution 4)

---

## 💡 Best Practice cho Windows

```bash
# 1. Luôn dùng virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Upgrade pip trước khi cài
python -m pip install --upgrade pip

# 3. Cài từng package để debug dễ hơn
pip install anthropic
pip install openai
# ... etc

# 4. Nếu 1 package lỗi, skip và thử package khác
pip install google-generativeai || echo "Skipped"
```

---

## 🚀 Start Translating

Sau khi fix xong:

```bash
# Với Gradio UI
python ui_gradio.py

# Hoặc CLI
python cli.py input.txt output.txt --provider groq --api-key gsk_...
```

---

## 📊 Comparison of Solutions

| Solution | Time | Difficulty | Recommended |
|----------|------|-----------|-------------|
| **Pre-built Wheels** | 2 min | ⭐ Easy | ⭐⭐⭐⭐⭐ |
| **Anaconda** | 10 min | ⭐ Easy | ⭐⭐⭐⭐ |
| **Downgrade** | 3 min | ⭐⭐ Medium | ⭐⭐⭐ |
| **Build Tools** | 30+ min | ⭐⭐⭐ Hard | ⭐⭐ |

**Kết luận**: Dùng **Pre-built Wheels** (Solution 1) cho nhanh nhất!

---

**Happy Translating! 📚✨**
