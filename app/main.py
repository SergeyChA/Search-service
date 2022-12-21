import csv

from datetime import datetime
from fastapi import FastAPI, UploadFile
from typing import List
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from . import schemas
from .db import engine, metadata, posts
from .elastic import gendata


app = FastAPI()
es = AsyncElasticsearch(hosts='http://localhost:9200')


@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


@app.on_event("shutdown")
async def es_shutdown():
    await es.close()


@app.get("/posts", response_model=List[schemas.Post])
async def get_all_posts():
    async with engine.connect() as conn:
        result = await conn.execute(posts.select())
    return result.fetchall()


@app.post('/import')
async def import_csv(file: UploadFile):
    reader = csv.DictReader(
        (line.decode('utf-8') for line in file.file),
    )
    async with engine.begin() as conn:
        for row in reader:
            row["created_date"] = datetime.strptime(row["created_date"], r"%Y-%m-%d %H:%M:%S")
            await conn.execute(posts.insert(), row)
    await engine.dispose()
    await async_bulk(es, gendata())
