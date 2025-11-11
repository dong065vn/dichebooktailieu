#!/bin/bash
# Quick launcher for Book Translator UI

echo "📚 Book Translator - UI Launcher"
echo "================================"
echo ""
echo "Chọn UI bạn muốn chạy:"
echo ""
echo "1. Gradio UI (Khuyến nghị) - Modern, đẹp, dễ dùng"
echo "2. Streamlit UI - Professional, nhiều tính năng"
echo "3. Exit"
echo ""

read -p "Nhập lựa chọn (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Đang khởi động Gradio UI..."
        echo "Mở trình duyệt tại: http://localhost:7860"
        echo ""
        python ui_gradio.py
        ;;
    2)
        echo ""
        echo "🚀 Đang khởi động Streamlit UI..."
        echo "Mở trình duyệt tại: http://localhost:8501"
        echo ""
        streamlit run ui_streamlit.py
        ;;
    3)
        echo "Tạm biệt!"
        exit 0
        ;;
    *)
        echo "❌ Lựa chọn không hợp lệ!"
        exit 1
        ;;
esac
