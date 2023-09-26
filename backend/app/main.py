from fastapi import FastAPI
# from api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.api_v1.api import api_router

app = FastAPI()


origins = [
    "http://localhost:4200",
    "https://grind-meter.com:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(ACCESS_ROUTER)
app.include_router(api_router, prefix="/api/v1")
