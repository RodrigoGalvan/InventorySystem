from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.database_models as models
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse  
from app.Products.Models.CreateProductRequest import CreateProductRequest

async def post_product(db: Session, product: CreateProductRequest):
    #Validate price
    if(product.price < 0):
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRICE_NEGATIVE.value)

    #See if category exists
    category = db.query(models.Category).filter(models.Category.id_category == product.id_category).first()

    if category is None:
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.CATEGORY_NOT_FOUND.value)

    try:
        #Add product
        db_product = models.Product(
            name=product.name,
            description=product.description,
            id_category=product.id_category,
            price=product.price,
            sku=product.sku
        )
        db.add(db_product)

        db.commit()

        #Refresh object and return it 
        db.refresh(db_product)

        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=ErrorStatus.INTERNAL_SERVER_ERROR.value, detail=ErrorResponse.ERROR_CREATING_PRODUCT.value)
