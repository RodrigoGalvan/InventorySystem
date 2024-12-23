from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.database_models as models
import math
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse  
from uuid import UUID

async def get_products(db: Session, category: UUID, price: float, stock: int, items: int, page: int):
    #Validatons before filtering
    if(price is not None and price < 0):
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PRICE_NEGATIVE.value)

    if(stock is not None and stock < 0):
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.STOCK_NEGATIVE.value)

    if(items is not None and items < 0 or page is not None and page < 0):
        raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.PAGINATION_INVALID.value)

    #Get products and their stock
    db_query = db.query(models.Product).outerjoin(models.Inventory, models.Product.id_product == models.Inventory.id_product)
    

    #Filter only by the filters that come from the request
    if category:
        db_query = db_query.filter(models.Product.id_category == category)
    if price:
        db_query = db_query.filter(models.Product.price == price)
    if stock:
        db_query = db_query.filter(models.Inventory.quantity == stock)

    total_products = db_query.count()
    total_pages = math.ceil(total_products / items)
    current_page = page

    if items and page:
        db_query = db_query.offset((page - 1) * items).limit(items)

    #No product found
    if(db_query.count() == 0):
        raise HTTPException(status_code=ErrorStatus.NO_CONTENT.value, detail=ErrorResponse.PRODUCT_NOT_FOUND.value)

    result = db_query.all()

    return result, total_products, total_pages, current_page