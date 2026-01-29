import json
from app.models import Employee
from app.config import EMPLOYEES_FILE


def read() -> list[Employee]:
    """Load employees from JSON file. Returns empty list if file doesn't exist."""
    if not EMPLOYEES_FILE.exists():
        return []
    
    # Read and convert JSON to Employee objects
    with open(EMPLOYEES_FILE, 'r') as file:
        data = json.load(file)
        return [Employee(**employee_data) for employee_data in data]


def save(employees: list[Employee]):
    """Save employees to JSON file in storage folder."""
    # Convert Employee objects to dictionaries
    employee_data = [employee.model_dump() for employee in employees]
    
    # Save to JSON file
    with open(EMPLOYEES_FILE, 'w') as file:
        json.dump(employee_data, file, indent=2)