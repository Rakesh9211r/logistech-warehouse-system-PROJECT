import unittest
import threading
from src.core.singleton import LogiMaster

class TestSingleton(unittest.TestCase):
    
    def test_singleton_instance(self):
        """Test that only one instance is created"""
        controller1 = LogiMaster()
        controller2 = LogiMaster()
        
        self.assertIs(controller1, controller2)
        self.assertEqual(id(controller1), id(controller2))
    
    def test_singleton_thread_safety(self):
        """Test singleton thread safety"""
        instances = []
        
        def create_instance():
            instances.append(LogiMaster())
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All instances should be the same
        first_instance = instances[0]
        for instance in instances[1:]:
            self.assertIs(first_instance, instance)

if __name__ == '__main__':
    unittest.main()