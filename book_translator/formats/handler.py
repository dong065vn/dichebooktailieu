"""Main file handler - Auto-detect và route tới handler phù hợp"""

import os
import logging
from typing import Optional

from .txt_handler import TxtHandler
from .pdf_handler import PdfHandler
from .epub_handler import EpubHandler
from .docx_handler import DocxHandler

logger = logging.getLogger(__name__)


class FileHandler:
    """
    Main file handler với auto-detection

    Hỗ trợ:
    - TXT
    - PDF
    - EPUB
    - DOCX
    """

    def __init__(self):
        self.handlers = {
            'txt': TxtHandler(),
            'pdf': PdfHandler(),
            'epub': EpubHandler(),
            'docx': DocxHandler(),
            'doc': DocxHandler(),
        }

    def read_file(self, file_path: str, format: Optional[str] = None) -> str:
        """
        Đọc file

        Args:
            file_path: Đường dẫn file
            format: Format (auto-detect nếu None)

        Returns:
            Nội dung văn bản
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Auto-detect format
        if format is None:
            format = self._detect_format(file_path)

        format = format.lower()

        if format not in self.handlers:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Reading {format.upper()} file: {file_path}")
        handler = self.handlers[format]

        return handler.read(file_path)

    def write_file(
        self,
        file_path: str,
        content: str,
        format: Optional[str] = None
    ):
        """
        Ghi file

        Args:
            file_path: Đường dẫn file output
            content: Nội dung
            format: Format (auto-detect nếu None)
        """
        # Auto-detect format
        if format is None:
            format = self._detect_format(file_path)

        format = format.lower()

        if format not in self.handlers:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Writing {format.upper()} file: {file_path}")
        handler = self.handlers[format]

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)

        handler.write(file_path, content)

    def _detect_format(self, file_path: str) -> str:
        """Auto-detect file format từ extension"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower().lstrip('.')

        if not ext:
            # Try to detect from file content
            return 'txt'  # Default to txt

        if ext in self.handlers:
            return ext

        # Default to txt
        logger.warning(f"Unknown extension .{ext}, treating as TXT")
        return 'txt'

    def get_supported_formats(self) -> list:
        """Lấy list các format được hỗ trợ"""
        return list(self.handlers.keys())
