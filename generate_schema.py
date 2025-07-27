import json
from genson import SchemaBuilder

# Your sample JSON object
sample = {
    'name': 'Acts 25:6',
    'text': '非斯都在他們那裡住了不過十天八天，就下該撒利亞去；第二天坐堂，吩咐將保羅提上來。',
    'book': 'Acts',
    'chapter': 25,
    'verse': 6,
    'language': 'cn',
    'translation': 'cuv',
    'abbreviation': 'act'
}

# Generate schema
builder = SchemaBuilder()
builder.add_object(sample)

schema = builder.to_schema()
print(schema)

with open("schema/bible_schema.json", "w") as f:
    json.dump(schema, f, indent=2)
