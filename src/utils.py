import os

import aiohttp
from loguru import logger


async def send_webhook(message: str) -> None:
    webhook_url = os.environ.get("WEBHOOK_URL")
    if webhook_url is None:
        msg = "WEBHOOK_URL is not set"
        raise ValueError(msg)

    try:
        async with aiohttp.ClientSession() as session:
            await session.post(webhook_url, json={"content": message})
    except Exception:
        logger.exception("Failed to send webhook")
