from functools import wraps
from fastapi.responses import JSONResponse

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