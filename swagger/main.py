from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router

import os

root_path = os.getenv('ROOT_PATH', "backend")

app = FastAPI(
    root_path=root_path,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
