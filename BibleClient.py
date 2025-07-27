from Config import Config
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from BaseModel import BibleMeta
from id_generator import generate_qdrant_uuid_id


class BibleClient:
    config: Config
    client: QdrantClient
    transformer: SentenceTransformer

    def __init__(self, config):
        self.config = config
        # Step 3: Initialize Qdrant client
        self.client = QdrantClient(
            host=config.QDRANT_HOST, port=config.QDRANT_PORT)

        print(f"🔍 Loading embedding model '{config.MODEL_NAME}'...")
        self.transformer = SentenceTransformer(config.MODEL_NAME)

    def get(self, request: list[BibleMeta]):
        try:
            ids = [generate_qdrant_uuid_id(data.id()) for data in request]
            print(ids)
            response = self.client.retrieve(
                collection_name=self.config.COLLECTION_NAME, ids=ids)
            return response
        except UnexpectedResponse as e:
            print(e)
            return None

    def query(self, query_text: str):
        query_vector = self.transformer.encode(f"query: {query_text}").tolist()
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="translation",
                    match=models.MatchValue(value="cuv"),
                ),
                models.FieldCondition(
                    key="language",
                    match=models.MatchValue(value="cn"),
                ),
            ]
        )

        results = self.client.search(
            collection_name=self.config.COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=self.config.VERSE_SEARCH_LIMIT,
        )

        return results
