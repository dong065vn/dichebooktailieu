#!/usr/bin/env python3
"""
Book Translator - Gradio Web UI
Giao diện web hiện đại với đầy đủ tính năng
"""

import gradio as gr
import os
import time
from pathlib import Path
import logging

from book_translator.core.translator import BookTranslator
from book_translator.llm_providers import (
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    CohereProvider,
    GroqProvider,
    DeepSeekProvider
)
from book_translator.utils.logger import setup_logger

# Setup logging
logger = setup_logger(level=logging.INFO)

# Provider mapping
PROVIDERS = {
    'OpenAI (GPT-4o, GPT-4)': ('openai', OpenAIProvider, 'gpt-4o'),
    'Google Gemini (Fast & Cheap)': ('google', GoogleProvider, 'gemini-1.5-flash'),
    'Google Gemini Pro': ('google', GoogleProvider, 'gemini-1.5-pro'),
    'Anthropic Claude 3.5 Sonnet': ('anthropic', AnthropicProvider, 'claude-3-5-sonnet-20241022'),
    'Groq Llama (FREE & FAST!)': ('groq', GroqProvider, 'llama-3.1-70b-versatile'),
    'DeepSeek (Cheap)': ('deepseek', DeepSeekProvider, 'deepseek-chat'),
    'Cohere Command': ('cohere', CohereProvider, 'command-r-plus'),
}

# Language mapping
LANGUAGES = {
    'English': 'english',
    'Chinese (中文)': 'chinese',
    'Russian (Русский)': 'russian',
}

# Global state
current_translator = None
translation_stats = {}


def translate_file(
    input_file,
    provider_name,
    api_key,
    source_lang,
    target_lang,
    max_workers,
    max_chunk_size,
    min_chunk_size,
    context_size,
    temperature,
    progress=gr.Progress()
):
    """Main translation function"""

    if input_file is None:
        return None, "❌ Please upload a file first!", ""

    if not api_key or api_key.strip() == "":
        return None, "❌ Please enter your API key!", ""

    try:
        progress(0, desc="Initializing...")

        # Get provider info
        provider_key, provider_class, default_model = PROVIDERS[provider_name]
        source_lang_code = LANGUAGES[source_lang]

        # Create provider
        progress(0.1, desc=f"Connecting to {provider_name}...")
        llm_provider = provider_class(
            api_key=api_key.strip(),
            model=default_model,
            temperature=temperature
        )

        # Create translator
        global current_translator
        current_translator = BookTranslator(
            llm_provider=llm_provider,
            max_workers=int(max_workers),
            max_chunk_size=int(max_chunk_size),
            min_chunk_size=int(min_chunk_size),
            context_size=int(context_size),
            show_progress=False  # We'll use Gradio progress
        )

        # Get file paths
        input_path = input_file.name
        file_ext = Path(input_path).suffix
        output_path = f"translated_{int(time.time())}{file_ext}"

        # Progress callback
        chunks_done = [0]
        total_chunks = [0]

        def update_progress(chunk_id, total, translation):
            chunks_done[0] = chunk_id + 1
            total_chunks[0] = total
            percent = (chunk_id + 1) / total
            progress(percent, desc=f"Translating chunk {chunk_id + 1}/{total}")

        progress(0.2, desc="Reading and chunking file...")

        # Translate
        start_time = time.time()
        current_translator.translate_file(
            input_file=input_path,
            output_file=output_path,
            source_lang=source_lang_code,
            target_lang='vietnamese'
        )

        duration = time.time() - start_time

        # Get stats
        global translation_stats
        translation_stats = current_translator.get_stats()

        # Create stats message
        stats_msg = f"""
✅ **Translation Complete!**

📊 **Statistics:**
- Total chunks: {translation_stats['total_chunks']}
- Successful: {translation_stats['successful_chunks']}
- Failed: {translation_stats['failed_chunks']}
- Total characters: {translation_stats['total_chars']:,}
- Duration: {duration:.1f} seconds
- Speed: {translation_stats['total_chars']/duration:.1f} chars/sec

📁 **Output:** {output_path}
        """

        progress(1.0, desc="Done!")

        return output_path, stats_msg, output_path

    except Exception as e:
        error_msg = f"❌ **Error:** {str(e)}\n\nPlease check:\n- API key is correct\n- File format is supported\n- Internet connection is stable"
        logger.error(f"Translation error: {e}", exc_info=True)
        return None, error_msg, ""


