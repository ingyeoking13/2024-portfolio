from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.k8s.connect import K8SRouter
from src.routes.auth.auth import AuthRouter
from src.routes.id_gen.id_gen import IdGenRouter
from src.routes.rate_limiter.rate_limiter import RateLimiterRouter

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
rate = RateLimiterRouter()
app.include_router(k8s.router)
app.include_router(auth.router)
app.include_router(rate.router)
app.include_router(IdGenRouter().router)