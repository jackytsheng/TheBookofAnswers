from dataclasses import dataclass
from BaseModel import BibleMeta
@dataclass
class BibleVerse(BibleMeta):
    text: str
    name: str
    book: str