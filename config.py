import os

class Config:
    API_ID = int(os.getenv("API_ID", "12345"))
    API_HASH = os.getenv("API_HASH", "your_api_hash")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
    OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))