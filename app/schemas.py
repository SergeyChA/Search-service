from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    id: int
    text: str
    created_date: datetime
    rubrics: str
