@echo off
REM Auto installer for Book Translator on Windows
REM Handles pydantic-core compilation errors

echo.
echo 📚 Book Translator - Windows Installer
echo =======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Try Method 1: Pre-built wheels (fastest)
echo 🚀 Method 1: Installing with pre-built wheels...
echo.

pip install --only-binary :all: pydantic pydantic-core anthropic openai google-generativeai cohere groq 2>nul
if errorlevel 1 (
    echo ⚠️ Method 1 failed, trying Method 2...
    echo.
    goto method2
)

REM Continue with other packages
pip install gradio streamlit python-docx PyPDF2 ebooklib beautifulsoup4 requests tqdm colorama python-dotenv pillow
if errorlevel 1 (
    echo ⚠️ Some packages failed, trying Method 2...
    echo.
    goto method2
)

goto verify

:method2
REM Try Method 2: Windows-specific requirements
echo 🔄 Method 2: Installing with Windows-compatible versions...
echo.

pip install -r requirements-windows.txt
if errorlevel 1 (
    echo ❌ Method 2 failed
    echo.
    echo 💡 Please try manually:
    echo    1. Install Anaconda: https://www.anaconda.com/download
    echo    2. Or see WINDOWS_INSTALL_FIX.md for more solutions
    pause
    exit /b 1
)

:verify
echo.
echo ✅ Installation complete!
echo.
echo 🧪 Testing installation...
python -c "from book_translator import BookTranslator; print('✅ BookTranslator OK!')"
if errorlevel 1 (
    echo ⚠️ Import test failed, but you can still try running the app
)

echo.
echo 🎉 Setup complete! You can now:
echo.
echo    1. Run Web UI:   python ui_gradio.py
echo    2. Run CLI:      python cli.py --help
echo    3. Quick start:  run_ui.bat
echo.
pause
