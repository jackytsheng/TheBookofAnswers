import json
import uuid
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from BibleSchemaValidator import BibleSchemaValidator

# ---- Config ----
BIBLE_DIR = Path("bibles")
COLLECTION_NAME = "bible"
MODEL_NAME = "intfloat/multilingual-e5-large"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
VECTOR_DIM = 1024
CHUNK_SIZE = 500

# ---- Init ----
print("🔍 Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
validator = BibleSchemaValidator()

# ---- Create Collection if not exists ----
if not qdrant.collection_exists(COLLECTION_NAME):
    print(f"🧱 Creating collection: {COLLECTION_NAME}")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
    )
else:
    print(f"✅ Collection '{COLLECTION_NAME}' already exists.")

# ---- Track invalid points ----
invalid_verses = []

# ---- Upload Helper ----
def upload_batch(batch):
    if batch:
        qdrant.upload_points(collection_name=COLLECTION_NAME, points=batch)

# ---- Process Files One at a Time ----
for file in BIBLE_DIR.glob("*.json"):
    print(f"\n📖 Processing file: {file.name}")
    with file.open("r", encoding="utf-8") as f:
        verses = json.load(f)

    batch = []

    for verse in tqdm(verses, desc=f"Embedding {file.name}"):
        if not validator.is_valid(verse):
            invalid_verses.append({ "file": file.name, "verse": verse })
            continue

        verse_id = verse.get("id") or str(uuid.uuid4())
        text = verse["text"]
        book = verse["book"]
        chapter = verse["chapter"]
        verse_num = verse["verse"]
        language = verse.get("language", "unknown")
        name = verse.get("name", f"{book} {chapter}:{verse_num}")

        # Encode with prefix
        passage_text = f"passage: {text}"
        vector = model.encode(passage_text).tolist()

        point = PointStruct(
            id=verse_id,
            vector=vector,
            payload={
                "name": name,
                "text": text,
                "book": book,
                "chapter": chapter,
                "verse": verse_num,
                "language": language,
                "source_file": file.name
            }
        )

        batch.append(point)

        if len(batch) >= CHUNK_SIZE:
            upload_batch(batch)
            batch.clear()

    # Upload remaining
    if batch:
        upload_batch(batch)

# ---- Print Invalids ----
print("\n❌ Invalid Verses:")
for iv in invalid_verses:
    print(f"File: {iv['file']}, Verse: {iv['verse']}")
print(f"\n✅ Done. Uploaded Bible verses with {len(invalid_verses)} invalid entries skipped.")
