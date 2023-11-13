import asyncio
import aiohttp
import json
import time

start_time = time.time()
base_url = "http://******"
headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': base_url,
    'Pragma': 'no-cache',
    'Referer': f'{base_url}/admin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': '*****************',
    'Content-Type': 'application/x-www-form-urlencoded'
}


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))


async def usersDb(session):
    result = []
    for page in range(1, 116):
        url = f"{base_url}/admin/page?userid=&cn=&departmet=&department=&department_NAME=&usertype=&addfrom=&lockstatus=&page={page}&rows=1000&_=1707029695218"
        data = await fetch(url, session)
        result.extend(json.loads(data)["rows"])
    await write_to_file('users.json', result)


async def addfrom(session):
    url = f"{base_url}/accountmainten/paccount/seladdfrom"
    data = await fetch(url, session)
    await write_to_file('addfrom.json', json.loads(data))


async def usersType(session):
    url = f"{base_url}/accountmainten/paccount/selusertype"
    data = await fetch(url, session)
    await write_to_file('usersType.json', json.loads(data))


async def orgTree(session):
    Trees = []
    url = f"{base_url}/management/org/getOrgTree"
    for id in range(10000, 90001, 10000):
        payload = "" if id == 80000 else {"id": id}
        async with session.post(url, data=payload) as resp:
            data = await resp.json()
            Trees.extend(data)
    await write_to_file('orgTree.json', Trees)


async def main():
    tasks = []
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks.append(asyncio.create_task(usersDb(session)))
        tasks.append(asyncio.create_task(addfrom(session)))
        tasks.append(asyncio.create_task(usersType(session)))
        tasks.append(asyncio.create_task(orgTree(session)))

        await asyncio.gather(*tasks)
    await session.close()


asyncio.run(main())
end_time = time.time()
elapsed_time = end_time - start_time
print("耗时：", elapsed_time, "秒")
