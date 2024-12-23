from pydantic import BaseModel
from uuid import UUID
from pydantic import ConfigDict

class CreateProductRequest(BaseModel):
    name: str
    description: str
    id_category: UUID
    price: float
    sku: str
    model_config = ConfigDict(from_attributes=True)