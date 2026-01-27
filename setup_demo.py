# Mock MongoDB for demo purposes
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churn_api.settings')

import django
django.setup()

from analytics.db import get_db, CUSTOMERS_COLLECTION, create_indexes
import pandas as pd

def setup_mock_data():
    """Load data into MongoDB for demo"""
    try:
        # Read CSV
        df = pd.read_csv('cleaned_churn_data.csv')
        print(f"Loaded {len(df)} records from CSV")
        
        # Convert to dict records
        records = df.to_dict('records')
        
        # Add customer_id
        for i, record in enumerate(records):
            record['customer_id'] = f"CUST_{i+1:06d}"
        
        # Get MongoDB connection
        db = get_db()
        customers = db[CUSTOMERS_COLLECTION]
        
        # Clear and insert
        customers.delete_many({})
        
        # Insert in batches
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            customers.insert_many(batch)
            print(f"Inserted batch {i//batch_size + 1}")
        
        # Create indexes
        create_indexes()
        
        print(f"✅ Successfully loaded {len(records)} records into MongoDB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️ MongoDB not running. Please start MongoDB first:")
        print("   docker run -d -p 27017:27017 mongo:7.0")

if __name__ == "__main__":
    setup_mock_data()
