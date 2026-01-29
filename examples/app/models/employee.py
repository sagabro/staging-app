import time

from pydantic import BaseModel, Field

from .employee_role import EmployeeRole


class Employee(BaseModel):
    id: int | None = Field(default_factory=lambda: int(time.time()), description="Employee ID, uses the current time as a unique identifier")
    name: str
    role: EmployeeRole | None = EmployeeRole.EMPLOYEE
