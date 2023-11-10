from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.k8s.connect import K8SRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(K8SRouter)