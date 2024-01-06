import ray
import aiohttp

@ray.remote
class RequestUser:
    def __init__(self):
        pass

    async def task(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(response.status)
