"""
Package data models and operations.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Package:
    """Represents a package in the warehouse system."""
    
    package_id: str
    weight: float
    volume: float
    priority: int = 1  # 1: Low, 2: Medium, 3: High
    category: str = "general"
    arrival_time: Optional[datetime] = None
    destination_bin: Optional[str] = None
    
    def __post_init__(self):
        if self.arrival_time is None:
            self.arrival_time = datetime.now()
    
    def __str__(self):
        return f"Package {self.package_id} ({self.weight}kg, {self.volume}m³)"