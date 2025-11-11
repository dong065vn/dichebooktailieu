@echo off
REM Quick launcher for Book Translator UI (Windows)

echo.
echo 📚 Book Translator - UI Launcher
echo ================================
echo.
echo Chọn UI bạn muốn chạy:
echo.
echo 1. Gradio UI (Khuyến nghị) - Modern, đẹp, dễ dùng
echo 2. Streamlit UI - Professional, nhiều tính năng
echo 3. Exit
echo.

set /p choice="Nhập lựa chọn (1-3): "

if "%choice%"=="1" goto gradio
if "%choice%"=="2" goto streamlit
if "%choice%"=="3" goto exit
goto invalid

:gradio
echo.
echo 🚀 Đang khởi động Gradio UI...
echo Mở trình duyệt tại: http://localhost:7860
echo.
python ui_gradio.py
goto end

:streamlit
echo.
echo 🚀 Đang khởi động Streamlit UI...
echo Mở trình duyệt tại: http://localhost:8501
echo.
streamlit run ui_streamlit.py
goto end

:exit
echo Tạm biệt!
goto end

:invalid
echo ❌ Lựa chọn không hợp lệ!
goto end

:end
pause
