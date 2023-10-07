from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kubernetes import client, config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return {
        "message" : "안녕"
    }

@app.post('/connect/k8s')
async def connect_k8s():
    config.load_kube_config()
    return {
        'message': config.list_kube_config_contexts()
    }

@app.get('/k8s/pods')
async def get_pods():
    with client.ApiClient() as api_client:
        result = client.V1PodList()
    return {
        'meesage': result
    }


@app.get('/dashboard')
async def read_dashboard():
    return {
        'message': config.list_kube_config_contexts()
    }
