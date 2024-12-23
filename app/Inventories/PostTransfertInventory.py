from sqlalchemy.orm import Session
import app.database_models as models
from app.StandardModels.ErrorsCodes import ErrorStatus, ErrorResponse
from app.Inventories.Models.TransferProduct import TransferProduct, TransferType
from datetime import datetime
from fastapi import HTTPException

async def transfer_inventory(db: Session, transfer: TransferProduct):
    try:
        #Check if store exists
        db_store = db.query(models.Store).filter(models.Store.id_store == transfer.id_store_target).first()

        if not db_store:
            raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.STORE_NOT_FOUND.value)

        
        target_store = db.query(models.Inventory).filter(models.Inventory.id_product == transfer.id_product).filter(models.Inventory.id_store == transfer.id_store_target).first()

        #Check if target store exists with the product
        if(target_store is None):
            db.add(models.Inventory(
                id_product=transfer.id_product,
                id_store=transfer.id_store_target,
                quantity=0,
                min_stock=0
            ))
            db.flush()
            target_store = db.query(models.Inventory).filter(models.Inventory.id_product == transfer.id_product).filter(models.Inventory.id_store == transfer.id_store_target).first()

        #Transfer
        if transfer.type == TransferType.IN.value:
            target_store.quantity = target_store.quantity + transfer.quantity 
            
        elif transfer.type == TransferType.OUT.value:
            #Check if stock is sufficient
            if target_store.quantity < transfer.quantity:
                raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.STOCK_INSUFICIENT.value)

            target_store.quantity = target_store.quantity - transfer.quantity  

        elif transfer.type == TransferType.TRANSFER.value:
            db_store = db.query(models.Store).filter(models.Store.id_store == transfer.id_store_source).first()

            if not db_store:
                raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.STORE_NOT_FOUND.value)

            source_store = db.query(models.Inventory).filter(models.Inventory.id_product == transfer.id_product).filter(models.Inventory.id_store == transfer.id_store_target).first()
            
            check_stock = db.query(models.Inventory).filter(models.Inventory.id_product == transfer.id_product).filter(models.Inventory.id_store == transfer.id_store_source).first() 

            if check_stock.quantity < transfer.quantity:
                raise HTTPException(status_code=ErrorStatus.BAD_REQUEST.value, detail=ErrorResponse.STOCK_INSUFICIENT.value)

            source_store.quantity = source_store.quantity - transfer.quantity   
            target_store.quantity = target_store.quantity + transfer.quantity   

        db_movement = models.Movement(
            id_product=transfer.id_product,
            id_store_source=transfer.id_store_source,
            id_store_target=transfer.id_store_target,
            quantity=transfer.quantity,
            date=datetime.now(),
            type=transfer.type
        )

        db.add(db_movement)
    
        db.commit()

        return db_movement

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise 
        else:
            print(e)
            raise HTTPException(status_code=ErrorStatus.INTERNAL_SERVER_ERROR.value, detail=ErrorResponse.ERROR_TRANSFERRING_INVENTORY.value)