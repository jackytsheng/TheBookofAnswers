import uuid
from BibleVerse import BibleVerse

def generate_qdrant_uuid_id(id: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, id))

def generate_bible_id(verse: BibleVerse):
    return f"{verse.abbreviation}-{verse.chapter}-{verse.verse}-{verse.language}-{verse.translation}"