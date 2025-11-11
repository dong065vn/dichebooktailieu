#!/usr/bin/env python3
"""
Book Translator CLI
Công cụ dịch sách thông minh với LLM
"""

import os
import sys
import argparse
import logging
from pathlib import Path

from book_translator.core.translator import BookTranslator
from book_translator.llm_providers import (
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    CohereProvider,
    GroqProvider,
    DeepSeekProvider
)
from book_translator.utils.config import Config
from book_translator.utils.logger import setup_logger


PROVIDERS = {
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
    'google': GoogleProvider,
    'cohere': CohereProvider,
    'groq': GroqProvider,
    'deepseek': DeepSeekProvider,
}


def main():
    parser = argparse.ArgumentParser(
        description='Book Translator - Dịch sách thông minh với LLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dịch file TXT
  python cli.py input.txt output.txt --provider openai --api-key YOUR_KEY

  # Dịch file PDF từ tiếng Trung
  python cli.py input.pdf output.pdf --source-lang chinese --provider anthropic

  # Dịch với config file
  python cli.py input.epub output.epub --config config.json

  # Tạo config file mẫu
  python cli.py --create-config

Supported providers: openai, anthropic, google, cohere, groq, deepseek
Supported formats: txt, pdf, epub, docx
Supported languages: english, chinese, russian -> vietnamese
        """
    )

    # Main arguments
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path')

    # Provider settings
    parser.add_argument(
        '--provider',
        choices=list(PROVIDERS.keys()),
        default='openai',
        help='LLM provider to use (default: openai)'
    )
    parser.add_argument(
        '--api-key',
        help='API key for the provider'
    )
    parser.add_argument(
        '--model',
        help='Model name (default: depends on provider)'
    )

    # Language settings
    parser.add_argument(
        '--source-lang',
        choices=['english', 'chinese', 'russian'],
        default='english',
        help='Source language (default: english)'
    )
    parser.add_argument(
        '--target-lang',
        default='vietnamese',
        help='Target language (default: vietnamese)'
    )

    # Processing settings
    parser.add_argument(
        '--max-workers',
        type=int,
        default=5,
        help='Number of parallel workers (default: 5)'
    )
    parser.add_argument(
        '--max-chunk-size',
        type=int,
        default=3000,
        help='Maximum chunk size in characters (default: 3000)'
    )
    parser.add_argument(
        '--min-chunk-size',
        type=int,
        default=500,
        help='Minimum chunk size in characters (default: 500)'
    )

    # Config
    parser.add_argument(
        '--config',
        help='Path to config file (JSON)'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a default config file'
    )

    # Other
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--log-file',
        help='Log file path'
    )

    args = parser.parse_args()

    # Create config
    if args.create_config:
        Config.create_default_config_file('config.json')
        print("Created config.json - Please edit it with your API keys")
        return

    # Validate input
    if not args.input or not args.output:
        parser.error("input and output files are required (or use --create-config)")

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(level=log_level, log_file=args.log_file)

    # Load config
    config = Config(args.config)

    # Override with CLI arguments
    if args.provider:
        config.set('llm_provider', args.provider)
    if args.api_key:
        config.set('api_key', args.api_key)
    if args.model:
        config.set('model', args.model)
    if args.source_lang:
        config.set('source_lang', args.source_lang)
    if args.target_lang:
        config.set('target_lang', args.target_lang)
    if args.max_workers:
        config.set('max_workers', args.max_workers)
    if args.max_chunk_size:
        config.set('max_chunk_size', args.max_chunk_size)
    if args.min_chunk_size:
        config.set('min_chunk_size', args.min_chunk_size)

    # Validate config
    if not config.get('api_key'):
        logger.error("API key is required! Set it via --api-key or config file or environment variable")
        sys.exit(1)

    # Check input file
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)

    # Create LLM provider
    provider_class = PROVIDERS[config.get('llm_provider')]
    logger.info(f"Using provider: {config.get('llm_provider')}")

    # Get model name (use default if not specified)
    model_defaults = {
        'openai': 'gpt-4o',
        'anthropic': 'claude-3-5-sonnet-20241022',
        'google': 'gemini-1.5-pro',
        'cohere': 'command-r-plus',
        'groq': 'llama-3.1-70b-versatile',
        'deepseek': 'deepseek-chat',
    }
    model = config.get('model') or model_defaults[config.get('llm_provider')]

    try:
        llm_provider = provider_class(
            api_key=config.get('api_key'),
            model=model,
            temperature=config.get('temperature', 0.3),
            max_tokens=config.get('max_tokens', 4000)
        )
    except Exception as e:
        logger.error(f"Failed to initialize provider: {e}")
        sys.exit(1)

    # Create translator
    translator = BookTranslator(
        llm_provider=llm_provider,
        max_workers=config.get('max_workers', 5),
        max_chunk_size=config.get('max_chunk_size', 3000),
        min_chunk_size=config.get('min_chunk_size', 500),
        context_size=config.get('context_size', 300),
        show_progress=True
    )

    # Translate
    logger.info(f"Translating {args.input} -> {args.output}")
    logger.info(f"Language: {config.get('source_lang')} -> {config.get('target_lang')}")

    try:
        translator.translate_file(
            input_file=args.input,
            output_file=args.output,
            source_lang=config.get('source_lang'),
            target_lang=config.get('target_lang')
        )

        # Show stats
        stats = translator.get_stats()
        logger.info("\n" + "="*50)
        logger.info("TRANSLATION COMPLETE!")
        logger.info("="*50)
        logger.info(f"Total chunks: {stats['total_chunks']}")
        logger.info(f"Successful: {stats['successful_chunks']}")
        logger.info(f"Failed: {stats['failed_chunks']}")
        logger.info(f"Total characters: {stats['total_chars']}")
        if stats['end_time'] and stats['start_time']:
            duration = stats['end_time'] - stats['start_time']
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Speed: {stats['total_chars']/duration:.2f} chars/sec")
        logger.info(f"Output: {args.output}")
        logger.info("="*50)

    except Exception as e:
        logger.error(f"Translation failed: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == '__main__':
    main()
