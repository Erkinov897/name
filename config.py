import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()}
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()  # masalan: @kanal_username
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "").strip()
