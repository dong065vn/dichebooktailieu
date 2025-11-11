"""Smart Merging System - Ghép đoạn thông minh"""

import re
import logging
from typing import List, Dict
from .chunker import TextChunk

logger = logging.getLogger(__name__)


class SmartMerger:
    """
    Hệ thống ghép đoạn thông minh

    Đặc điểm:
    - Giữ nguyên cấu trúc và định dạng
    - Xử lý spacing và line breaks chính xác
    - Bảo toàn chapter markers và formatting
    - Đảm bảo văn bản liền mạch
    """

    def __init__(self, preserve_formatting: bool = True):
        """
        Args:
            preserve_formatting: Giữ nguyên formatting
        """
        self.preserve_formatting = preserve_formatting

    def merge_chunks(
        self,
        chunks: List[TextChunk],
        translations: List[str]
    ) -> str:
        """
        Ghép các chunks đã dịch thành văn bản hoàn chỉnh

        Args:
            chunks: List các TextChunk gốc
            translations: List các bản dịch tương ứng

        Returns:
            Văn bản đã dịch hoàn chỉnh
        """
        if len(chunks) != len(translations):
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks but {len(translations)} translations"
            )

        logger.info(f"Merging {len(chunks)} translated chunks")

        result_parts = []

        for i, (chunk, translation) in enumerate(zip(chunks, translations)):
            # Clean up translation
            clean_translation = self._clean_translation(translation)

            # Determine spacing based on chunk type and position
            spacing = self._determine_spacing(chunk, chunks, i)

            # Add spacing before if needed
            if i > 0 and spacing['before']:
                result_parts.append(spacing['before'])

            # Add the translated text
            result_parts.append(clean_translation)

            # Add spacing after if needed
            if spacing['after']:
                result_parts.append(spacing['after'])

        merged_text = ''.join(result_parts)

        # Final cleanup
        merged_text = self._final_cleanup(merged_text)

        logger.info(f"Merged text length: {len(merged_text)} characters")

        return merged_text

    def _clean_translation(self, translation: str) -> str:
        """Làm sạch bản dịch"""
        # Remove common LLM artifacts
        translation = translation.strip()

        # Remove markdown code blocks if present
        if translation.startswith('```') and translation.endswith('```'):
            lines = translation.split('\n')
            translation = '\n'.join(lines[1:-1])

        # Remove "Here is the translation:" type prefixes
        prefixes_to_remove = [
            r'^Here is the translation:?\s*',
            r'^Translation:?\s*',
            r'^Bản dịch:?\s*',
            r'^\[.*?\]\s*',
        ]

        for pattern in prefixes_to_remove:
            translation = re.sub(pattern, '', translation, flags=re.IGNORECASE)

        return translation.strip()

    def _determine_spacing(
        self,
        chunk: TextChunk,
        all_chunks: List[TextChunk],
        index: int
    ) -> Dict[str, str]:
        """Xác định spacing trước và sau chunk"""
        spacing = {'before': '', 'after': ''}

        if index == 0:
            # First chunk - no spacing before
            spacing['before'] = ''
        else:
            prev_chunk = all_chunks[index - 1]

            # Determine spacing based on chunk types
            if chunk.chunk_type == 'chapter':
                # Chapters should have double line break before
                spacing['before'] = '\n\n\n'
            elif chunk.chunk_type == 'section':
                # Sections should have double line break
                spacing['before'] = '\n\n'
            elif chunk.chunk_type == 'paragraph':
                # Paragraphs should have single or double line break
                if prev_chunk.chunk_type in ['chapter', 'section']:
                    spacing['before'] = '\n\n'
                else:
                    spacing['before'] = '\n\n'
            else:
                # Default spacing
                spacing['before'] = '\n'

        # Spacing after is usually handled by the next chunk's "before"
        # But we can set it for special cases
        if index == len(all_chunks) - 1:
            # Last chunk - add final newline
            spacing['after'] = '\n'

        return spacing

    def _final_cleanup(self, text: str) -> str:
        """Cleanup cuối cùng cho văn bản đã merge"""
        # Remove excessive line breaks (more than 3)
        text = re.sub(r'\n{4,}', '\n\n\n', text)

        # Remove trailing spaces on lines
        lines = text.split('\n')
        lines = [line.rstrip() for line in lines]
        text = '\n'.join(lines)

        # Ensure single newline at end
        text = text.rstrip() + '\n'

        return text

    def validate_merge(
        self,
        original_chunks: List[TextChunk],
        merged_text: str
    ) -> Dict:
        """
        Validate merged text

        Returns:
            Dict với thông tin validation
        """
        original_length = sum(len(chunk.text) for chunk in original_chunks)
        merged_length = len(merged_text)

        # Count line breaks
        original_breaks = sum(chunk.text.count('\n') for chunk in original_chunks)
        merged_breaks = merged_text.count('\n')

        validation = {
            'original_length': original_length,
            'merged_length': merged_length,
            'length_ratio': merged_length / original_length if original_length > 0 else 0,
            'original_line_breaks': original_breaks,
            'merged_line_breaks': merged_breaks,
            'has_content': len(merged_text.strip()) > 0,
        }

        # Check for issues
        issues = []

        if validation['length_ratio'] < 0.5:
            issues.append("Translated text significantly shorter than original")
        elif validation['length_ratio'] > 2.0:
            issues.append("Translated text significantly longer than original")

        if merged_breaks < original_breaks * 0.5:
            issues.append("Many line breaks lost in translation")

        if not validation['has_content']:
            issues.append("Merged text is empty!")

        validation['issues'] = issues
        validation['is_valid'] = len(issues) == 0

        return validation
