import json
from pathlib import Path

def add_language_field(input_path, output_path, language_code):
    with open(input_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    for item in data:
        item["translation"] = language_code
        item["id"] = f"{item["id"]}-{language_code}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Add language to NIV
add_language_field("bibles/niv.json", "bibles/niv.json", "niv")

# Add language to CUV (if needed later)
add_language_field("bibles/cuv.json", "bibles/cuv.json", "cuv")
