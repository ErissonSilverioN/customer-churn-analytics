"""
Data migration script to load CSV data into MongoDB
"""
import os
import sys
import django
import pandas as pd
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churn_api.settings')
django.setup()

from analytics.db import get_db, create_indexes, CUSTOMERS_COLLECTION
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_customers_to_mongodb(csv_file='cleaned_churn_data.csv'):
    """
    Migrate customer data from CSV to MongoDB
    
    Args:
        csv_file (str): Path to CSV file
    """
    try:
        # Read CSV
        logger.info(f"Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} records from CSV")
        
        # Convert to dict records
        records = df.to_dict('records')
        
        # Add customer_id if not present
        for i, record in enumerate(records):
            if 'customer_id' not in record:
                record['customer_id'] = f"CUST_{i+1:06d}"
        
        # Get MongoDB connection
        db = get_db()
        customers = db[CUSTOMERS_COLLECTION]
        
        # Clear existing data (optional - comment out to append)
        logger.info("Clearing existing customer data...")
        customers.delete_many({})
        
        # Insert in batches for performance
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            result = customers.insert_many(batch)
            total_inserted += len(result.inserted_ids)
            logger.info(f"Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} records")
        
        logger.info(f"Total records inserted: {total_inserted}")
        
        # Create indexes
        logger.info("Creating MongoDB indexes...")
        create_indexes()
        
        # Verify data
        count = customers.count_documents({})
        logger.info(f"Verification: {count} documents in MongoDB")
        
        # Sample document
        sample = customers.find_one()
        logger.info(f"Sample document: {sample}")
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'cleaned_churn_data.csv'
    migrate_customers_to_mongodb(csv_file)
