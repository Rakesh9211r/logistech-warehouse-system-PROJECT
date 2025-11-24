from abc import ABC, abstractmethod
from typing import List

class StorageUnit(ABC):
    """Abstract base class for all storage units"""
    
    @abstractmethod
    def occupy_space(self, amount: int) -> bool:
        """Occupy space in the storage unit"""
        pass
    
    @abstractmethod
    def free_space(self) -> int:
        """Get available free space"""
        pass
    
    @abstractmethod
    def get_utilization(self) -> float:
        """Get space utilization percentage"""
        pass

class StorageBin(StorageUnit):
    """Concrete class for storage bins"""
    
    def __init__(self, bin_id: int, capacity: int, location_code: str, occupied_space: int = 0):
        self.bin_id = bin_id
        self.capacity = capacity
        self.location_code = location_code
        self.occupied_space = occupied_space
    
    def occupy_space(self, amount: int) -> bool:
        if self.occupied_space + amount <= self.capacity:
            self.occupied_space += amount
            return True
        return False
    
    def free_space(self) -> int:
        return self.capacity - self.occupied_space
    
    def get_utilization(self) -> float:
        return (self.occupied_space / self.capacity) * 100 if self.capacity > 0 else 0
    
    def __lt__(self, other):
        return self.capacity < other.capacity
    
    def __eq__(self, other):
        return self.bin_id == other.bin_id
    
    def __repr__(self):
        return f"Bin({self.bin_id}, cap:{self.capacity}, free:{self.free_space()})"

class Truck(StorageUnit):
    """Concrete class for delivery trucks"""
    
    def __init__(self, truck_id: int, capacity: int, destination: str, current_load: int = 0):
        self.truck_id = truck_id
        self.capacity = capacity
        self.destination = destination
        self.current_load = current_load
        self.loaded_packages = []
    
    def occupy_space(self, amount: int) -> bool:
        if self.current_load + amount <= self.capacity:
            self.current_load += amount
            return True
        return False
    
    def free_space(self) -> int:
        return self.capacity - self.current_load
    
    def get_utilization(self) -> float:
        return (self.current_load / self.capacity) * 100 if self.capacity > 0 else 0
    
    def add_package(self, package):
        """Add package to truck"""
        if self.occupy_space(package.size):
            self.loaded_packages.append(package)
            return True
        return False
    
    def __repr__(self):
        return f"Truck({self.truck_id}, dest:{self.destination}, load:{self.current_load}/{self.capacity})"