import os
from pathlib import Path

# Get the absolute path to the app directory
APP_DIR = Path(__file__).parent.resolve()

# Define storage directory
STORAGE_DIR = APP_DIR / "storage"

# Ensure storage directory exists
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Define storage file paths
EMPLOYEES_FILE = STORAGE_DIR / "employees.json"
TABLES_FILE = STORAGE_DIR / "tables.json"
