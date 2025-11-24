"""
Conveyor system simulation and optimization.
"""

from core.packages import Package
from typing import List, Dict
import heapq

class ConveyorSystem:
    """
    Simulates and optimizes conveyor belt operations.
    """
    
    def __init__(self):
        self.conveyors = {}
        self.package_queue = []
        
    def add_conveyor(self, conveyor_id: str, speed: float, destinations: List[str]):
        """Add a conveyor to the system."""
        self.conveyors[conveyor_id] = {
            'speed': speed,
            'destinations': destinations,
            'current_load': 0
        }
        
    def schedule_package(self, package: Package, destination: str) -> str:
        """Schedule a package for delivery to a destination."""
        # Use priority queue where priority is based on package priority
        # and arrival time (higher priority and earlier arrival come first)
        priority = (-package.priority, package.arrival_time.timestamp())
        heapq.heappush(self.package_queue, (priority, package, destination))
        return f"Scheduled {package.package_id} for {destination}"
        
    def process_next_package(self) -> Dict:
        """Process the next package in the queue."""
        if not self.package_queue:
            return {"status": "empty", "message": "No packages in queue"}
            
        priority, package, destination = heapq.heappop(self.package_queue)
        return {
            "status": "processed",
            "package": package.package_id,
            "destination": destination,
            "priority": package.priority
        }