import unittest
from src.core.storage import StorageBin
from src.core.packages import Package
from src.algorithms.bin_selector import BinSelector
from src.algorithms.cargo_loader import CargoLoader

class TestAlgorithms(unittest.TestCase):
    
    def setUp(self):
        # Create test bins
        self.bins = [
            StorageBin(1, 5, "A1"), StorageBin(2, 10, "A2"),
            StorageBin(3, 15, "A3"), StorageBin(4, 50, "A4")
        ]
        self.bins.sort()
        
        # Create test packages
        self.packages = [
            Package("P1", 10, "D1"), Package("P2", 20, "D2"),
            Package("P3", 30, "D3"), Package("P4", 5, "D4")
        ]
    
    def test_binary_search_best_fit(self):
        """Test binary search bin selection"""
        selector = BinSelector()
        
        # Test exact match
        result = selector.find_best_fit(self.bins, 10)
        self.assertEqual(result.capacity, 10)
        
        # Test best fit
        result = selector.find_best_fit(self.bins, 12)
        self.assertEqual(result.capacity, 15)
        
        # Test no fit
        result = selector.find_best_fit(self.bins, 60)
        self.assertIsNone(result)
    
    def test_backtracking_loader(self):
        """Test backtracking cargo loader"""
        loader = CargoLoader()
        
        # Test possible load
        can_load, selection = loader.can_load_packages(50, self.packages)
        self.assertTrue(can_load)
        self.assertGreater(len(selection), 0)
        
        # Test impossible load
        can_load, selection = loader.can_load_packages(5, self.packages[:2])
        self.assertFalse(can_load)

if __name__ == '__main__':
    unittest.main()