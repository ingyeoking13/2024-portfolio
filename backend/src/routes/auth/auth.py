from src.models.k8s.k8s import KubeContainer, KubePod, KubePodMetadata, KubePodStatus
from src.repository.user.repo import UserRepo
from src.utils.k8s import K8SConfigure
from src.dao.user.user import User
from src.models.user.auth import Auth
from src.models.response.response import BasicResponse, Content

from fastapi import APIRouter, Depends


class AuthRouter:
    router = APIRouter(prefix='/v1/auth')

    @router.post('/signup', response_model=Content[bool])
    async def signup(auth: Auth, db: UserRepo = Depends(UserRepo)):
        try:
            db.db.add(User(name=auth.name))
        except:
            return BasicResponse(Content(data=False))
        return BasicResponse(Content(data=True))
    
    @router.get('/users')
    async def users(db: UserRepo = Depends(UserRepo)):
        result = db.db.query(User).all()
        return result

