from fastapi import FastAPI
from pydantic import BaseModel
from Config import Config
from BibleClient import BibleClient
from BaseModel import BibleMeta
# prod init config
config = Config(False)
client = BibleClient(config)

app = FastAPI()

# Define a request body schema


class InputText(BaseModel):
    query_text: str


@app.post("/ask")
def process_text(input_data: InputText):
    return client.query(input_data.query_text)


@app.post("/get-verses")
def process_text(input_data: list[BibleMeta]):
    return client.get(input_data)
