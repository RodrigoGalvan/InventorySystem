from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.database_models as models
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse  
from uuid import UUID
from app.Products.Models.CreateProductRequest import CreateProductRequest

async def put_product(db: Session, id: UUID, product: CreateProductRequest):

    try:
        #Validate price
        if(product.price < 0):
            raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRICE_NEGATIVE.value)

        #Check if product exists
        db_product = db.query(models.Product).filter(models.Product.id_product == id).first()

        if not db_product:
            raise HTTPException(status_code=ErrorStatus.NO_CONTENT.value, detail=ErrorResponse.PRODUCT_NOT_FOUND.value)
        

        #Update product
        db_product.name = product.name
        db_product.description = product.description
        db_product.id_category = product.id_category
        db_product.price = product.price
        db_product.sku = product.sku
    
        db.commit()

        #Refresh product and return it
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=ErrorStatus.INTERNAL_SERVER_ERROR.value, detail=ErrorResponse.ERROR_UPDATING_PRODUCT.value)