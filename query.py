from Config import Config
from BibleVerse import BibleVerse
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

import sys

# Disable warning from model internally
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Step 1: Load config
config = Config()

# Step 2: Load model
print(f"🔍 Loading embedding model '{config.MODEL_NAME}'...")
model = SentenceTransformer(config.MODEL_NAME)

# Step 3: Initialize Qdrant client
client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)

# Step 4: Get user query
query_text = input("Enter your query: ").strip()
if not query_text:
    print("⚠️ Empty query. Exiting.")
    sys.exit(1)

# Step 5: Encode query to vector
query_vector = model.encode(f"query: {query_text}").tolist()
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
    ),

# Step 6: Perform search
results = client.search(
    collection_name=config.COLLECTION_NAME,
    query_vector=query_vector,
    limit=config.VERSE_SEARCH_LIMIT,
)

# Step 7: Display top matches
print("\n🔎 Top Matches:")
for i, res in enumerate(results, 1):
    res.payload["id"] = res.id
    verse = BibleVerse(**res.payload)
    score = res.score
    print(f"{i}. {verse.name} [Score: {100*score:.4f}%]")
    print(verse.name)
    print(f"   {verse.text}\n")
