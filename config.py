"""Configuration helpers for the Inter-sight Streamlit application."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
DB_NAME = os.getenv("DB_NAME", "intersight_db")
DB_USER = os.getenv("DB_USER", "intersight_user")
DB_PASS = os.getenv("DB_PASS", "intersight@pass@123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))


__all__ = [
    "GOOGLE_API_KEY",
    "DB_NAME",
    "DB_USER",
    "DB_PASS",
    "DB_HOST",
    "DB_PORT",
    "UPLOAD_DIR",
]
