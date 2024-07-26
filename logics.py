import asyncio
import aiofiles
import json

import config


async def add_prices_function(china: str, usa: str) -> None:
    async with aiofiles.open('files/prices.json', 'w') as file:
        prices_container = {
            "china": china,
            "usa": usa
        }
        await file.write(json.dumps(prices_container, indent=4, ensure_ascii=False))


async def create_prices_function(id: int) -> bool:
    return id in [config.DEV_ID, config.OWNER_ID]
    