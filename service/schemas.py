from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ImportFiles(BaseModel):
    name: str
    suffix: str
    date: datetime

    class Config:
        orm_mode = True


class FileData(BaseModel):
    columns: list[Any]
    data: list[dict[str, Any]]


class FileSettings(BaseModel):
    sheet: str
    base_column: str
    compare_column: str
    precision: float
