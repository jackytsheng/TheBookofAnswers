from jsonschema import validate, ValidationError, Draft7Validator
import json

class BibleSchemaValidator:
    def __init__(self, schema_path: str = "schema/bible_schema.json"):
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
            self.validator = Draft7Validator(self.schema)

    def is_valid(self, data: dict) -> bool:
        """Returns True if data is valid, False otherwise."""
        return self.validator.is_valid(data)

    def validate(self, data: dict):
        """Raises ValidationError if invalid."""
        validate(instance=data, schema=self.schema)

    def get_errors(self, data: dict) -> list[str]:
        """Returns a list of validation error messages."""
        return [error.message for error in self.validator.iter_errors(data)]
