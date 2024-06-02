import json
import pathlib

from .schema import Post

FILE_PATH = pathlib.Path("posts.json")


def load_posts() -> list[Post]:
    if not FILE_PATH.exists():
        return []
    with open(FILE_PATH, encoding="utf-8") as f:
        return [Post(**post) for post in json.load(f)]


def get_post(posted_at: str) -> Post | None:
    posts = load_posts()
    for post in posts:
        if post.posted_at == posted_at:
            return post
    return None


def save_posts(posts: list[Post]) -> list[Post]:
    posts_to_dump = [post for post in posts if get_post(post.posted_at) is None]
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([post.model_dump() for post in posts_to_dump], f, ensure_ascii=False, indent=2)

    return posts_to_dump
