import json
from genson import SchemaBuilder

# Your sample JSON object
sample =  {
    "id": "act-28-28-cn-cuv",
    "name": "Acts 28:28",
    "text": "所以你們當知道，神這救恩，如今傳給外邦人，他們也必聽受。（有古卷在此有：",
    "book": "Acts",
    "chapter": 28,
    "verse": 28,
    "language": "cn",
    "translation": "cuv"
  },

# Generate schema
builder = SchemaBuilder()
builder.add_object(sample)

schema = builder.to_schema()
print(schema)

with open("schema/bible_schema.json", "w") as f:
    json.dump(schema, f, indent=2)