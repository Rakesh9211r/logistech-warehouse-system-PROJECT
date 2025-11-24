"""
Database handler for warehouse operations.
"""

import sqlite3
from pathlib import Path
from core.singleton import SingletonMeta

class DatabaseHandler(metaclass=SingletonMeta):
    """
    Handles all database operations for the warehouse system.
    """
    
    def __init__(self, db_path: str = "warehouse.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create packages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                package_id TEXT PRIMARY KEY,
                weight REAL NOT NULL,
                volume REAL NOT NULL,
                priority INTEGER DEFAULT 1,
                category TEXT DEFAULT 'general',
                arrival_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                destination_bin TEXT,
                status TEXT DEFAULT 'incoming'
            )
        ''')
        
        # Create bins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bins (
                bin_id TEXT PRIMARY KEY,
                capacity REAL NOT NULL,
                location TEXT NOT NULL,
                current_load REAL DEFAULT 0,
                status TEXT DEFAULT 'available'
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def insert_package(self, package_data: dict) -> bool:
        """Insert a new package into the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO packages 
                (package_id, weight, volume, priority, category, destination_bin)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                package_data['package_id'],
                package_data['weight'],
                package_data['volume'],
                package_data.get('priority', 1),
                package_data.get('category', 'general'),
                package_data.get('destination_bin')
            ))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
            
    def get_package(self, package_id: str) -> dict:
        """Retrieve package information from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM packages WHERE package_id = ?', (package_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'package_id': result[0],
                'weight': result[1],
                'volume': result[2],
                'priority': result[3],
                'category': result[4],
                'arrival_time': result[5],
                'destination_bin': result[6],
                'status': result[7]
            }
        return {}