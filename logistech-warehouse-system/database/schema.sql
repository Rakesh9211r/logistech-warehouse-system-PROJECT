-- Initialize the database schema
CREATE TABLE IF NOT EXISTS BinConfiguration (
    bin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    capacity INTEGER NOT NULL,
    location_code TEXT NOT NULL,
    occupied_space INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ShipmentLogs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT NOT NULL,
    bin_id INTEGER,
    truck_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    package_size INTEGER,
    destination TEXT,
    FOREIGN KEY (bin_id) REFERENCES BinConfiguration(bin_id)
);

CREATE TABLE IF NOT EXISTS Trucks (
    truck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    capacity INTEGER NOT NULL,
    current_load INTEGER DEFAULT 0,
    destination TEXT,
    status TEXT DEFAULT 'AVAILABLE'
);

-- Insert sample data
INSERT OR IGNORE INTO BinConfiguration (bin_id, capacity, location_code) VALUES
(1, 5, 'A1-001'), (2, 10, 'A1-002'), (3, 15, 'A1-003'), (4, 20, 'A1-004'),
(5, 25, 'A2-001'), (6, 30, 'A2-002'), (7, 35, 'A2-003'), (8, 50, 'A2-004'),
(9, 60, 'B1-001'), (10, 75, 'B1-002'), (11, 100, 'B1-003');

INSERT OR IGNORE INTO Trucks (truck_id, capacity, destination) VALUES
(1, 200, 'New York'),
(2, 150, 'California'),
(3, 300, 'Texas');