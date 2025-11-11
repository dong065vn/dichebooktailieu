#!/usr/bin/env python3
"""
Example usage of Book Translator
"""

import os
from book_translator import BookTranslator
from book_translator.llm_providers import (
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider
)


def example_basic_translation():
    """Ví dụ cơ bản: Dịch file TXT"""
    print("Example 1: Basic Translation with OpenAI")
    print("-" * 50)

    # Khởi tạo provider
    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    # Khởi tạo translator
    translator = BookTranslator(
        llm_provider=provider,
        max_workers=5
    )

    # Dịch file
    translator.translate_file(
        input_file="input.txt",
        output_file="output.txt",
        source_lang="english",
        target_lang="vietnamese"
    )

    print("Translation complete!")
    print()


def example_anthropic_claude():
    """Ví dụ với Anthropic Claude"""
    print("Example 2: Translation with Claude")
    print("-" * 50)

    provider = AnthropicProvider(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-5-sonnet-20241022"
    )

    translator = BookTranslator(
        llm_provider=provider,
        max_workers=5
    )

    translator.translate_file(
        input_file="input.txt",
        output_file="output_claude.txt",
        source_lang="english"
    )

    print("Translation complete!")
    print()


def example_groq_fast():
    """Ví dụ với Groq (cực nhanh!)"""
    print("Example 3: Fast Translation with Groq")
    print("-" * 50)

    provider = GroqProvider(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-70b-versatile"
    )

    # Sử dụng nhiều workers hơn vì Groq nhanh
    translator = BookTranslator(
        llm_provider=provider,
        max_workers=10  # Groq xử lý nhanh, có thể dùng nhiều workers
    )

    translator.translate_file(
        input_file="input.txt",
        output_file="output_groq.txt",
        source_lang="english"
    )

    print("Translation complete!")
    print()


def example_text_translation():
    """Ví dụ: Dịch text trực tiếp"""
    print("Example 4: Direct Text Translation")
    print("-" * 50)

    text = """
    Chapter 1: The Beginning

    It was a dark and stormy night. The wind howled through the trees,
    and rain pounded against the windows. Inside the old mansion,
    a mysterious figure sat by the fireplace, reading an ancient book.

    The book contained secrets that had been hidden for centuries,
    waiting for the right person to discover them.
    """

    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    translator = BookTranslator(llm_provider=provider)

    translated = translator.translate_text(
        text=text,
        source_lang="english",
        target_lang="vietnamese"
    )

    print("Original:")
    print(text)
    print("\nTranslated:")
    print(translated)
    print()


def example_with_callback():
    """Ví dụ với progress callback"""
    print("Example 5: Translation with Progress Callback")
    print("-" * 50)

    def progress_callback(chunk_id, total, translation):
        percentage = (chunk_id + 1) / total * 100
        print(f"Progress: {percentage:.1f}% ({chunk_id + 1}/{total} chunks)")

    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    translator = BookTranslator(llm_provider=provider, max_workers=3)

    text = "This is a sample text. " * 1000  # Long text

    translated = translator.translate_text(
        text=text,
        source_lang="english",
        callback=progress_callback
    )

    print("\nTranslation complete!")
    print()


def example_pdf_translation():
    """Ví dụ: Dịch file PDF"""
    print("Example 6: PDF Translation")
    print("-" * 50)

    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    translator = BookTranslator(llm_provider=provider)

    translator.translate_file(
        input_file="book.pdf",
        output_file="book_vi.pdf",
        source_lang="english"
    )

    print("PDF translation complete!")
    print()


def example_chinese_translation():
    """Ví dụ: Dịch từ tiếng Trung"""
    print("Example 7: Chinese to Vietnamese Translation")
    print("-" * 50)

    chinese_text = """
    第一章：开始

    这是一个黑暗而暴风雨的夜晚。风在树间呼啸，
    雨点敲打着窗户。在老宅子里，一个神秘的人物
    坐在壁炉旁，读着一本古老的书。
    """

    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    translator = BookTranslator(llm_provider=provider)

    translated = translator.translate_text(
        text=chinese_text,
        source_lang="chinese",
        target_lang="vietnamese"
    )

    print("Original (Chinese):")
    print(chinese_text)
    print("\nTranslated (Vietnamese):")
    print(translated)
    print()


def example_custom_chunking():
    """Ví dụ: Custom chunking parameters"""
    print("Example 8: Custom Chunking Parameters")
    print("-" * 50)

    provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    # Tùy chỉnh chunking
    translator = BookTranslator(
        llm_provider=provider,
        max_chunk_size=5000,  # Chunks lớn hơn
        min_chunk_size=1000,  # Chunks nhỏ nhất
        context_size=500,     # Context dài hơn
        max_workers=5
    )

    translator.translate_file(
        input_file="input.txt",
        output_file="output_custom.txt",
        source_lang="english"
    )

    # Xem statistics
    stats = translator.get_stats()
    print(f"\nStatistics:")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Successful: {stats['successful_chunks']}")
    print(f"Failed: {stats['failed_chunks']}")
    print(f"Total characters: {stats['total_chars']}")
    if stats['end_time'] and stats['start_time']:
        duration = stats['end_time'] - stats['start_time']
        print(f"Duration: {duration:.2f} seconds")
        print(f"Speed: {stats['total_chars']/duration:.2f} chars/sec")
    print()


if __name__ == "__main__":
    print("Book Translator - Example Usage")
    print("=" * 50)
    print()

    # Uncomment examples you want to run:

    # example_basic_translation()
    # example_anthropic_claude()
    # example_groq_fast()
    # example_text_translation()
    # example_with_callback()
    # example_pdf_translation()
    # example_chinese_translation()
    # example_custom_chunking()

    print("\nTo run examples, uncomment the function calls above")
    print("Make sure to set your API keys in environment variables:")
    print("  export OPENAI_API_KEY='your-key'")
    print("  export ANTHROPIC_API_KEY='your-key'")
    print("  export GROQ_API_KEY='your-key'")
