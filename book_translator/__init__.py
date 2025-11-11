"""
Multilingual Book Translator
Dịch sách thông minh với khả năng giữ nguyên mạch văn bản
"""

__version__ = "1.0.0"
__author__ = "Book Translator Team"

from .core.translator import BookTranslator
from .core.chunker import IntelligentChunker
from .core.merger import SmartMerger

__all__ = ['BookTranslator', 'IntelligentChunker', 'SmartMerger']