def get_api_key_help(provider_name):
    """Get help text for API key"""
    helps = {
        'OpenAI (GPT-4o, GPT-4)': "Get your API key at: https://platform.openai.com/api-keys\nFormat: sk-...",
        'Google Gemini (Fast & Cheap)': "Get your API key at: https://makersuite.google.com/app/apikey\nFormat: AIza...",
        'Google Gemini Pro': "Get your API key at: https://makersuite.google.com/app/apikey\nFormat: AIza...",
        'Anthropic Claude 3.5 Sonnet': "Get your API key at: https://console.anthropic.com/\nFormat: sk-ant-...",
        'Groq Llama (FREE & FAST!)': "Get your FREE API key at: https://console.groq.com/\nFormat: gsk_...",
        'DeepSeek (Cheap)': "Get your API key at: https://platform.deepseek.com/\nFormat: sk-...",
        'Cohere Command': "Get your API key at: https://dashboard.cohere.com/\nFormat: varies",
    }
    return helps.get(provider_name, "Enter your API key")


# Create Gradio Interface
def create_ui():
    """Create Gradio UI"""

    with gr.Blocks(
        title="Book Translator - Dịch Sách Thông Minh",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .main-title {
            text-align: center;
            margin-bottom: 2rem;
        }
        """
    ) as demo:

        # Header
        gr.Markdown(
            """
            # 📚 Book Translator - Dịch Sách Thông Minh

            Dịch sách từ Tiếng Anh, Tiếng Trung, Tiếng Nga sang Tiếng Việt với AI

            🚀 **Tính năng:** Chia đoạn thông minh • Dịch song song • Giữ nguyên mạch văn
            """,
            elem_classes="main-title"
        )

        with gr.Tabs():
            # Tab 1: Translation
            with gr.TabItem("🔄 Dịch Sách"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📥 Input")

                        input_file = gr.File(
                            label="Upload File",
                            file_types=['.txt', '.pdf', '.epub', '.docx', '.doc'],
                            type="filepath"
                        )

                        source_lang = gr.Dropdown(
                            choices=list(LANGUAGES.keys()),
                            value='English',
                            label="Ngôn ngữ nguồn",
                            info="Ngôn ngữ của sách gốc"
                        )

                        gr.Markdown("### 🤖 LLM Provider")

                        provider = gr.Dropdown(
                            choices=list(PROVIDERS.keys()),
                            value='Groq Llama (FREE & FAST!)',
                            label="Chọn Provider",
                            info="Groq khuyến nghị: Miễn phí & nhanh nhất!"
                        )

                        api_key = gr.Textbox(
                            label="API Key",
                            type="password",
                            placeholder="Nhập API key của bạn...",
                            info="API key sẽ không được lưu"
                        )

                        api_help = gr.Markdown(
                            get_api_key_help('Groq Llama (FREE & FAST!)'),
                            elem_classes="api-help"
                        )

                        # Update help when provider changes
                        provider.change(
                            fn=get_api_key_help,
                            inputs=[provider],
                            outputs=[api_help]
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### ⚙️ Settings")

                        with gr.Accordion("Cài đặt cơ bản", open=True):
                            max_workers = gr.Slider(
                                minimum=1,
                                maximum=20,
                                value=7,
                                step=1,
                                label="Max Workers (Số luồng song song)",
                                info="Groq: 15-20, OpenAI/Google: 5-7"
                            )

                            temperature = gr.Slider(
                                minimum=0.0,
                                maximum=1.0,
                                value=0.3,
                                step=0.1,
                                label="Temperature",
                                info="Thấp = nhất quán, Cao = sáng tạo"
                            )

                        with gr.Accordion("Cài đặt nâng cao", open=False):
                            max_chunk_size = gr.Slider(
                                minimum=1000,
                                maximum=8000,
                                value=3000,
                                step=500,
                                label="Max Chunk Size",
                                info="Kích thước chunk tối đa (chars)"
                            )

                            min_chunk_size = gr.Slider(
                                minimum=100,
                                maximum=2000,
                                value=500,
                                step=100,
                                label="Min Chunk Size",
                                info="Kích thước chunk tối thiểu (chars)"
                            )

                            context_size = gr.Slider(
                                minimum=0,
                                maximum=1000,
                                value=300,
                                step=50,
                                label="Context Size",
                                info="Số chars context từ chunk trước"
                            )

                        translate_btn = gr.Button(
                            "🚀 Bắt Đầu Dịch",
                            variant="primary",
                            size="lg"
                        )

                # Output area
                gr.Markdown("### 📤 Output")

                with gr.Row():
                    with gr.Column():
                        status_box = gr.Markdown(
                            "Chọn file và nhấn 'Bắt Đầu Dịch' để bắt đầu...",
                            elem_classes="status-box"
                        )

                with gr.Row():
                    output_file = gr.File(
                        label="📥 Download File Đã Dịch",
                        visible=True
                    )

                # Translation action
                translate_btn.click(
                    fn=translate_file,
                    inputs=[
                        input_file,
                        provider,
                        api_key,
                        source_lang,
                        gr.Textbox(value="Vietnamese", visible=False),  # target_lang
                        max_workers,
                        max_chunk_size,
                        min_chunk_size,
                        context_size,
                        temperature
                    ],
                    outputs=[output_file, status_box, gr.Textbox(visible=False)]
                )

            # Tab 2: Guide
            with gr.TabItem("📖 Hướng Dẫn"):
                gr.Markdown(
                    """
                    ## 🚀 Hướng Dẫn Sử Dụng

                    ### Bước 1: Upload File
                    - Hỗ trợ: TXT, PDF, EPUB, DOCX
                    - Kích thước: Không giới hạn

                    ### Bước 2: Chọn Provider & API Key

                    #### 🎯 Khuyến Nghị Providers:

                    | Provider | Ưu Điểm | Nhược Điểm | Giá | API Key |
                    |----------|---------|------------|-----|---------|
                    | **Groq Llama** ⭐ | FREE, Cực nhanh | - | 💰 FREE | [Get Key](https://console.groq.com/) |
                    | **Gemini Flash** | Nhanh, Rẻ | - | 💰 $0.5/sách | [Get Key](https://makersuite.google.com/app/apikey) |
                    | **GPT-4o** | Chất lượng cao | Hơi chậm | 💰💰 $3-5/sách | [Get Key](https://platform.openai.com/api-keys) |
                    | **Claude 3.5** | Tốt nhất văn học | Đắt | 💰💰💰 $5-7/sách | [Get Key](https://console.anthropic.com/) |

                    ### Bước 3: Cài Đặt

                    **Max Workers:**
                    - Groq: 15-20 (rất nhanh, không giới hạn)
                    - Google/OpenAI: 5-7 (tránh rate limit)

                    **Temperature:**
                    - 0.2-0.3: Dịch nhất quán (khuyến nghị)
                    - 0.4-0.7: Cân bằng
                    - 0.8-1.0: Sáng tạo (không khuyến nghị)

                    ### Bước 4: Bắt Đầu Dịch

                    1. Click "Bắt Đầu Dịch"
                    2. Đợi progress bar
                    3. Download file đã dịch

                    ## 💡 Tips

                    - ✅ Dùng Groq cho hầu hết trường hợp (FREE!)
                    - ✅ Test với file nhỏ trước
                    - ✅ Tăng workers với Groq (15-20)
                    - ✅ Giảm workers với paid APIs (5-7)

                    ## ❓ Troubleshooting

                    **Lỗi API Key:**
                    - Check API key đúng format
                    - Verify key còn quota

                    **Lỗi Rate Limit:**
                    - Giảm max_workers
                    - Đổi sang Groq (unlimited)

                    **Dịch chậm:**
                    - Dùng Groq (nhanh nhất)
                    - Tăng max_workers
                    - Dùng Gemini Flash
                    """
                )

            # Tab 3: About
            with gr.TabItem("ℹ️ About"):
                gr.Markdown(
                    """
                    ## 📚 Book Translator v1.0

                    ### ✨ Tính Năng

                    - 🧠 **Intelligent Chunking**: Tự động nhận diện chapters, sections, paragraphs
                    - ⚡ **Parallel Processing**: Dịch nhiều đoạn cùng lúc, nhanh gấp 5-10 lần
                    - 🔗 **Context Preservation**: Giữ nguyên mạch văn giữa các đoạn
                    - 📄 **Multi-Format**: Hỗ trợ TXT, PDF, EPUB, DOCX
                    - 🤖 **Multi-LLM**: Tích hợp 6 providers (OpenAI, Google, Anthropic, Groq, etc.)

                    ### 🌍 Ngôn Ngữ

                    **Nguồn:** English, Chinese (中文), Russian (Русский)

                    **Đích:** Vietnamese (Tiếng Việt)

                    ### 🛠️ Technical Stack

                    - Python 3.8+
                    - Gradio (Web UI)
                    - OpenAI, Anthropic, Google AI SDKs
                    - PyPDF2, pdfplumber (PDF)
                    - ebooklib (EPUB)
                    - python-docx (DOCX)

                    ### 📊 Performance

                    **Sách 100,000 từ (500,000 chars):**
                    - Groq: ~10-15 phút
                    - Gemini Flash: ~15-20 phút
                    - GPT-4o: ~20-30 phút

                    ### 📝 License

                    MIT License

                    ### 🙏 Credits

                    Developed with ❤️ for Vietnamese readers

                    ---

                    **GitHub:** [Book Translator](https://github.com/yourusername/book-translator)

                    **Docs:** See README.md, USAGE_GUIDE.md, CONFIG_GUIDE.md
                    """
                )

        # Footer
        gr.Markdown(
            """
            ---
            💡 **Tip:** Dùng Groq provider để dịch miễn phí và nhanh nhất! |
            📚 [Documentation](README.md) |
            🐛 [Report Issues](https://github.com/yourusername/book-translator/issues)
            """
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()

    # Launch with options
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to create public link
        show_error=True,
        quiet=False
    )
