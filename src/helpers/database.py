# helpers/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def connect(self):
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DATABASE]
        print("Database connected ✅")

    async def disconnect(self):
        if self.client:
            self.client.close()
            print("Database disconnected ✅")

# Initialize the singleton
db = Database()