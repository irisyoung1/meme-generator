"""Pdf parsing module."""
import os
import re
import tempfile
from typing import List
from pdfminer.high_level import extract_text

from .IngestorInterface import IngestorInterface
from .model import QuoteModel


class PdfIngestor(IngestorInterface):
    """Parse PDF files using pdfminer.six (pure Python)."""

    ext = ".pdf"
    quote_regex = re.compile('"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from a PDF file using pdfminer.six."""
        text = extract_text(path)
        quotes = []
        for line in text.splitlines():
            for m in cls.quote_regex.finditer(line):
                # Strip whitespace from body and author
                body = m[1].strip()
                author = m[2].strip()
                quotes.append(QuoteModel(body, author))
        return quotes
