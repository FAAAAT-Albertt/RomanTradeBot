import asyncio
import aiofiles
import json

import config


async def add_prices_function(file: str, china: str = None, usa: str = None) -> None:
    result = await show_prices_function(file)
    
    if not china is None:
        result['china'] = china
    elif not usa is None:
        result['usa'] = usa

    async with aiofiles.open(file, 'w') as file:
        await file.write(json.dumps(result, indent=4, ensure_ascii=False))


async def create_prices_function(id: int) -> bool:
    return id in [config.DEV_ID, config.OWNER_ID]
    

async def show_prices_function(file: str) -> dict:
    async with aiofiles.open(file, 'r') as file:
        content = await file.read()
        result = json.loads(content)
    return result