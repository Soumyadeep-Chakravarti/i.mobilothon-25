# backend/app/src/db/client.py
import logging
from typing import List, Type

from beanie import init_beanie
from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

# This list will hold all Beanie Document models to be initialized
DOCUMENT_MODELS: List[Type] = []


class MongoDBClient:
    """
    Manages the asynchronous connection to MongoDB and initializes Beanie ODM.
    """

    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database = None

    async def connect(self):
        """
        Establishes the connection and initializes Beanie.
        """
        try:
            logger.info("Connecting to MongoDB...")
            self.client = AsyncIOMotorClient(
                settings.MONGO_URI, serverSelectionTimeoutMS=5000
            )

            # The database name is typically extracted from the URI or set here
            db_name = self.client.get_default_database().name
            self.database = self.client[db_name]

            # Initialize Beanie ODM for document management
            await init_beanie(database=self.database, document_models=DOCUMENT_MODELS)
            logger.info(f"MongoDB connected successfully to DB: {db_name}")

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            # In production, this might raise an exception to prevent the app from starting
            # if the DB is critical for readiness.

    async def close(self):
        """
        Closes the MongoDB connection gracefully.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")


mongo_client = MongoDBClient()
