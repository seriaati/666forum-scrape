from pydantic import BaseModel


class Post(BaseModel):
    posted_at: str
    content: str | None = None
    url: str

    @property
    def real_url(self) -> str:
        return f"https://mikeon88.666forum.com/{self.url}"
