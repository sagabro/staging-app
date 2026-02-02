from app.models import Employee, EmployeeRole, Table


def init_data(repo):
    print("Starting Restaurant Management System...")

    # Get existing employees
    employees = repo.employees.read()
    print(f"Found {len(employees)} existing employees.")

    # Create employees if none exist
    if not employees:
        print("No employees found. Creating 20 initial employees...")
        employees = create_initial_employees()
        repo.employees.save(employees)
        print("✅ Created and saved 20 employees!")

    # Get existing tables
    tables = repo.tables.read()
    print(f"Found {len(tables)} existing tables.")

    # Create tables if none exist
    if not tables:
        print("No tables found. Creating 20 initial tables...")
        tables = create_initial_tables()
        repo.tables.save(tables)
        print("✅ Created and saved 20 tables!")

    # Show summary
    print(f"\n📊 Summary:")
    print(f"   - Total employees: {len(employees)}")
    print(f"   - Total tables: {len(tables)}")
    print("\n🎉 Restaurant Management System is ready!")


def create_initial_employees() -> list[Employee]:
    """Create 20 sample employees with different roles."""
    employees = []

    # Create employees with different names and roles
    employee_names = [
        "Alice Smith", "Bob Johnson", "Carol Davis", "David Wilson", "Emma Brown",
        "Frank Miller", "Grace Lee", "Henry Garcia", "Ivy Martinez", "Jack Anderson",
        "Kate Thompson", "Luke Taylor", "Mia Moore", "Noah Jackson", "Olivia White",
        "Paul Harris", "Quinn Martin", "Ruby Clark", "Sam Lewis", "Tara Walker"
    ]

    for i, name in enumerate(employee_names):
        # Make every 5th person a manager, every 10th person an admin
        if i % 10 == 0:
            role = EmployeeRole.ADMIN
        elif i % 5 == 0:
            role = EmployeeRole.MANAGER
        else:
            role = EmployeeRole.EMPLOYEE

        # Create employee (ID will be auto-generated)
        employee = Employee(name=name, role=role)
        employees.append(employee)

    return employees


def create_initial_tables() -> list[Table]:
    """Create 20 sample tables numbered 1-20."""
    tables = []

    # Create tables numbered 1 through 20
    for table_number in range(1, 21):
        table = Table(number=table_number)
        tables.append(table)

    return tables
