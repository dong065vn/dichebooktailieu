"""Basic tests for Book Translator"""

import pytest
from book_translator.core.chunker import IntelligentChunker, TextChunk
from book_translator.core.merger import SmartMerger


def test_chunker_basic():
    """Test basic chunking functionality"""
    chunker = IntelligentChunker(max_chunk_size=100, min_chunk_size=20)

    text = """Chapter 1: Introduction

This is the first paragraph of the book.
It contains some important information.

This is the second paragraph.
It has different content.

Chapter 2: Details

More content here."""

    chunks = chunker.chunk_text(text, "english")

    assert len(chunks) > 0
    assert all(isinstance(c, TextChunk) for c in chunks)
    assert all(len(c.text) > 0 for c in chunks)


def test_merger_basic():
    """Test basic merging functionality"""
    merger = SmartMerger()

    chunks = [
        TextChunk(0, "First chunk", 0, 11, "paragraph", {}),
        TextChunk(1, "Second chunk", 11, 23, "paragraph", {}),
        TextChunk(2, "Third chunk", 23, 34, "paragraph", {}),
    ]

    translations = [
        "Đoạn đầu tiên",
        "Đoạn thứ hai",
        "Đoạn thứ ba"
    ]

    result = merger.merge_chunks(chunks, translations)

    assert len(result) > 0
    assert "Đoạn đầu tiên" in result
    assert "Đoạn thứ hai" in result
    assert "Đoạn thứ ba" in result


def test_chunker_stats():
    """Test chunk statistics"""
    chunker = IntelligentChunker()

    text = "This is a test. " * 100

    chunks = chunker.chunk_text(text, "english")
    stats = chunker.get_chunk_stats(chunks)

    assert 'total_chunks' in stats
    assert 'avg_length' in stats
    assert stats['total_chunks'] > 0
    assert stats['avg_length'] > 0


def test_merger_validation():
    """Test merge validation"""
    merger = SmartMerger()

    chunks = [
        TextChunk(0, "Test chunk", 0, 10, "paragraph", {}),
    ]

    translations = ["Đoạn kiểm tra"]

    result = merger.merge_chunks(chunks, translations)
    validation = merger.validate_merge(chunks, result)

    assert 'is_valid' in validation
    assert 'original_length' in validation
    assert 'merged_length' in validation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
