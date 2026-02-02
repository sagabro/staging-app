import time

from pydantic import BaseModel, Field


class Table(BaseModel):
    id: int | None = Field(default_factory=lambda: int(time.time()),
                           description="Table ID, uses the current time as a unique identifier")
    number: int
