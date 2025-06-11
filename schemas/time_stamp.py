from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimeStampModel(BaseModel):
    created_at: datetime
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S")
        }
    )
