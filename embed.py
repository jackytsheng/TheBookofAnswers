import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm
from BibleVerse import BibleVerse
from BibleSchemaValidator import BibleSchemaValidator
from Config import Config
from id_generator import generate_qdrant_uuid_id, generate_bible_id

# Disable warning from model internally
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Loading Config
config = Config()

# ---- Init ----
print(f"🔍 Loading embedding model '{config.MODEL_NAME}'...")
model = SentenceTransformer(config.MODEL_NAME)

qdrant = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
validator = BibleSchemaValidator()
invalid_verses = []

# ---- Create Collection if not exists ----
if not qdrant.collection_exists(config.COLLECTION_NAME):
    print(f"🧱 Creating collection: {config.COLLECTION_NAME}")
    qdrant.create_collection(
        collection_name=config.COLLECTION_NAME,
        vectors_config=VectorParams(
            size=config.VECTOR_DIM, distance=Distance.COSINE),
    )
else:
    print(f"✅ Collection '{config.COLLECTION_NAME}' already exists.")

# ---- Upload Helper ----
total_upload_point = 0


def upload_batch(batch):
    global total_upload_point
    if batch:
        qdrant.upload_points(
            collection_name=config.COLLECTION_NAME, points=batch)
        total_upload_point += len(batch)


# Collect points from all JSON files in bibles/
points = []

# ---- Process Files One at a Time ----
for file in config.BIBLE_DIR.glob("*.json"):
    print(f"\n📖 Processing file: {file.name}")
    with file.open("r", encoding="utf-8") as f:
        verses = json.load(f)

    batch = []

    for verse_raw in tqdm(verses, desc=f"Embedding {file.name}"):
        if not validator.is_valid(verse_raw):
            invalid_verses.append({"file": file.name, "verse": verse_raw})
            continue
        verse = BibleVerse(**verse_raw)
        payload = verse.__dict__.copy()
        # Prefix as required by the model
        passage_text = f"passage: {verse.text}"
        embedding = model.encode(passage_text).tolist()

        point = PointStruct(
            id=generate_qdrant_uuid_id(generate_bible_id(verse)),
            vector=embedding,
            payload=payload
        )
        batch.append(point)
        if len(batch) >= config.CHUNK_SIZE:
            upload_batch(batch)
            batch.clear()

    # Upload remaining
    if batch:
        upload_batch(batch)

# ---- Print Invalids ----
if len(invalid_verses) != 0:
    print("\n❌ Invalid Verses:")
    for iv in invalid_verses:
        print(f"File: {iv['file']}, Verse: {iv['verse']}")
print(
    f"\n✅ Done. Uploaded {total_upload_point} Bible verses with {len(invalid_verses)} invalid entries skipped.")
