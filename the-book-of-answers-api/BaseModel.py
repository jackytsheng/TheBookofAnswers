from dataclasses import dataclass
@dataclass
class BibleMeta:
    abbreviation: str
    chapter: int
    verse: int
    language: str
    translation: str 
    
    # Don't change this as this corresponding to the vector db uuid conversion
    def id(self):
        return f"{self.abbreviation}-{self.chapter}-{self.verse}-{self.language}-{self.translation}"