import json
import os
from app.models import Table


def read() -> list[Table]:
    """Load tables from JSON file. Returns empty list if file doesn't exist."""
    file_path = "app/storage/tables.json"
    
    # Check if file exists
    if not os.path.exists(file_path):
        return []
    
    # Read and convert JSON to Table objects
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Table(**table_data) for table_data in data]


def save(tables: list[Table]):
    """Save tables to JSON file in storage folder."""
    file_path = "app/storage/tables.json"
    
    # Convert Table objects to dictionaries
    table_data = [table.model_dump() for table in tables]
    
    # Save to JSON file
    with open(file_path, 'w') as file:
        json.dump(table_data, file, indent=2)