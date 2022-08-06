from datetime import datetime

from pydantic import BaseModel


class ImportFiles(BaseModel):
    name: str
    suffix: str
    date: datetime

    class Config:
        orm_mode = True
