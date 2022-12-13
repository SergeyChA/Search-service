import csv
from datetime import datetime
from fastapi import FastAPI, UploadFile
from typing import List

from . import schemas
from .db import engine, metadata, posts


app = FastAPI()


@app.on_event('startup')
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


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
