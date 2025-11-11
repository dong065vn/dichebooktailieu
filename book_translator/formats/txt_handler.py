"""TXT file handler"""

import logging

logger = logging.getLogger(__name__)


class TxtHandler:
    """Handler cho file TXT"""

    def read(self, file_path: str) -> str:
        """Đọc file TXT"""
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'gb2312', 'gbk', 'big5']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                logger.info(f"Successfully read TXT file with {encoding} encoding")
                return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading TXT with {encoding}: {e}")
                continue

        raise ValueError(f"Could not read file with any supported encoding: {file_path}")

    def write(self, file_path: str, content: str):
        """Ghi file TXT"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Written TXT file: {file_path}")
