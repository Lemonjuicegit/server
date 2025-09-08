import asyncio
from src.package.重庆市网上中介服务信息 import Service
from src.package.重庆市网上中介服务信息.setup import insert_jggg,insert_cggg

async def  cggg_task() -> None:
    while True:
        insert_cggg()
        insert_jggg()
        await asyncio.sleep(120)