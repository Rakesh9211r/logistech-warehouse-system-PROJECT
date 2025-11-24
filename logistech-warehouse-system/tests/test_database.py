"""
Tests for database operations.
"""

import pytest
import os
from src.database.db_handler import DatabaseHandler

class TestDatabaseHandler:
    """Test database operations."""
    
    def setup_method(self):
        """Set up test database."""
        self.test_db = "test_warehouse.db"
        if DatabaseHandler in DatabaseHandler._instances:
            del DatabaseHandler._instances[DatabaseHandler]
        self.db = DatabaseHandler(self.test_db)
        
    def teardown_method(self):
        """Clean up test database."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
    def test_insert_package(self):
        """Test package insertion."""
        package_data = {
            'package_id': 'TEST001',
            'weight': 10.5,
            'volume': 0.5,
            'priority': 2
        }
        
        result = self.db.insert_package(package_data)
        assert result is True
        
        # Verify insertion
        package = self.db.get_package('TEST001')
        assert package['package_id'] == 'TEST001'
        assert package['weight'] == 10.5