import uuid

def generate_qdrant_uuid_id(id: str):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, id))
