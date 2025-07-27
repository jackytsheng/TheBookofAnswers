import json
import uuid
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from tqdm import tqdm

# Config
BIBLE_DIR = Path("bibles")
COLLECTION_NAME = "bible" # to be replaced with something else
MODEL_NAME = "intfloat/multilingual-e5-large"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
VECTOR_DIM = 1024  # required by multilingual-e5-large

# Load embedding model
print("🔍 Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# Init Qdrant client
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Create or reset collection
print(f"🧱 Recreating collection: {COLLECTION_NAME}")
# Delete and recreate safely
if not qdrant.collection_exists(COLLECTION_NAME):
    print(f"🧱 Creating collection: {COLLECTION_NAME}")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
    )

# todo: add validation
# Collect points from all JSON files in bibles/
points = []

for file in BIBLE_DIR.glob("*.json"):
    print(f"📖 Loading {file.name}...")
    with file.open("r", encoding="utf-8") as f:
        verses = json.load(f)

    for verse in tqdm(verses, desc=f"Embedding {file.name}"):
        verse_id = verse.get("id","")
        text = verse["text"]
        book = verse["book"]
        chapter = verse["chapter"]
        verse_num = verse["verse"]
        language = verse.get("language", "unknown")
        name = verse.get("name", f"{book} {chapter}:{verse_num}")

        # Prefix as required by the model
        passage_text = f"passage: {text}"
        embedding = model.encode(passage_text).tolist()

        point = PointStruct(
            id=verse_id,
            vector=embedding,
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
        points.append(point)

# Upload in chunks
print(f"🚀 Uploading {len(points)} verses to Qdrant...")
qdrant.upload_points(collection_name=COLLECTION_NAME, points=points)
print("✅ Done.")
