from . import db


async def gendata():
    async with db.engine.connect() as conn:
        result = await conn.execute(db.posts.select())
        posts = result.fetchall()
        for post in posts:
            yield {
                "_index": "posts",
                "doc": {
                    "id": post["id"],
                    "text": post["text"]
                },
            }
