import bisect
from typing import List, Optional
from ..core.storage import StorageBin

class BinSelector:
    """
    Binary search-based bin selection algorithm
    Finds the optimal bin for package storage
    """
    
    @staticmethod
    def find_best_fit(bins: List[StorageBin], package_size: int) -> Optional[StorageBin]:
        """
        Find the smallest bin that can fit the package using binary search
        Time Complexity: O(log N)
        """
        if not bins or package_size <= 0:
            return None
        
        # Filter bins that have enough space and sort by capacity
        suitable_bins = [bin for bin in bins if bin.free_space() >= package_size]
        if not suitable_bins:
            return None
        
        suitable_bins.sort(key=lambda x: x.capacity)
        
        # Binary search for the best fit
        left, right = 0, len(suitable_bins) - 1
        best_fit_index = -1
        
        while left <= right:
            mid = (left + right) // 2
            current_bin = suitable_bins[mid]
            
            if current_bin.free_space() >= package_size:
                best_fit_index = mid
                right = mid - 1  # Look for smaller bin
            else:
                left = mid + 1  # Look for larger bin
        
        return suitable_bins[best_fit_index] if best_fit_index != -1 else None
    
    @staticmethod
    def find_first_fit(bins: List[StorageBin], package_size: int) -> Optional[StorageBin]:
        """Find first available bin that fits (less optimal but faster)"""
        for bin in bins:
            if bin.free_space() >= package_size:
                return bin
        return None
    
    @staticmethod
    def find_worst_fit(bins: List[StorageBin], package_size: int) -> Optional[StorageBin]:
        """Find the largest available bin"""
        suitable_bins = [bin for bin in bins if bin.free_space() >= package_size]
        return max(suitable_bins, key=lambda x: x.capacity) if suitable_bins else None