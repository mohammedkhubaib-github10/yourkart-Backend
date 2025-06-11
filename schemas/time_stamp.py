from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TimeStampModel(BaseModel):
    created_at: datetime
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S")
        }
    )
