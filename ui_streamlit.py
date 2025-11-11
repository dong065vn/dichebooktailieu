#!/usr/bin/env python3
"""
Book Translator - Streamlit UI
Alternative UI với Streamlit
"""

import streamlit as st
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

# Page config
st.set_page_config(
    page_title="Book Translator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logging
logger = setup_logger(level=logging.INFO)

# Provider mapping
PROVIDERS = {
    'Groq Llama (FREE & FAST!) ⭐': {
        'class': GroqProvider,
        'model': 'llama-3.1-70b-versatile',
        'key': 'groq',
        'url': 'https://console.groq.com/',
        'format': 'gsk_...'
    },
    'Google Gemini Flash (Fast & Cheap)': {
        'class': GoogleProvider,
        'model': 'gemini-1.5-flash',
        'key': 'google',
        'url': 'https://makersuite.google.com/app/apikey',
        'format': 'AIza...'
    },
    'Google Gemini Pro': {
        'class': GoogleProvider,
        'model': 'gemini-1.5-pro',
        'key': 'google',
        'url': 'https://makersuite.google.com/app/apikey',
        'format': 'AIza...'
    },
    'OpenAI GPT-4o': {
        'class': OpenAIProvider,
        'model': 'gpt-4o',
        'key': 'openai',
        'url': 'https://platform.openai.com/api-keys',
        'format': 'sk-...'
    },
    'Anthropic Claude 3.5 Sonnet': {
        'class': AnthropicProvider,
        'model': 'claude-3-5-sonnet-20241022',
        'key': 'anthropic',
        'url': 'https://console.anthropic.com/',
        'format': 'sk-ant-...'
    },
    'DeepSeek (Cheap)': {
        'class': DeepSeekProvider,
        'model': 'deepseek-chat',
        'key': 'deepseek',
        'url': 'https://platform.deepseek.com/',
        'format': 'sk-...'
    },
}

LANGUAGES = {
    'English 🇬🇧': 'english',
    'Chinese 🇨🇳': 'chinese',
    'Russian 🇷🇺': 'russian',
}


def translate_file(
    uploaded_file,
    provider_name,
    api_key,
    source_lang,
    max_workers,
    max_chunk_size,
    min_chunk_size,
    context_size,
    temperature
):
    """Translate file"""

    # Save uploaded file temporarily
    temp_input = f"temp_input_{int(time.time())}{Path(uploaded_file.name).suffix}"
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Get provider info
    provider_info = PROVIDERS[provider_name]

    # Create provider
    llm_provider = provider_info['class'](
        api_key=api_key,
        model=provider_info['model'],
        temperature=temperature
    )

    # Create translator
    translator = BookTranslator(
        llm_provider=llm_provider,
        max_workers=max_workers,
        max_chunk_size=max_chunk_size,
        min_chunk_size=min_chunk_size,
        context_size=context_size,
        show_progress=False
    )

    # Output file
    output_file = f"translated_{int(time.time())}{Path(uploaded_file.name).suffix}"

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    chunks_done = [0]
    total_chunks = [0]

    def update_progress(chunk_id, total, translation):
        chunks_done[0] = chunk_id + 1
        total_chunks[0] = total
        percent = (chunk_id + 1) / total
        progress_bar.progress(percent)
        status_text.text(f"Translating chunk {chunk_id + 1}/{total}")

    # Translate
    status_text.text("Reading file...")
    start_time = time.time()

    translator.translate_file(
        input_file=temp_input,
        output_file=output_file,
        source_lang=LANGUAGES[source_lang],
        target_lang='vietnamese'
    )

    duration = time.time() - start_time

    # Cleanup
    os.remove(temp_input)

    # Get stats
    stats = translator.get_stats()

    progress_bar.progress(1.0)
    status_text.text("Complete!")

    return output_file, stats, duration


def main():
    """Main app"""

    # Header
    st.title("📚 Book Translator")
    st.markdown("**Dịch sách thông minh từ English, Chinese, Russian sang Tiếng Việt**")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Provider selection
        provider_name = st.selectbox(
            "🤖 LLM Provider",
            options=list(PROVIDERS.keys()),
            index=0,  # Default to Groq
            help="Groq khuyến nghị: FREE và nhanh nhất!"
        )

        provider_info = PROVIDERS[provider_name]

        # API Key
        st.markdown(f"**API Key** ([Get key]({provider_info['url']}))")
        api_key = st.text_input(
            "Enter API key",
            type="password",
            placeholder=f"Format: {provider_info['format']}",
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Language
        source_lang = st.selectbox(
            "📖 Source Language",
            options=list(LANGUAGES.keys()),
            index=0
        )

        st.markdown("---")

        # Workers
        st.markdown("**Performance**")
        max_workers = st.slider(
            "Max Workers",
            min_value=1,
            max_value=20,
            value=15 if 'Groq' in provider_name else 7,
            help="Groq: 15-20, Others: 5-7"
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Lower = more consistent"
        )

        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            max_chunk_size = st.slider(
                "Max Chunk Size",
                min_value=1000,
                max_value=8000,
                value=3000,
                step=500
            )

            min_chunk_size = st.slider(
                "Min Chunk Size",
                min_value=100,
                max_value=2000,
                value=500,
                step=100
            )

            context_size = st.slider(
                "Context Size",
                min_value=0,
                max_value=1000,
                value=300,
                step=50
            )

    # Main area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📥 Upload")
        uploaded_file = st.file_uploader(
            "Choose a book file",
            type=['txt', 'pdf', 'epub', 'docx', 'doc'],
            help="Supported formats: TXT, PDF, EPUB, DOCX"
        )

        if uploaded_file:
            st.success(f"✅ File loaded: {uploaded_file.name}")
            st.info(f"📄 Size: {uploaded_file.size / 1024:.1f} KB")

    with col2:
        st.header("📤 Output")

        if 'output_file' in st.session_state and st.session_state.output_file:
            with open(st.session_state.output_file, 'rb') as f:
                st.download_button(
                    label="⬇️ Download Translated File",
                    data=f,
                    file_name=st.session_state.output_file,
                    mime="application/octet-stream"
                )

            # Show stats
            if 'stats' in st.session_state:
                stats = st.session_state.stats
                duration = st.session_state.duration

                st.success("✅ Translation Complete!")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Chunks", stats['total_chunks'])
                with col_b:
                    st.metric("Success", stats['successful_chunks'])
                with col_c:
                    st.metric("Failed", stats['failed_chunks'])

                col_d, col_e = st.columns(2)
                with col_d:
                    st.metric("Characters", f"{stats['total_chars']:,}")
                with col_e:
                    st.metric("Speed", f"{stats['total_chars']/duration:.0f} c/s")

    # Translate button
    st.markdown("---")

    if st.button("🚀 Start Translation", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("❌ Please upload a file first!")
        elif not api_key:
            st.error("❌ Please enter your API key!")
        else:
            try:
                with st.spinner("Translating..."):
                    output_file, stats, duration = translate_file(
                        uploaded_file,
                        provider_name,
                        api_key,
                        source_lang,
                        max_workers,
                        max_chunk_size,
                        min_chunk_size,
                        context_size,
                        temperature
                    )

                    # Store in session state
                    st.session_state.output_file = output_file
                    st.session_state.stats = stats
                    st.session_state.duration = duration

                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                logger.error(f"Translation error: {e}", exc_info=True)

    # Instructions
    with st.expander("📖 How to Use"):
        st.markdown("""
        ### Quick Start

        1. **Choose Provider**: Select Groq (FREE!) or another provider
        2. **Get API Key**: Click the link next to API Key field
        3. **Upload File**: Support TXT, PDF, EPUB, DOCX
        4. **Configure**: Adjust workers and other settings
        5. **Translate**: Click "Start Translation"
        6. **Download**: Get your translated file

        ### Provider Recommendations

        | Provider | Speed | Cost | Quality |
        |----------|-------|------|---------|
        | **Groq** ⭐ | ⚡⚡⚡⚡⚡ | FREE | ⭐⭐⭐⭐ |
        | Gemini Flash | ⚡⚡⚡⚡ | $ | ⭐⭐⭐⭐ |
        | GPT-4o | ⚡⚡⚡ | $$ | ⭐⭐⭐⭐⭐ |
        | Claude 3.5 | ⚡⚡⚡ | $$$ | ⭐⭐⭐⭐⭐ |

        ### Tips

        - ✅ Use Groq for most cases (FREE & fast!)
        - ✅ Increase workers to 15-20 for Groq
        - ✅ Decrease workers to 5-7 for paid APIs
        - ✅ Test with small files first
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "Made with ❤️ for Vietnamese readers | "
        "[GitHub](https://github.com/yourusername/book-translator) | "
        "[Documentation](README.md)"
    )


if __name__ == "__main__":
    main()
