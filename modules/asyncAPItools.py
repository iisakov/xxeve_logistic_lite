import asyncio
import aiohttp


async def get_killmails_by_killmail_keys(killmail_keys: list):
    async def get_killmail(killmail_id, killmail_hash):
        async with aiohttp.ClientSession() as session:
            url = f'https://esi.evetech.net/latest/killmails/{killmail_id}/{killmail_hash}/?datasource=tranquility'
            async with session.get(url=url) as resp:
                result = await resp.json()
                return result

    tasks = []
    for killmail_key in killmail_keys:
        tasks.append(asyncio.create_task(get_killmail(killmail_key[0], killmail_key[1])))

    return await asyncio.gather(*tasks)


async def get_killmail_by_many_region_id(region_id_list: [list, set]):
    async def get_killmail(region_id):
        async with aiohttp.ClientSession() as session:
            url = f'https://zkillboard.com/api/regionID/{region_id}/pastSeconds/3600/'
            resp = await session.get(url=url)
            while resp.status != 200:
                resp = await session.get(url=url)
            return await resp.json()

    tasks = []
    for region_id in region_id_list:
        tasks.append(asyncio.create_task(get_killmail(region_id)))

    return await asyncio.gather(*tasks)
