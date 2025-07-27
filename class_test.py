from BibleVerse import BibleVerse

verse_dict = {
    "id": "act-28-28-cn-cuv",
    "name": "Acts 28:28",
    "text": "所以你們當知道，神這救恩，如今傳給外邦人，他們也必聽受。（有古卷在此有：",
    "book": "Acts",
    "chapter": 28,
    "verse": 28,
    "language": "cn",
    "translation": "cuv",
}

verse = BibleVerse(**verse_dict)
# Only happy if this success
print(verse)
