from Config import Config
from qdrant_client import QdrantClient

# Connect to Qdrant
config = Config()
client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)

# Index fields: translation, book, language

for field in config.FIELDS_TO_INDEX:
    print(f"🔧 Creating index for `{field}`...")
    client.create_payload_index(
        collection_name=config.COLLECTION_NAME,
        field_name=field,
        field_schema='keyword'  # use "keyword" for string fields
    )
