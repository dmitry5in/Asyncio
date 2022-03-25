import aiohttp
import time
import asyncio
import requests
import asyncpg


URL = 'https://swapi.dev/api/people'
count = requests.get(URL).json()['count']
PG_DSN = 'postgresql://demodb:123456@localhost:5432/demodb'


async def get_person(number):
    session = aiohttp.ClientSession()

    response = await session.get(f'{URL}/{number}')
    response_json = await response.json()
    response_json['id'] = number
    for i in ['url', 'created', 'edited']:
        if i in response_json:
            del response_json[i]

    await session.close()
    return response_json


async def get_requests_data():
    list_of_coros = []
    for number in range(1, count + 1):
        coro = get_person(number)
        list_of_coros.append(coro)
    result = await asyncio.gather(*list_of_coros)
    return result


async def get_insert(item):

    conn = await asyncpg.connect('postgresql://demodb:123456@localhost:5432/demodb')
    coro = await conn.execute('''INSERT INTO people (sw_id, birth_year, eye_color, gender, hair_color, height, name, 
    mass, skin_color, homeworld, starships, vehicles, species, films) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)''',
    item.get('id'),
    item.get("birth_year"),
    item.get("eye_color"),
    item.get("gender"),
    item.get("hair_color"),
    item.get("height"),
    item.get("name"),
    item.get("mass"),
    item.get("skin_color"),
    item.get("homeworld"),
    item.get("starships"),
    item.get("vehicles"),
    item.get("species"),
    item.get("films"))

    await conn.close()


async def upload_to_base(data):
    coro_list_of_pstgre = []
    for item in data:
        coro = get_insert(item)
        coro_list_of_pstgre.append(coro)
    await asyncio.gather(*coro_list_of_pstgre)


if __name__ == '__main__':
    start = time.time()
    data = asyncio.get_event_loop().run_until_complete(get_requests_data())
    asyncio.get_event_loop().run_until_complete(upload_to_base(data))
    print('Время выполнения:', time.time() - start)