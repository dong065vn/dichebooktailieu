"""DOCX file handler"""

import logging

logger = logging.getLogger(__name__)


class DocxHandler:
    """Handler cho file DOCX/DOC"""

    def __init__(self):
        try:
            from docx import Document
            self.has_docx = True
            self.Document = Document
        except ImportError:
            self.has_docx = False
            logger.warning("python-docx not installed. DOCX support disabled.")

    def read(self, file_path: str) -> str:
        """Đọc file DOCX"""
        if not self.has_docx:
            raise ImportError("python-docx not installed. Run: pip install python-docx")

        doc = self.Document(file_path)
        text_parts = []

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                text_parts.append(text)

        # Also read tables
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        row_text.append(cell_text)
                if row_text:
                    text_parts.append(' | '.join(row_text))

        content = '\n\n'.join(text_parts)
        logger.info(f"Read DOCX: {len(content)} chars")
        return content

    def write(self, file_path: str, content: str):
        """Ghi file DOCX"""
        if not self.has_docx:
            raise ImportError("python-docx not installed. Run: pip install python-docx")

        from docx.shared import Pt, Inches

        doc = self.Document()

        # Set default font
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)

        # Split content into paragraphs
        paragraphs = content.split('\n\n')

        for para_text in paragraphs:
            para_text = para_text.strip()
            if para_text:
                # Check if it's a heading (simple heuristic)
                if self._is_heading(para_text):
                    para = doc.add_heading(para_text, level=1)
                else:
                    para = doc.add_paragraph(para_text)

                    # Handle single line breaks within paragraph
                    if '\n' in para_text and '\n\n' not in para_text:
                        # This paragraph has single line breaks
                        # We already added it as one paragraph, which is fine
                        pass

        # Save document
        doc.save(file_path)
        logger.info(f"Written DOCX file: {file_path}")

    def _is_heading(self, text: str) -> bool:
        """Kiểm tra xem text có phải heading không"""
        # Simple heuristic
        if len(text) < 100 and (
            text.isupper() or
            text.startswith('Chapter ') or
            text.startswith('Chương ') or
            text.startswith('CHAPTER ') or
            text.startswith('第') and '章' in text
        ):
            return True
        return False
