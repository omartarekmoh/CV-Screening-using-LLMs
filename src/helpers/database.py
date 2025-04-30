from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from pymongo.errors import DuplicateKeyError
import inspect
import logging
from pydantic import BaseModel as PydanticBaseModel

# Logger setup
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.models = []

    async def connect(self):
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DATABASE]
        
        # Create indexes for all registered models
        await self.create_indexes()
        logger.info("Database connected ✅")

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Database disconnected ✅")

    async def create_indexes(self):
        for model in self.models:
            # Get the collection name and indexes from the model
            collection_name, indexes = model.get_indexes()
            collection = self.db.get_collection(collection_name)
            
            for index in indexes:
                try:
                    # Create index if it doesn't exist
                    await collection.create_index(index["key"], name=index["name"], unique=index.get("unique", False))
                    logger.info(f"Index '{index['name']}' created for collection '{collection_name}' ✅")
                except DuplicateKeyError:
                    logger.warning(f"Index '{index['name']}' already exists for collection '{collection_name}' ⚠️")

    def register_model(self, model):
        """Register a model to be processed during index creation."""
        self.models.append(model)

    def register_all_models(self, models_module):
        """Dynamically register all models in a module that are subclasses of BaseModel."""
        for name, obj in inspect.getmembers(models_module):
            if inspect.isclass(obj) and issubclass(obj, PydanticBaseModel) and obj is not PydanticBaseModel:
                self.register_model(obj)
                logger.info(f"Model '{obj.__name__}' registered successfully.")
    
    async def init_db(self):
        # Import the models dynamically from the models module
        import models.db_schemes  # This import can be adjusted based on where your models are located
        self.register_all_models(models.db_schemes)
        await db.connect()
        await db.create_indexes()

# Initialize the singleton
db = Database()

def get_db(request: Request):
    # Return the database connection stored in app.state
    return request.app.db