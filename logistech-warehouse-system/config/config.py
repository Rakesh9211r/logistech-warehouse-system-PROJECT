"""
Configuration settings for the warehouse system.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Warehouse configuration
WAREHOUSE_CONFIG = {
    'MAX_BIN_CAPACITY': 1000.0,  # kg
    'HIGH_PRIORITY_THRESHOLD': 3,
    'DEFAULT_CONVEYOR_SPEED': 2.5,  # m/s
    'DATABASE_PATH': os.getenv('DATABASE_PATH', 'warehouse.db'),
    'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO')
}

# Algorithm parameters
ALGORITHM_CONFIG = {
    'BIN_SELECTION_STRATEGY': 'priority',  # 'first_fit', 'best_fit', 'priority'
    'ENABLE_LOAD_OPTIMIZATION': True,
    'MAX_QUEUE_SIZE': 1000
}