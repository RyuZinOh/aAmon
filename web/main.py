import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from web.api.v1 import auth, backgrounds, users

load_dotenv()

app = FastAPI(
    title="aamon",
    description="website",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/public",
    StaticFiles(directory="public"),
    name="public",
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(backgrounds.router, prefix="/api/v1", tags=["backgrounds"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
