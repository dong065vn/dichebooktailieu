"""File format handlers"""

from .handler import FileHandler
from .txt_handler import TxtHandler
from .pdf_handler import PdfHandler
from .epub_handler import EpubHandler
from .docx_handler import DocxHandler

__all__ = [
    'FileHandler',
    'TxtHandler',
    'PdfHandler',
    'EpubHandler',
    'DocxHandler'
]
