from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.k8s.connect import K8SRouter
from src.routes.auth.auth import AuthRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

k8s = K8SRouter()
auth = AuthRouter()
app.include_router(k8s.router)
app.include_router(auth.router)