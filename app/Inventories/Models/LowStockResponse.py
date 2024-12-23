from pydantic import BaseModel
from uuid import UUID
from pydantic import ConfigDict

class LowStockResponse(BaseModel):
    id_product: UUID
    name: str
    quantity: int
    id_store: UUID
    comercial_name: str
    address: str    
    min_stock: int  
    model_config = ConfigDict(from_attributes=True)