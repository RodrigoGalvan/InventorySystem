from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import ConfigDict

class TransferType(Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"   

class TransferProduct(BaseModel):
    id_product: UUID
    id_store_source: Optional[UUID]
    id_store_target: UUID
    quantity: int
    type: str
    model_config = ConfigDict(from_attributes=True)

class MovementResponse(BaseModel):
    id_product: UUID
    id_store_source: Optional[UUID]
    id_store_target: UUID
    quantity: int
    date: datetime
    type: str   
    model_config = ConfigDict(from_attributes=True)
    