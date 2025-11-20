from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

DataType = TypeVar('DataType')

class PaginatedResponse(BaseModel, Generic[DataType]):
    items: List[DataType]
    total: int
    page: int
    per_page: int

    class Config:
        arbitrary_types_allowed = True