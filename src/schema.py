from pydantic import BaseModel


class Post(BaseModel):
    posted_at: str
    content: str | None = None
