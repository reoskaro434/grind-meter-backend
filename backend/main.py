from fastapi import FastAPI
from backend.rest.access_endpoint import ACCESS_ROUTER
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ACCESS_ROUTER)

@app.get("/")
async def root():
    return {"message": "Hello World"}