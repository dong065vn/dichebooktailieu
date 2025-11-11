"""EPUB file handler"""

import logging
import re

logger = logging.getLogger(__name__)


class EpubHandler:
    """Handler cho file EPUB"""

    def __init__(self):
        try:
            import ebooklib
            from ebooklib import epub
            self.has_ebooklib = True
            self.epub = epub
        except ImportError:
            self.has_ebooklib = False
            logger.warning("ebooklib not installed. EPUB support disabled.")

    def read(self, file_path: str) -> str:
        """Đọc file EPUB"""
        if not self.has_ebooklib:
            raise ImportError("ebooklib not installed. Run: pip install ebooklib")

        from bs4 import BeautifulSoup

        book = self.epub.read_epub(file_path)
        text_parts = []

        # Extract text from all documents
        for item in book.get_items():
            if item.get_type() == self.epub.ITEM_DOCUMENT:
                # Parse HTML content
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text
                text = soup.get_text()

                # Clean up
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                if text:
                    text_parts.append(text)

        content = '\n\n'.join(text_parts)
        logger.info(f"Read EPUB: {len(content)} chars")
        return content

    def write(self, file_path: str, content: str):
        """Ghi file EPUB"""
        if not self.has_ebooklib:
            raise ImportError("ebooklib not installed. Run: pip install ebooklib")

        # Create new EPUB
        book = self.epub.EpubBook()

        # Set metadata
        book.set_identifier('translated_book')
        book.set_title('Translated Book')
        book.set_language('vi')

        # Split content into chapters (by double line breaks or chapter markers)
        chapters_text = self._split_into_chapters(content)

        chapters = []
        for i, chapter_text in enumerate(chapters_text):
            # Create chapter
            chapter = self.epub.EpubHtml(
                title=f'Chapter {i+1}',
                file_name=f'chap_{i+1:03d}.xhtml',
                lang='vi'
            )

            # Convert text to HTML
            html_content = self._text_to_html(chapter_text)
            chapter.set_content(html_content)

            book.add_item(chapter)
            chapters.append(chapter)

        # Define Table of Contents
        book.toc = tuple(chapters)

        # Add default NCX and Nav files
        book.add_item(self.epub.EpubNcx())
        book.add_item(self.epub.EpubNav())

        # Define CSS style
        style = '''
        @namespace epub "http://www.idpf.org/2007/ops";
        body {
            font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
        }
        p {
            text-align: justify;
            text-indent: 1.5em;
            margin: 0.5em 0;
        }
        '''
        nav_css = self.epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)

        # Create spine
        book.spine = ['nav'] + chapters

        # Write EPUB
        from ebooklib import epub
        epub.write_epub(file_path, book, {})

        logger.info(f"Written EPUB file: {file_path}")

    def _split_into_chapters(self, content: str) -> list:
        """Chia content thành chapters"""
        # Try to split by chapter markers
        chapter_pattern = r'\n\n(?=(?:Chapter|Chương|CHAPTER|第.*?章)\s+\d+)'
        chapters = re.split(chapter_pattern, content)

        # If no chapters found, split by length
        if len(chapters) == 1:
            # Split every ~10000 characters
            chunk_size = 10000
            chapters = []
            for i in range(0, len(content), chunk_size):
                chapters.append(content[i:i+chunk_size])

        return chapters

    def _text_to_html(self, text: str) -> str:
        """Convert text to HTML"""
        # Split into paragraphs
        paragraphs = text.split('\n\n')

        html_parts = ['<?xml version="1.0" encoding="UTF-8"?>',
                      '<html xmlns="http://www.w3.org/1999/xhtml">',
                      '<head><title>Chapter</title></head>',
                      '<body>']

        for para in paragraphs:
            para = para.strip()
            if para:
                # Escape HTML
                para = para.replace('&', '&amp;')
                para = para.replace('<', '&lt;')
                para = para.replace('>', '&gt;')

                # Replace single line breaks with <br/>
                para = para.replace('\n', '<br/>')

                html_parts.append(f'<p>{para}</p>')

        html_parts.append('</body></html>')

        return '\n'.join(html_parts)
