from pymongo import MongoClient, ASCENDING, DESCENDING
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MongoDBConnection:
    """Singleton MongoDB connection manager"""
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def get_client(self):
        """Get MongoDB client with connection pooling"""
        if self._client is None:
            try:
                if settings.MONGO_USER and settings.MONGO_PASSWORD:
                    connection_string = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
                else:
                    connection_string = f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
                
                self._client = MongoClient(
                    connection_string,
                    maxPoolSize=50,
                    minPoolSize=10,
                    serverSelectionTimeoutMS=5000
                )
                # Test connection
                self._client.admin.command('ping')
                logger.info("MongoDB connection established successfully")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return self._client

    def get_database(self):
        """Get database instance"""
        if self._db is None:
            client = self.get_client()
            self._db = client[settings.MONGO_DB_NAME]
        return self._db

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None


# Global database instance
def get_db():
    """Get MongoDB database instance"""
    return MongoDBConnection().get_database()


# Collection names
CUSTOMERS_COLLECTION = 'customers'
PREDICTIONS_COLLECTION = 'predictions'


def create_indexes():
    """Create optimized indexes for MongoDB collections"""
    db = get_db()
    
    # Customer collection indexes
    customers = db[CUSTOMERS_COLLECTION]
    customers.create_index([('customer_id', ASCENDING)], unique=True)
    customers.create_index([('Contract', ASCENDING)])
    customers.create_index([('InternetService', ASCENDING)])
    customers.create_index([('tenure', ASCENDING)])
    customers.create_index([('MonthlyCharges', DESCENDING)])
    customers.create_index([('Churn', ASCENDING)])
    
    # Compound indexes for common queries
    customers.create_index([('Contract', ASCENDING), ('Churn', ASCENDING)])
    customers.create_index([('InternetService', ASCENDING), ('Churn', ASCENDING)])
    
    # Predictions collection indexes
    predictions = db[PREDICTIONS_COLLECTION]
    predictions.create_index([('customer_id', ASCENDING)])
    predictions.create_index([('prediction_date', DESCENDING)])
    predictions.create_index([('churn_probability', DESCENDING)])
    
    logger.info("MongoDB indexes created successfully")
