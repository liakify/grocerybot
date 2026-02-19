"""Configuration management for GroceryBot."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Database configuration
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "grocerybot.db"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_STREAM = sys.stdout
