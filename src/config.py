import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global static config
APP_URL = os.getenv("APP_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DEFAULT_WAIT_DURATION = int(os.getenv("DEFAULT_WAIT_DURATION", 10))
LONGER_WAIT_DURATION = int(os.getenv("LONGER_WAIT_DURATION", DEFAULT_WAIT_DURATION + 15))
COOKIES_FILE = os.getenv("COOKIES_FILE")
DAILY_SIMPLE_BRONZE_SBC_NAMES = os.getenv("DAILY_SIMPLE_BRONZE_SBC_NAMES", "Daily Bronze Upgrade").split(',')
DAILY_SIMPLE_SILVER_SBC_NAMES = os.getenv("DAILY_SIMPLE_SILVER_SBC_NAMES", "Daily Silver Upgrade").split(',')
PACK_NAMES = os.getenv("PACK_NAMES", "BRONZE PLAYERS PREMIUM,SMALL BRONZE PLAYERS,SILVER PLAYERS PREMIUM,Small Silver Players Pack,Super Bronze Pack").split(',')
GOLD_PACK_NAMES = os.getenv("GOLD_PACK_NAMES", "x11 Gold Players Pack").split(',')