"""Intelligent Text Chunking System - Chia đoạn thông minh"""

import re
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    """Đại diện cho một đoạn văn bản"""
    id: int
    text: str
    start_pos: int
    end_pos: int
    chunk_type: str  # 'chapter', 'paragraph', 'section'
    metadata: Dict
    context_before: str = ""  # Context từ chunk trước để giữ mạch


class IntelligentChunker:
    """
    Hệ thống chia đoạn thông minh cho sách

    Đặc điểm:
    - Nhận diện chapter, section, paragraph
    - Giữ nguyên cấu trúc và format
    - Tạo chunks tối ưu cho translation
    - Bảo toàn context giữa các chunks
    """

    def __init__(
        self,
        max_chunk_size: int = 3000,
        min_chunk_size: int = 500,
        context_size: int = 300,
        preserve_formatting: bool = True
    ):
        """
        Args:
            max_chunk_size: Kích thước tối đa của chunk (chars)
            min_chunk_size: Kích thước tối thiểu của chunk (chars)
            context_size: Số ký tự context từ chunk trước
            preserve_formatting: Giữ nguyên formatting
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.context_size = context_size
        self.preserve_formatting = preserve_formatting

        # Patterns để nhận diện cấu trúc
        self.chapter_patterns = [
            r'^Chapter\s+\d+',
            r'^CHAPTER\s+\d+',
            r'^Chương\s+\d+',
            r'^\d+\.\s+[A-Z]',
            r'^第[一二三四五六七八九十百千\d]+章',  # Chinese chapters
            r'^Глава\s+\d+',  # Russian chapters
            r'^Part\s+\d+',
            r'^PART\s+\d+',
        ]

        self.section_patterns = [
            r'^\#{1,3}\s+',  # Markdown headers
            r'^[A-Z][A-Z\s]{3,}$',  # ALL CAPS titles
            r'^\d+\.\d+',  # Numbered sections
        ]

    def chunk_text(self, text: str, source_lang: str = "english") -> List[TextChunk]:
        """
        Chia văn bản thành các chunks thông minh

        Args:
            text: Văn bản đầy đủ
            source_lang: Ngôn ngữ nguồn

        Returns:
            List các TextChunk
        """
        logger.info(f"Chunking text of length {len(text)} characters")

        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Phát hiện các điểm chia tự nhiên
        split_points = self._find_split_points(text)

        # Tạo chunks từ split points
        chunks = self._create_chunks(text, split_points)

        # Thêm context cho mỗi chunk
        chunks = self._add_context(chunks)

        logger.info(f"Created {len(chunks)} chunks")
        return chunks

    def _find_split_points(self, text: str) -> List[Tuple[int, str, int]]:
        """
        Tìm các điểm chia tự nhiên trong văn bản

        Returns:
            List of (position, type, priority) tuples
        """
        split_points = [(0, 'start', 0)]  # Start point

        # Tìm chapters (ưu tiên cao nhất)
        for pattern in self.chapter_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                split_points.append((match.start(), 'chapter', 1))

        # Tìm sections (ưu tiên trung bình)
        for pattern in self.section_patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                split_points.append((match.start(), 'section', 2))

        # Tìm paragraph breaks (ưu tiên thấp)
        # Double line breaks indicate paragraph boundaries
        for match in re.finditer(r'\n\n+', text):
            split_points.append((match.end(), 'paragraph', 3))

        # Tìm single line breaks (ưu tiên thấp nhất)
        for match in re.finditer(r'\n', text):
            if match.start() not in [sp[0] for sp in split_points]:
                split_points.append((match.end(), 'line', 4))

        # Sort by position
        split_points.sort(key=lambda x: (x[0], x[2]))

        return split_points

    def _create_chunks(
        self,
        text: str,
        split_points: List[Tuple[int, str, int]]
    ) -> List[TextChunk]:
        """Tạo chunks từ split points"""
        chunks = []
        current_start = 0
        current_type = 'paragraph'
        chunk_id = 0

        i = 0
        while i < len(split_points):
            pos, point_type, priority = split_points[i]

            # Tìm điểm kết thúc tốt nhất cho chunk hiện tại
            end_pos = self._find_best_end_point(
                text, pos, split_points[i:], current_start
            )

            if end_pos > current_start:
                chunk_text = text[current_start:end_pos].strip()

                if len(chunk_text) > 0:
                    chunks.append(TextChunk(
                        id=chunk_id,
                        text=chunk_text,
                        start_pos=current_start,
                        end_pos=end_pos,
                        chunk_type=point_type if priority <= 2 else 'paragraph',
                        metadata={
                            'length': len(chunk_text),
                            'priority': priority
                        }
                    ))
                    chunk_id += 1

                current_start = end_pos

            i += 1

        # Add final chunk if needed
        if current_start < len(text):
            final_text = text[current_start:].strip()
            if len(final_text) > 0:
                chunks.append(TextChunk(
                    id=chunk_id,
                    text=final_text,
                    start_pos=current_start,
                    end_pos=len(text),
                    chunk_type='paragraph',
                    metadata={'length': len(final_text)}
                ))

        return chunks

    def _find_best_end_point(
        self,
        text: str,
        start_pos: int,
        remaining_splits: List[Tuple[int, str, int]],
        absolute_start: int
    ) -> int:
        """Tìm điểm kết thúc tốt nhất cho chunk"""
        current_length = start_pos - absolute_start

        # Nếu đã đủ lớn, tìm break point gần nhất
        if current_length >= self.max_chunk_size:
            # Tìm paragraph break gần nhất
            for pos, point_type, priority in remaining_splits[1:]:
                if pos > start_pos and point_type in ['paragraph', 'line']:
                    return pos
            return min(start_pos + self.max_chunk_size, len(text))

        # Tìm split point tiếp theo với ưu tiên cao
        for i, (pos, point_type, priority) in enumerate(remaining_splits[1:], 1):
            chunk_size = pos - absolute_start

            # Nếu gặp chapter/section mới, kết thúc chunk hiện tại
            if priority <= 2 and chunk_size >= self.min_chunk_size:
                return pos

            # Nếu đạt max size, kết thúc tại paragraph break
            if chunk_size >= self.max_chunk_size:
                return pos

            # Nếu size tốt và có paragraph break, có thể kết thúc
            if (self.min_chunk_size <= chunk_size <= self.max_chunk_size and
                point_type == 'paragraph'):
                # Check xem có split point quan trọng hơn trong tầm không
                next_important = self._find_next_important_split(
                    remaining_splits[i+1:], pos, 500
                )
                if next_important is None:
                    return pos

        # Mặc định: lấy split point tiếp theo
        if len(remaining_splits) > 1:
            return remaining_splits[1][0]

        return len(text)

    def _find_next_important_split(
        self,
        splits: List[Tuple[int, str, int]],
        current_pos: int,
        look_ahead: int
    ) -> Tuple[int, str, int]:
        """Tìm split point quan trọng trong tầm look_ahead"""
        for pos, point_type, priority in splits:
            if pos > current_pos + look_ahead:
                break
            if priority <= 2:  # chapter or section
                return (pos, point_type, priority)
        return None

    def _add_context(self, chunks: List[TextChunk]) -> List[TextChunk]:
        """Thêm context từ chunk trước vào mỗi chunk"""
        for i in range(1, len(chunks)):
            prev_chunk = chunks[i - 1]
            # Lấy context_size ký tự cuối từ chunk trước
            context = prev_chunk.text[-self.context_size:] if len(prev_chunk.text) > self.context_size else prev_chunk.text
            chunks[i].context_before = context.strip()

        return chunks

    def get_chunk_stats(self, chunks: List[TextChunk]) -> Dict:
        """Thống kê về chunks"""
        if not chunks:
            return {}

        lengths = [len(chunk.text) for chunk in chunks]
        types = {}
        for chunk in chunks:
            types[chunk.chunk_type] = types.get(chunk.chunk_type, 0) + 1

        return {
            'total_chunks': len(chunks),
            'avg_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'chunk_types': types,
            'total_chars': sum(lengths)
        }
