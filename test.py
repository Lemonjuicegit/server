from src.package.重庆市网上中介服务信息.setup import insert_jggg,insert_cggg

import asyncio
async def  cggg_task() -> None:
    while True:
        insert_cggg()
        insert_jggg()
        await asyncio.sleep(120)

asyncio.run(cggg_task())