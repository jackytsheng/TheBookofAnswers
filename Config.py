from pathlib import Path

class Config:
    COLLECTION_NAME: str
    MODEL_NAME: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    VECTOR_DIM: int
    CHUNK_SIZE: int
    VERSE_SEARCH_LIMIT: int
    FIELDS_TO_INDEX: list[str]

    def __init__(self, user_prompt = True):
        
        # Default
        self.COLLECTION_NAME = "bible"
        self.BIBLE_DIR = Path("bibles")

        use_dev = False
        if user_prompt:
            use_dev = input("Use Development Collection? (y/n): ").strip().lower() == "y"

        if use_dev:
            self.COLLECTION_NAME = "bible-test"
            self.BIBLE_DIR = Path("test_bibles")

        self.MODEL_NAME = "intfloat/multilingual-e5-large"
        self.QDRANT_HOST = "localhost"
        self.QDRANT_PORT = 6333
        self.VECTOR_DIM = 1024  # required by multilingual-e5-large
        self.CHUNK_SIZE = 500
        self.VERSE_SEARCH_LIMIT = 10
        self.FIELDS_TO_INDEX = ["translation", "book", "language"]
