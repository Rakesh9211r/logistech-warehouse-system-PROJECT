"""
Integration tests for the complete system.
"""

import pytest
from src.core.storage import WarehouseStorage
from src.core.packages import Package
from src.algorithms.bin_selector import BinSelector
from src.database.db_handler import DatabaseHandler

class TestIntegration:
    """Integration tests."""
    
    def setup_method(self):
        """Set up integration test environment."""
        # Clear singletons
        for cls in [WarehouseStorage, BinSelector, DatabaseHandler]:
            if cls in getattr(cls, '_instances', {}):
                del cls._instances[cls]
                
        self.storage = WarehouseStorage()
        self.selector = BinSelector()
        self.db = DatabaseHandler("test_integration.db")
        
    def test_complete_workflow(self):
        """Test complete package workflow."""
        # Add bins to storage
        self.storage.add_bin("INT001", 100, "ZoneA")
        
        # Create and store package
        package = Package("INT_PKG001", 25, 0.3, priority=2)
        
        # Select bin and store package
        bin_id = self.selector.select_bin_first_fit(package)
        assert bin_id == "INT001"
        
        # Store package
        success = self.storage.store_package(package, bin_id)
        assert success is True
        
        # Verify in database
        db_package = self.db.get_package("INT_PKG001")
        assert db_package is not None