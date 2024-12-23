from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class ProductResponse(BaseModel):
    id_product: Optional[UUID]
    name: Optional[str]
    description: Optional[str]
    id_category: Optional[UUID]    
    price: Optional[float]
    sku: Optional[str]
    model_config = ConfigDict(from_attributes=True)