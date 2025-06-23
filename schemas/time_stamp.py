from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TimeStampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S")
        }
    )
