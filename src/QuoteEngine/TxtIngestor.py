"""Txt parsing module."""
from typing import List

from .IngestorInterface import IngestorInterface
from .model import QuoteModel


class TxtIngestor(IngestorInterface):
    """Parse plain text files."""

    ext = ".txt"

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse a .txt file and return a list of QuoteModel objects."""
        quotes = []
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                if len(line.strip()) > 0:
                    body, author = line.strip().split(" - ")
                    quotes.append(QuoteModel(body, author))
        return quotes
