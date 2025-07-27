import json
from genson import SchemaBuilder

# Your sample JSON object
sample = {
    "id": "re-22-19",
    "name": "Revelation 22:19",
    "text": "這書上的預言，若有人刪去甚麼，神必從這書上所寫的生命樹和聖城刪去他的分。",
    "book": "Revelation",
    "chapter": 22,
    "verse": 19,
    "language": "cn"
  }

# Generate schema
builder = SchemaBuilder()
builder.add_object(sample)

schema = builder.to_schema()
print(schema)

with open("bible_schema.json", "w") as f:
    json.dump(schema, f, indent=2)