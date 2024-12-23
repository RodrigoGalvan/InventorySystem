from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.database_models as models
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse  
from uuid import UUID

async def get_product_detail(db: Session, id: UUID):
    product = db.query(models.Product).filter(models.Product.id_product == id).first()

    #No product found
    if(product is None):    
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRODUCT_NOT_FOUND.value)

    return product