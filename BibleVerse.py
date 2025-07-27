from dataclasses import dataclass

@dataclass
class BibleVerse:
    abbreviation: str
    name: str
    text: str
    book: str
    chapter: int
    verse: int
    language: str
    translation: str
