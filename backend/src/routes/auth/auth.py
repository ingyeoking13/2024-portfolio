from src.models.k8s.k8s import KubeContainer, KubePod, KubePodMetadata, KubePodStatus
from src.repository.user.repo import UserRepo
from src.utils.k8s import K8SConfigure
from src.dao.user.user import User

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from kubernetes import client, config
from sqlalchemy.orm import Session


class AuthRouter:
    router = APIRouter(prefix='/v1/auth')

    @router.post('/signup')
    async def signup(db: UserRepo = Depends(UserRepo)):
        result = db.db.query(User).all()

