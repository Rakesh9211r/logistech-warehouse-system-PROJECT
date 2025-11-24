"""
Main entry point for the Logistech Warehouse System.
"""

from core.storage import WarehouseStorage
from algorithms.bin_selector import BinSelector
from database.db_handler import DatabaseHandler
import config.config as config

def main():
    """Main application entry point."""
    print("🚀 Starting Logistech Warehouse System...")
    
    # Initialize components
    db_handler = DatabaseHandler()
    storage = WarehouseStorage()
    bin_selector = BinSelector()
    
    print("✅ System initialized successfully!")
    print(f"📊 Configuration: {config.WAREHOUSE_CONFIG}")

if __name__ == "__main__":
    main()