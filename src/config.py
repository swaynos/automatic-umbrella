import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global static config
APP_URL = os.getenv("APP_URL", "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DEFAULT_WAIT_DURATION = int(os.getenv("DEFAULT_WAIT_DURATION", 10))
LONGER_WAIT_DURATION = int(os.getenv("LONGER_WAIT_DURATION", DEFAULT_WAIT_DURATION + 15))
COOKIES_FILE = os.getenv("COOKIES_FILE", "cookies.json")
DAILY_SIMPLE_BRONZE_SBC_NAMES = os.getenv("DAILY_SIMPLE_BRONZE_SBC_NAMES", "Daily Bronze Upgrade").split(',')
DAILY_SIMPLE_SILVER_SBC_NAMES = os.getenv("DAILY_SIMPLE_SILVER_SBC_NAMES", "Daily Silver Upgrade").split(',')
PACK_NAMES = os.getenv("PACK_NAMES", "BRONZE PLAYERS PREMIUM,SMALL BRONZE PLAYERS,SILVER PLAYERS PREMIUM,Small Silver Players Pack,Super Bronze Pack").split(',')
GOLD_PACK_NAMES = os.getenv("GOLD_PACK_NAMES", "x11 Gold Players Pack").split(',')

OPEN_GOLD_PACKS = os.getenv("OPEN_GOLD_PACKS", "false").lower() in ("true", "1", "t")
OPEN_CHEAP_PACKS = os.getenv("OPEN_CHEAP_PACKS", "false").lower() in ("true", "1", "t")
SOLVE_DAILY_CHALLENGES = os.getenv("SOLVE_DAILY_CHALLENGES", "true").lower() in ("true", "1", "t")
GOLD_UPGRADE = os.getenv("GOLD_UPGRADE", "false").lower() in ("true", "1", "t")
GRASSROOT_GRIND = os.getenv("GRASSROOT_GRIND", "false").lower() in ("true", "1", "t")
TOTY_CRAFTING_UPGRADE = os.getenv("TOTY_CRAFTING_UPGRADE", "false").lower() in ("true", "1", "t")
EIGHTYONE_PLUS_PLAYER_PICK = os.getenv("EIGHTYONE_PLUS_PLAYER_PICK", "false").lower() in ("true", "1", "t")