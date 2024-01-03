from src.repository.user.repo import UserRepo
from src.dao.user.user import User
from src.models.user.auth import Auth
from src.models.response.response import BasicResponse, Content
from fastapi import APIRouter, Depends

import bcrypt

class AuthRouter:
    router = APIRouter(prefix='/v1/auth')

    @router.post('/signup', response_model=Content[bool])
    async def signup(auth: Auth, db: UserRepo = Depends(UserRepo)):
        try:
            salt = bcrypt.gensalt()
            with db.session as session:
                session.add(User(name=auth.name,
                                 nickname=auth.nickname,     
                                 email=auth.email, 
                                 password=bcrypt.hashpw(
                                     auth.password.encode('utf-8'),
                                     salt
                                 ),
                                 salt=salt
                                 ))
        except Exception as e:
            return BasicResponse(Content(data=False, error_message=e))
        return BasicResponse(Content(data=True))
    
    @router.get('/users')
    async def users(db: UserRepo = Depends(UserRepo)):
        with db.session as session:
            result = session.query(User).all()
        return result

