import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/db_msg"

metadata = sqlalchemy.MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("created_date",  sqlalchemy.DateTime),
    sqlalchemy.Column("rubrics", sqlalchemy.String),
)
