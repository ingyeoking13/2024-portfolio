import aiohttp
import asyncio

from functools import wraps
from fastapi.responses import JSONResponse
from src.app import background_job

from src.repository.task_job.repo import TaskJobRepo
from src.models.job.task_job import TaskJob
from datetime import datetime
from uuid import uuid4

class RequestUser:
    def __init__(self, id, domain, sub_domain) -> None:
        self.id = id
        self.type = 'RequestUser'
        self.domain = domain
        self.sub_domain = sub_domain

    async def job(self, url):
        repo = TaskJobRepo()
        job = TaskJob(
            name=self.id,
            parent_name='', 
            start_time=datetime.now(),
            type=self.type,
            domain=self.domain,
            sub_domain=self.sub_domain
        )
        repo.add_job(job)
        jobs = []

        for _ in range(5000):
            id = str(uuid4())
            request_user = RequestChildUser(id,self.id)
            jobs.append(asyncio.create_task(request_user.job(url=url)))

        results = await asyncio.gather(*jobs)
        job.result = { 'result': results } 
        job.end_time = datetime.now()

        repo.set_result(job)

        return (self.id, results)

class RequestChildUser:
    def __init__(self, id, parent_id) -> None:
        self.id = id
        self.parent_id = parent_id
    
    async def job(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status

def APILimiter(algorithm):
    @wraps(algorithm)
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if await algorithm().consume():
                result = await func(*args, **kwargs)
            else:
                result = JSONResponse(
                    {
                        'error_message': 'too many requests'
                    }, status_code=429)
            return result
        return wrapper
    return decorator