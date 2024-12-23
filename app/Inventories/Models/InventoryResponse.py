from pydantic import BaseModel
from uuid import UUID
from pydantic import ConfigDict

class InventoryResponse(BaseModel):
    id_product: UUID
    name: str
    quantity: int
    id_store: UUID
    comercial_name: str
    address: str
    model_config = ConfigDict(from_attributes=True)