#!/usr/bin/env python3
"""
Database setup script
Run this first to initialize the database
"""
import sqlite3
import os

def setup_database():
    """Initialize the database with required tables and sample data"""
    db_path = 'warehouse.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    
    # Read and execute schema
    with open('src/database/schema.sql', 'r') as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.commit()
    conn.close()
    
    print("✅ Database setup completed successfully!")
    print("📊 Sample data loaded:")
    print("   - 11 storage bins with various capacities")
    print("   - 3 delivery trucks with different destinations")

if __name__ == "__main__":
    setup_database()