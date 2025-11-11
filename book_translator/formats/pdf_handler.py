"""PDF file handler"""

import logging

logger = logging.getLogger(__name__)


class PdfHandler:
    """Handler cho file PDF"""

    def __init__(self):
        try:
            import PyPDF2
            self.has_pypdf2 = True
        except ImportError:
            self.has_pypdf2 = False
            logger.warning("PyPDF2 not installed. PDF support limited.")

        try:
            import pdfplumber
            self.has_pdfplumber = True
        except ImportError:
            self.has_pdfplumber = False
            logger.warning("pdfplumber not installed. PDF support limited.")

    def read(self, file_path: str) -> str:
        """Đọc file PDF"""
        # Try pdfplumber first (better quality)
        if self.has_pdfplumber:
            try:
                return self._read_with_pdfplumber(file_path)
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}, trying PyPDF2...")

        # Fallback to PyPDF2
        if self.has_pypdf2:
            try:
                return self._read_with_pypdf2(file_path)
            except Exception as e:
                logger.error(f"PyPDF2 failed: {e}")
                raise

        raise ImportError(
            "No PDF library available. Install: pip install PyPDF2 pdfplumber"
        )

    def _read_with_pdfplumber(self, file_path: str) -> str:
        """Đọc PDF với pdfplumber"""
        import pdfplumber

        text_parts = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        content = '\n\n'.join(text_parts)
        logger.info(f"Read PDF with pdfplumber: {len(content)} chars")
        return content

    def _read_with_pypdf2(self, file_path: str) -> str:
        """Đọc PDF với PyPDF2"""
        import PyPDF2

        text_parts = []

        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        content = '\n\n'.join(text_parts)
        logger.info(f"Read PDF with PyPDF2: {len(content)} chars")
        return content

    def write(self, file_path: str, content: str):
        """
        Ghi file PDF (tạo PDF từ text)

        Note: Cần reportlab để tạo PDF
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import simpleSplit
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
        except ImportError:
            # Fallback: write as TXT
            logger.warning("reportlab not installed. Saving as TXT instead.")
            txt_path = file_path.rsplit('.', 1)[0] + '.txt'
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved as TXT: {txt_path}")
            return

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Try to register Unicode font
        try:
            # You might need to provide path to a Vietnamese-compatible font
            # pdfmetrics.registerFont(TTFont('Vietnamese', 'path/to/font.ttf'))
            # For now, use default
            pass
        except:
            pass

        # Write content
        y = height - 50
        lines = content.split('\n')

        for line in lines:
            if y < 50:  # New page
                c.showPage()
                y = height - 50

            # Handle long lines
            wrapped_lines = simpleSplit(line, 'Helvetica', 12, width - 100)

            for wrapped_line in wrapped_lines:
                if y < 50:
                    c.showPage()
                    y = height - 50

                try:
                    c.drawString(50, y, wrapped_line)
                except:
                    # Handle Unicode errors
                    c.drawString(50, y, wrapped_line.encode('latin-1', 'ignore').decode('latin-1'))

                y -= 15

        c.save()
        logger.info(f"Written PDF file: {file_path}")
