import sqlite3
import threading
from datetime import datetime
from typing import List, Optional
from ..core.storage import StorageBin, Truck
from ..core.packages import Package

class DatabaseHandler:
    """
    Database operations handler with thread safety
    """
    
    def __init__(self, db_path: str = 'warehouse.db'):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with required tables"""
        with self._lock:
            conn = self._get_connection()
            try:
                with open('src/database/schema.sql', 'r') as f:
                    schema = f.read()
                conn.executescript(schema)
                conn.commit()
            except Exception as e:
                print(f"Error initializing database: {e}")
            finally:
                conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def load_bins_from_db(self) -> List[StorageBin]:
        """Load all bins from database"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM BinConfiguration")
                bins = []
                for row in cursor.fetchall():
                    bin_obj = StorageBin(
                        bin_id=row['bin_id'],
                        capacity=row['capacity'],
                        location_code=row['location_code'],
                        occupied_space=row['occupied_space']
                    )
                    bins.append(bin_obj)
                return bins
            finally:
                conn.close()
    
    def load_trucks_from_db(self) -> List[Truck]:
        """Load all trucks from database"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Trucks")
                trucks = []
                for row in cursor.fetchall():
                    truck = Truck(
                        truck_id=row['truck_id'],
                        capacity=row['capacity'],
                        destination=row['destination'],
                        current_load=row['current_load']
                    )
                    trucks.append(truck)
                return trucks
            finally:
                conn.close()
    
    def log_shipment(self, tracking_id: str, bin_id: Optional[int] = None,
                    truck_id: Optional[int] = None, status: str = "PROCESSED",
                    package_size: int = 0, destination: str = "") -> bool:
        """Log shipment activity to database"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO ShipmentLogs 
                    (tracking_id, bin_id, truck_id, status, package_size, destination)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (tracking_id, bin_id, truck_id, status, package_size, destination))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error logging shipment: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
    
    def update_bin_occupancy(self, bin_id: int, occupied_space: int) -> bool:
        """Update bin occupancy in database"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE BinConfiguration 
                    SET occupied_space = ?
                    WHERE bin_id = ?
                """, (occupied_space, bin_id))
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error updating bin occupancy: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
    
    def get_audit_logs(self, limit: int = 100) -> List[dict]:
        """Get recent audit logs"""
        with self._lock:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM ShipmentLogs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()