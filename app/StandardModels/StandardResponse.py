from pydantic import BaseModel
from typing import Generic, TypeVar
from app.StandardModels.SuccessCodes import SuccessStatus

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    response: T
