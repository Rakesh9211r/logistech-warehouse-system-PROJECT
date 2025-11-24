import sqlite3
import threading
from typing import List, Optional

class LogiMaster:
    """
    Singleton class for warehouse control tower
    Only one instance should exist in the system
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LogiMaster, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.db_connection = sqlite3.connect('warehouse.db', check_same_thread=False)
            self.db_connection.row_factory = sqlite3.Row
            self._initialized = True
    
    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()