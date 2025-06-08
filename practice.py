from pydantic import BaseModel, Field, computed_field, ConfigDict
from typing import Optional, List
from datetime import datetime



class Developers(BaseModel):
    Name: str
    Exp: float = Field(..., gt=0)
    salary: float = Field(..., ge=600000)
    skills: Optional[list] = None,
    joined_date: datetime
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime
            ('%d-%m-%Y')
        }
    )

    @computed_field
    @property
    def deserved_salary(self) -> float:
        return self.Exp * self.salary


dev = Developers(
    Name="Khubaib",
    Exp=2,
    salary="12000000",
    skills=["java", "kotlin", "python"],
    joined_date=datetime(2024, 4, 2)
)
json_str = dev.model_dump_json()
print(json_str)
