import asyncio

from dotenv import load_dotenv
from loguru import logger

from src.database import load_posts, save_posts
from src.scraper import fetch_forum_page, get_posts, get_total_page
from src.utils import line_notify


async def main() -> None:
    logger.info("Start scraping")

    load_dotenv()

    total_page = await get_total_page()
    logger.info(f"Total page: {total_page}")

    last_page = (total_page - 1) * 25
    last_page_content = await fetch_forum_page(last_page)

    posts = get_posts(last_page_content)
    logger.info(f"Found {len(posts)} posts")

    current_posts = load_posts()
    logger.info(f"{len(current_posts)} posts in database")

    saved_posts = save_posts(posts, current_posts)
    logger.info(f"Saved {len(saved_posts)} posts")

    for post in saved_posts:
        if post.content is not None:
            await line_notify(f"\n新貼文\n發布於: {post.posted_at}\n\n{post.content}\n\n{post.real_url}")
        else:
            await line_notify(f"\n新貼文\n發布於: {post.posted_at}\n\n(無內容)\n\n{post.real_url}")

    logger.info("Scraping finished")


if __name__ == "__main__":
    asyncio.run(main())
