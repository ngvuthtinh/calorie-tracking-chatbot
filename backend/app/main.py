import sys
import os

# Add the repository root to sys.path to allow 'import backend.app...'
# main.py is in backend/app/, so ../.. goes to repo root.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import chat, calendar, profile, overview

app = FastAPI(title="Calorie Tracking Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(calendar.router, prefix="/api", tags=["calendar"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(overview.router, prefix="/api/overview", tags=["overview"])
