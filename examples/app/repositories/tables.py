import json
from examples.app.models import Table
from examples.app.config import TABLES_FILE


def read() -> list[Table]:
    """Load tables from JSON file. Returns empty list if file doesn't exist."""
    if not TABLES_FILE.exists():
        return []
    
    # Read and convert JSON to Table objects
    with open(TABLES_FILE, 'r') as file:
        data = json.load(file)
        return [Table(**table_data) for table_data in data]


def save(tables: list[Table]):
    """Save tables to JSON file in storage folder."""
    # Convert Table objects to dictionaries
    table_data = [table.model_dump() for table in tables]
    
    # Save to JSON file
    with open(TABLES_FILE, 'w') as file:
        json.dump(table_data, file, indent=2)