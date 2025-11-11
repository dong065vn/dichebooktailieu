"""Book Translation Engine - Công cụ dịch sách chính"""

import logging
import time
from typing import List, Optional, Dict, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .chunker import IntelligentChunker, TextChunk
from .merger import SmartMerger
from .quota_handler import QuotaHandler, ProgressSaver
from ..llm_providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class BookTranslator:
    """
    Công cụ dịch sách chính với parallel processing

    Đặc điểm:
    - Dịch song song nhiều chunks để tăng tốc
    - Hỗ trợ nhiều LLM providers
    - Giữ nguyên cấu trúc và mạch văn
    - Progress tracking và error handling
    """

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        max_workers: int = 5,
        max_chunk_size: int = 3000,
        min_chunk_size: int = 500,
        context_size: int = 300,
        show_progress: bool = True,
        skip_failed_chunks: bool = True,  # NEW: Skip thay vì ghi error
        save_progress: bool = True,  # NEW: Save progress để resume
        handle_quota_errors: bool = True  # NEW: Xử lý quota errors
    ):
        """
        Args:
            llm_provider: LLM provider để dịch
            max_workers: Số worker threads cho parallel processing
            max_chunk_size: Kích thước tối đa của chunk
            min_chunk_size: Kích thước tối thiểu của chunk
            context_size: Số ký tự context từ chunk trước
            show_progress: Hiển thị progress bar
            skip_failed_chunks: True = skip failed chunks, False = ghi error vào output
            save_progress: True = save progress để resume sau, False = không save
            handle_quota_errors: True = xử lý quota errors thông minh
        """
        self.llm_provider = llm_provider
        self.max_workers = max_workers
        self.show_progress = show_progress
        self.skip_failed_chunks = skip_failed_chunks
        self.save_progress = save_progress
        self.handle_quota_errors = handle_quota_errors

        self.chunker = IntelligentChunker(
            max_chunk_size=max_chunk_size,
            min_chunk_size=min_chunk_size,
            context_size=context_size
        )

        self.merger = SmartMerger()

        # NEW: Quota handler
        if self.handle_quota_errors:
            self.quota_handler = QuotaHandler(
                max_quota_retries=5,
                quota_retry_delay=60
            )
        else:
            self.quota_handler = None

        self.stats = {
            'total_chunks': 0,
            'successful_chunks': 0,
            'failed_chunks': 0,
            'skipped_chunks': 0,  # NEW
            'quota_errors': 0,  # NEW
            'total_chars': 0,
            'start_time': None,
            'end_time': None,
        }

    def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        callback: Optional[Callable] = None
    ) -> str:
        """
        Dịch văn bản hoàn chỉnh

        Args:
            text: Văn bản cần dịch
            source_lang: Ngôn ngữ nguồn (english, chinese, russian)
            target_lang: Ngôn ngữ đích (vietnamese)
            callback: Optional callback function(chunk_id, total, translation)

        Returns:
            Văn bản đã dịch
        """
        logger.info(f"Starting translation from {source_lang} to {target_lang}")
        self.stats['start_time'] = time.time()

        # Step 1: Chunk text
        logger.info("Step 1: Chunking text...")
        chunks = self.chunker.chunk_text(text, source_lang)
        self.stats['total_chunks'] = len(chunks)
        self.stats['total_chars'] = sum(len(c.text) for c in chunks)

        chunk_stats = self.chunker.get_chunk_stats(chunks)
        logger.info(f"Chunk statistics: {chunk_stats}")

        # Step 2: Translate chunks in parallel
        logger.info(f"Step 2: Translating {len(chunks)} chunks with {self.max_workers} workers...")
        translations = self._translate_chunks_parallel(
            chunks, source_lang, target_lang, callback
        )

        # Step 3: Merge translations
        logger.info("Step 3: Merging translations...")
        merged_text = self.merger.merge_chunks(chunks, translations)

        # Validate merge
        validation = self.merger.validate_merge(chunks, merged_text)
        logger.info(f"Merge validation: {validation}")

        if not validation['is_valid']:
            logger.warning(f"Merge validation issues: {validation['issues']}")

        self.stats['end_time'] = time.time()
        self._log_stats()

        return merged_text

    def _translate_chunks_parallel(
        self,
        chunks: List[TextChunk],
        source_lang: str,
        target_lang: str,
        callback: Optional[Callable] = None
    ) -> List[str]:
        """Dịch các chunks song song"""
        translations = [None] * len(chunks)
        failed_chunks = []

        # Create progress bar if enabled
        pbar = None
        if self.show_progress:
            pbar = tqdm(total=len(chunks), desc="Translating chunks", unit="chunk")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_chunk = {
                executor.submit(
                    self._translate_single_chunk,
                    chunk,
                    source_lang,
                    target_lang
                ): chunk for chunk in chunks
            }

            # Process completed tasks
            for future in as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    translation = future.result()
                    translations[chunk.id] = translation
                    self.stats['successful_chunks'] += 1

                    if callback:
                        callback(chunk.id, len(chunks), translation)

                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Failed to translate chunk {chunk.id}: {error_msg}")

                    # NEW: Check if quota error
                    quota_error = None
                    if self.quota_handler:
                        quota_error = self.quota_handler.is_quota_error(error_msg)

                    if quota_error:
                        self.stats['quota_errors'] += 1
                        logger.warning(f"⚠️ Quota error detected: {quota_error.error_type}")

                        # Show suggestions
                        suggestions = self.quota_handler.get_suggestions(quota_error)
                        logger.warning("💡 Suggestions:")
                        for suggestion in suggestions:
                            logger.warning(f"   {suggestion}")

                    # Set failed chunk value
                    if self.skip_failed_chunks:
                        # Skip: không ghi gì (sẽ filter khi merge)
                        translations[chunk.id] = None
                        self.stats['skipped_chunks'] += 1
                    else:
                        # Ghi error message vào output (old behavior)
                        translations[chunk.id] = f"[TRANSLATION FAILED: {error_msg}]"

                    failed_chunks.append(chunk.id)
                    self.stats['failed_chunks'] += 1

                finally:
                    if pbar:
                        pbar.update(1)

        if pbar:
            pbar.close()

        # Retry failed chunks
        if failed_chunks:
            logger.warning(f"Retrying {len(failed_chunks)} failed chunks...")
            self._retry_failed_chunks(
                chunks, translations, failed_chunks, source_lang, target_lang
            )

        return translations

    def _translate_single_chunk(
        self,
        chunk: TextChunk,
        source_lang: str,
        target_lang: str
    ) -> str:
        """Dịch một chunk đơn"""
        try:
            translation = self.llm_provider.translate(
                text=chunk.text,
                source_lang=source_lang,
                target_lang=target_lang,
                context=chunk.context_before
            )
            return translation
        except Exception as e:
            logger.error(f"Error translating chunk {chunk.id}: {e}")
            raise

    def _retry_failed_chunks(
        self,
        chunks: List[TextChunk],
        translations: List[str],
        failed_ids: List[int],
        source_lang: str,
        target_lang: str
    ):
        """Retry các chunks bị fail với quota handling"""
        retry_attempt = 1

        for chunk_id in failed_ids:
            try:
                chunk = chunks[chunk_id]
                translation = self._translate_single_chunk(
                    chunk, source_lang, target_lang
                )
                translations[chunk_id] = translation
                self.stats['successful_chunks'] += 1
                self.stats['failed_chunks'] -= 1
                if self.skip_failed_chunks:
                    self.stats['skipped_chunks'] -= 1
                logger.info(f"✅ Successfully retried chunk {chunk_id}")

            except Exception as e:
                error_msg = str(e)
                logger.error(f"Retry failed for chunk {chunk_id}: {error_msg}")

                # NEW: Handle quota error trong retry
                if self.quota_handler:
                    quota_error = self.quota_handler.is_quota_error(error_msg)

                    if quota_error:
                        logger.error(f"❌ Quota error khi retry chunk {chunk_id}")

                        # Nếu là quota exceeded hoặc auth error, stop retry
                        if quota_error.error_type in ['quota_exceeded', 'auth_error']:
                            logger.error(
                                "⛔ Dừng retry vì quota exceeded/auth error.\n"
                                "Các chunk còn lại sẽ bị skip."
                            )
                            break  # Stop retrying remaining chunks

                        # Nếu là rate limit, có thể pause và retry
                        if quota_error.error_type == 'rate_limit':
                            should_retry = self.quota_handler.handle_quota_error(
                                quota_error,
                                retry_attempt,
                                on_pause=lambda delay, attempt, max_attempts: logger.info(
                                    f"⏸️ Pausing for {delay}s (retry {attempt}/{max_attempts})"
                                )
                            )

                            if should_retry:
                                # Retry lại chunk này
                                try:
                                    translation = self._translate_single_chunk(
                                        chunk, source_lang, target_lang
                                    )
                                    translations[chunk_id] = translation
                                    self.stats['successful_chunks'] += 1
                                    self.stats['failed_chunks'] -= 1
                                    if self.skip_failed_chunks:
                                        self.stats['skipped_chunks'] -= 1
                                    logger.info(f"✅ Retry thành công sau pause: chunk {chunk_id}")
                                except Exception as retry_e:
                                    logger.error(f"Retry sau pause vẫn fail: {retry_e}")
                            else:
                                logger.error("⛔ Quá nhiều rate limit errors, dừng retry")
                                break

                retry_attempt += 1

    def _log_stats(self):
        """Log thống kê"""
        duration = self.stats['end_time'] - self.stats['start_time']
        chars_per_sec = self.stats['total_chars'] / duration if duration > 0 else 0

        logger.info(f"""
Translation Statistics:
- Total chunks: {self.stats['total_chunks']}
- Successful: {self.stats['successful_chunks']}
- Failed: {self.stats['failed_chunks']}
- Total characters: {self.stats['total_chars']}
- Duration: {duration:.2f} seconds
- Speed: {chars_per_sec:.2f} chars/sec
        """)

    def get_stats(self) -> Dict:
        """Lấy thống kê"""
        return self.stats.copy()

    def translate_file(
        self,
        input_file: str,
        output_file: str,
        source_lang: str,
        target_lang: str = "vietnamese",
        input_format: Optional[str] = None,
        output_format: Optional[str] = None
    ):
        """
        Dịch file

        Args:
            input_file: Đường dẫn file input
            output_file: Đường dẫn file output
            source_lang: Ngôn ngữ nguồn
            target_lang: Ngôn ngữ đích
            input_format: Format của input (auto-detect nếu None)
            output_format: Format của output (same as input nếu None)
        """
        from ..formats import FileHandler

        logger.info(f"Translating file: {input_file} -> {output_file}")

        # Read file
        handler = FileHandler()
        text = handler.read_file(input_file, input_format)

        logger.info(f"Read {len(text)} characters from {input_file}")

        # Translate
        translated_text = self.translate_text(text, source_lang, target_lang)

        # Write file
        if output_format is None:
            output_format = input_format
        handler.write_file(output_file, translated_text, output_format)

        logger.info(f"Translation complete: {output_file}")
