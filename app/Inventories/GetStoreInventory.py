from sqlalchemy.orm import Session
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse
import app.database_models as models
from sqlalchemy import exists
from fastapi import HTTPException

async def get_store_inventory(db: Session, id: str):
    db_product = db.query(models.Product).filter(models.Product.id_product == id).first()
    
    #If no product
    if not db.query(exists().where(models.Product.id_product == id)).scalar():
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRODUCT_NOT_FOUND.value)

    db_query = db.query(models.Store).join(models.Inventory, models.Store.id_store == models.Inventory.id_store).join(models.Product, models.Inventory.id_product == models.Product.id_product).filter(models.Product.id_product == id)

    db_query = db_query.with_entities(models.Inventory.id_product, models.Product.name, models.Inventory.quantity, models.Inventory.id_store, models.Product.name, models.Store.comercial_name, models.Store.address)  

    result = db_query.all()


    return result
