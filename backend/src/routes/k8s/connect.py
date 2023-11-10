from typing import List
from fastapi import APIRouter, HTTPException

from src.models.k8s.k8s import KubeContainer, KubePod, KubePodMetadata, KubePodStatus
from kubernetes import client, config
from src.utils.k8s import K8SConfigure

K8SRouter = APIRouter(prefix='/v1/k8s')

@K8SRouter.post('/connect')
async def connect_k8s():
    config = K8SConfigure().load_config()
    result = config.list_kube_config_contexts()[1]
    return {
        'message': result
    }

@K8SRouter.get('/pods')
async def get_pods():
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod('default')
    result: List[KubePod] = [
        KubePod(
            **{'status': KubePodStatus(**_kubepod.status.__dict__),
               'metadata': KubePodMetadata(**_kubepod.metadata.__dict__)
               }) for _kubepod in pods.items
        ]
    return {
        'meesage': result
    }

@K8SRouter.get('/dashboard')
async def read_dashboard():
    _client = K8SConfigure().load_config()
    if _client is None:
        return HTTPException(
            status_code=404, 
            detail='kubernetes 컨텍스트를 찾을 수 없습니다.' +\
            ' docker, k8s가 켜져있는지 확인부탁합니다.'
        )
    return {
        'message': config.list_kube_config_contexts()
    }
