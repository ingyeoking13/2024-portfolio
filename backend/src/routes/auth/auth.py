from src.repository.user.repo import UserRepo
from src.dao.user.user import User
from src.models.user.auth import Auth
from src.models.response.response import BasicResponse, Content
from fastapi import APIRouter, Depends, Response
from datetime import datetime, timedelta
import jwt

secret_key = 'my_secret_key' 
expire_minutes = 30

class AuthRouter:
    router = APIRouter(prefix='/v1/auth')

    @router.post('/signup', response_model=Content[bool])
    async def signup(auth: Auth, db: UserRepo = Depends(UserRepo)):
        try:
            if not db.check_user_exist(auth.name):
                db.add_user(auth)
            else:
                raise Exception('사용자가 존재합니다.')
        except Exception as e:
            return BasicResponse(
                Content(data=False, 
                        error_code=100,
                        error_message=e.args[0]))
        return BasicResponse(Content(data=True))
    
    @router.post('/signin', response_model=Content[bool])
    async def signin(auth: Auth, 
                     db: UserRepo = Depends(UserRepo)):
        try:
            if not db.check_user_exist(auth.name):
                raise Exception('사용자가 존재하지 않습니다.')
            if db.check_password(auth):
                response = BasicResponse(Content(data=True))
                response.set_cookie(
                    'access_token', 
                    jwt.encode({ 
                        'expire': (datetime.utcnow() + 
                                   timedelta(minutes=expire_minutes)).isoformat()
                    }, secret_key, 
                        'HS256'), 
                   httponly=True, 
                   max_age=1800)
            else:
                raise Exception('비밀번호가 일치하지 않습니다.')
        except Exception as e:
            return BasicResponse(
                Content(data=False,
                        error_code=101,
                        error_message=e.args[0]
                )
            )
        return response
    
    @router.get('/users')
    async def users(db: UserRepo = Depends(UserRepo)):
        with db.session as session:
            result = session.query(User).all()
        return result

