from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.database_models as models
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse  
from uuid import UUID
from sqlalchemy import exists

async def delete_product(db: Session, id: UUID):

    #If product does not exist return error
    if not db.query(exists().where(models.Product.id_product == id)).scalar():
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRODUCT_NOT_FOUND.value)

    #Check if product exists in inventory   
    if db.query(exists().where(models.Inventory.id_product == id)).scalar():
        db_inventory = db.query(models.Inventory).filter(models.Inventory.id_product == id).first()
        if  db_inventory.quantity > 0:
            raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRODUCT_IN_STOCK.value)
    
    try:
        db_product = db.query(models.Product).filter(models.Product.id_product == id).first() 
        db_inventory = db.query(models.Inventory).filter(models.Inventory.id_product == id).first()


        #If there is no inventory it can be deleted
        if db.query(exists().where(models.Inventory.id_product == id)).scalar():
            db.delete(db_inventory)
        db.delete(db_product)
        db.commit()
        return db_product
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=ErrorStatus.INTERNAL_SERVER_ERROR.value, detail=ErrorResponse.ERROR_DELETING_PRODUCT.value)