from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Pagination(BaseModel):
    total_products: int
    total_pages: int
    current_page: int

class PaginatedResponse(BaseModel, Generic[T]):
    result: T
    pagination: Pagination