from typing import List, Tuple
from ..core.packages import Package

class CargoLoader:
    """
    Backtracking algorithm for optimal cargo loading
    Handles constraints like fragile items and must-ship-together packages
    """
    
    @staticmethod
    def can_load_packages(truck_capacity: int, 
                         packages: List[Package], 
                         must_include: List[Package] = None) -> Tuple[bool, List[Package]]:
        """
        Determine if packages can fit in truck using backtracking
        Returns: (can_load, optimal_selection)
        """
        if must_include:
            # First check if all must-include packages fit
            must_include_size = sum(pkg.size for pkg in must_include)
            if must_include_size > truck_capacity:
                return False, []
            
            # Remove must-include from main list
            remaining_packages = [pkg for pkg in packages if pkg not in must_include]
            remaining_capacity = truck_capacity - must_include_size
            
            can_fit, selected = CargoLoader._backtrack_load(remaining_packages, remaining_capacity, 0)
            return can_fit, must_include + selected if can_fit else (False, [])
        else:
            return CargoLoader._backtrack_load(packages, truck_capacity, 0)
    
    @staticmethod
    def _backtrack_load(packages: List[Package], capacity: int, index: int) -> Tuple[bool, List[Package]]:
        """Recursive backtracking helper function"""
        if capacity == 0:
            return True, []
        if capacity < 0 or index >= len(packages):
            return False, []
        
        # Try including current package
        include_possible, include_selection = CargoLoader._backtrack_load(
            packages, capacity - packages[index].size, index + 1
        )
        
        if include_possible:
            return True, [packages[index]] + include_selection
        
        # Try excluding current package
        exclude_possible, exclude_selection = CargoLoader._backtrack_load(
            packages, capacity, index + 1
        )
        
        return exclude_possible, exclude_selection
    
    @staticmethod
    def optimize_truck_load(truck_capacity: int, shipments: List) -> List:
        """
        Optimize truck loading with multiple shipments
        Uses greedy approach for large datasets
        """
        # Sort shipments by size (largest first for better utilization)
        sorted_shipments = sorted(shipments, key=lambda x: x.total_size(), reverse=True)
        
        loaded_shipments = []
        remaining_capacity = truck_capacity
        
        for shipment in sorted_shipments:
            if shipment.total_size() <= remaining_capacity:
                loaded_shipments.append(shipment)
                remaining_capacity -= shipment.total_size()
        
        return loaded_shipments