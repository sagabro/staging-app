import json
import os
from app.models import Employee


def read() -> list[Employee]:
    """Load employees from JSON file. Returns empty list if file doesn't exist."""
    file_path = "app/storage/employees.json"
    
    # Check if file exists
    if not os.path.exists(file_path):
        return []
    
    # Read and convert JSON to Employee objects
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [Employee(**employee_data) for employee_data in data]


def save(employees: list[Employee]):
    """Save employees to JSON file in storage folder."""
    file_path = "app/storage/employees.json"
    
    # Convert Employee objects to dictionaries
    employee_data = [employee.model_dump() for employee in employees]
    
    # Save to JSON file
    with open(file_path, 'w') as file:
        json.dump(employee_data, file, indent=2)