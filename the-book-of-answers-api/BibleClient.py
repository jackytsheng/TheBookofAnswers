import json
from Config import Config
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm
from BaseModel import BibleMeta
from BibleVerse import BibleVerse
from BibleSchemaValidator import BibleSchemaValidator
from id_generator import generate_qdrant_uuid_id


class BibleClient:
    config: Config
    client: QdrantClient
    transformer: SentenceTransformer
    validator: BibleSchemaValidator

    def __init__(self, config):
        self.config = config
        # Step 3: Initialize Qdrant client
        print(f"♻️  creating Qdrant client at url '{config.QDRANT_HOST}'...")
        self.client = QdrantClient(
            host=config.QDRANT_HOST, port=config.QDRANT_PORT)

        print(f"🔍 Loading embedding model '{config.MODEL_NAME}'...")
        self.transformer = SentenceTransformer(config.MODEL_NAME)
        self.validator = BibleSchemaValidator()
        self.total_upload_point = 0

    def get(self, request: list[BibleMeta]):
        try:
            ids = [generate_qdrant_uuid_id(data.id()) for data in request]
            response = self.client.retrieve(
                collection_name=self.config.COLLECTION_NAME, ids=ids)
            return response
        except UnexpectedResponse as e:
            print(e)
            return None

    def embed(self, override_mode = False):
        # ---- Create Collection if not exists ----
        if not self.client.collection_exists(self.config.COLLECTION_NAME):
            print(f"🧱 Creating collection: {self.config.COLLECTION_NAME}")
            self.client.create_collection(
                collection_name=self.config.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.config.VECTOR_DIM, distance=Distance.COSINE),
            )
        else:
            print(
                f"✅ Collection '{self.config.COLLECTION_NAME}' already exists.")

        # ---- Process Files One at a Time ----
        for file in self.config.BIBLE_DIR.glob("*.json"):
            print(f"\n📖 Processing file: {file.name}")
            with file.open("r", encoding="utf-8") as f:
                verses = json.load(f)

            batch = []
            invalid_verses = []
            total_processed_count = 0
            for verse_raw in tqdm(verses, desc=f"Embedding {file.name}"):
                if not self.validator.is_valid(verse_raw):
                    invalid_verses.append(
                        {"file": file.name, "verse": verse_raw})
                    continue
                verse = BibleVerse(**verse_raw)
                if not override_mode:
                    if len(self.get([verse])) > 0:
                        # If record found then skip
                        continue
                    
                    
                payload = verse.__dict__.copy()
                # Prefix as required by the model
                passage_text = f"passage: {verse.text}"
                embedding = self.transformer.encode(passage_text).tolist()

                point_id = verse.id()
                point = PointStruct(
                    id=generate_qdrant_uuid_id(point_id),
                    vector=embedding,
                    payload=payload
                )
                batch.append(point)
                if len(batch) >= self.config.CHUNK_SIZE:
                    self.upload_batch(batch)
                    batch.clear()
                    total_processed_count += len(batch)

            # Upload remaining
            if batch:
                self.upload_batch(batch)
                total_processed_count += len(batch)

            # ---- Print Invalids ----
            if len(invalid_verses) != 0:
                print("\n❌ Invalid Verses:")
                for iv in invalid_verses:
                    print(f"File: {iv['file']}, Verse: {iv['verse']}")
            print(
                f"\n✅ Done. Uploaded {total_processed_count} Bible verses with {len(invalid_verses)} invalid entries skipped.")

    def upload_batch(self, batch: list[PointStruct]):
        if batch:
            self.client.upload_points(
                collection_name=self.config.COLLECTION_NAME, points=batch)

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
