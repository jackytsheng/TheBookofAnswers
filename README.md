
## Virtual Env
python3 -m venv venv


### Model
- Embedding `intfloat/multilingual-e5-large`
- AI : `ollama run qwen:7b-chat`

### Start
1. use virtual env 
# On Linux/Mac:
`source venv/bin/activate`
# On Windows use: 
`venv\Scripts\activate`

2. Embedding:
   1. Put Bible json with schema defined in `schema/bible_schema.json` 
   2. `python embed.py`
3. Create Index:
   1. 
4. Query
   1. `python query.py`

## Bible Link
- niv
https://github.com/jadenzaleski/BibleTranslations/tree/master
- cuv
https://github.com/MaatheusGois/bible/blob/main/versions/zh/cuv.json