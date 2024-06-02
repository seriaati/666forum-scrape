import os

import aiohttp


async def line_notify(message: str) -> None:
    token = os.environ.get("LINE_NOTIFY_TOKEN")
    if token is None:
        msg = "LINE_NOTIFY_TOKEN is not set"
        raise ValueError(msg)

    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {token}"}) as session:
        await session.post("https://notify-api.line.me/api/notify", data={"message": message})
