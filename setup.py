"""Setup script for Book Translator"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="book-translator",
    version="1.0.0",
    author="Book Translator Team",
    author_email="",
    description="Multilingual book translator using LLM APIs with intelligent chunking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/book-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tqdm>=4.65.0",
        "openai>=1.12.0",
        "anthropic>=0.18.0",
        "google-generativeai>=0.3.0",
        "cohere>=4.47",
        "groq>=0.4.0",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.10.0",
        "python-docx>=1.1.0",
        "ebooklib>=0.18",
        "beautifulsoup4>=4.12.0",
        "reportlab>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "book-translator=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
