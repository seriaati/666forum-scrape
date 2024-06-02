import re

import aiohttp
import bs4
from loguru import logger

from .schema import Post

FORUM_URL = "https://mikeon88.666forum.com/t2-topic"
FORUM_URL_WITH_PAGE = "https://mikeon88.666forum.com/t2p{page}-topic"
PROFILE_NAME = "mikeon88"


async def fetch_content(url: str) -> str:
    logger.info(f"Fetching {url}")
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        return await response.text()


async def fetch_forum_page(page: int) -> str:
    return await fetch_content(FORUM_URL_WITH_PAGE.format(page=page))


async def get_total_page() -> int:
    content = await fetch_content(FORUM_URL)
    soup = bs4.BeautifulSoup(content, "lxml")

    # Find div with class topic-actions
    topic_actions = soup.find("div", class_="topic-actions")

    if topic_actions is None:
        msg = "Cannot find topic-actions"
        raise ValueError(msg)

    # Get total page number: pattern is (共X頁)
    search = re.search(r"共(\d+)頁", topic_actions.text)
    if search is None:
        msg = "Cannot find total page number"
        raise ValueError(msg)
    total_page = search.group(1)

    try:
        return int(total_page)
    except ValueError as e:
        msg = "Cannot convert total page number to integer"
        raise ValueError(msg) from e


def get_posts(content: str) -> list[Post]:
    result: list[Post] = []
    soup = bs4.BeautifulSoup(content, "lxml")
    posts = soup.find_all("div", class_="post")
    for post in posts:
        post_profile_name = post.find("div", class_="postprofile-name").text.strip()
        if post_profile_name == PROFILE_NAME:
            post_content = post.find("div", class_="postbody").text
            posted_at = post.find("div", class_="topic-date").text
            result.append(Post(posted_at=posted_at, content=post_content or None))

    return result
