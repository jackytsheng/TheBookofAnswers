from BibleSchemaValidator import BibleSchemaValidator

validator = BibleSchemaValidator()

valid_data = {
    "id": "re-22-19",
    "name": "Revelation 22:19",
    "text": "這書上的預言...",
    "book": "Revelation",
    "chapter": 22,
    "verse": 19,
    "language": "cn"
}

invalid_data = {
    "id": "re-22-19",
    "name": "Revelation 22:19",
    "chapter": 22,
    "verse": 19,
    "language": "cn"
}

# Simple boolean check
print("Is valid?", validator.is_valid(valid_data))  # True
print("Is valid?", validator.is_valid(invalid_data))  # False

# Raise an error if invalid
try:
    validator.validate(valid_data)
    print("Valid JSON ✅")
except Exception as e:
    print("Invalid JSON ❌:", str(e))

# Get all errors
errors = validator.get_errors(invalid_data)
print("Validation Errors:", errors)
