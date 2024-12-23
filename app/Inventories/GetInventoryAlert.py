from sqlalchemy.orm import Session
import app.database_models as models

async def get_inventory_alert(db: Session):
    db_query = db.query(models.Inventory).join(
        models.Product,
        models.Inventory.id_product == models.Product.id_product
    ).join(
        models.Store,
        models.Inventory.id_store == models.Store.id_store
    ).filter(
        models.Inventory.quantity < models.Inventory.min_stock
    )    

    db_query = db_query.with_entities(
        models.Inventory.id_product,
        models.Product.name,
        models.Inventory.quantity,
        models.Inventory.id_store,
        models.Store.comercial_name,
        models.Store.address,
        models.Inventory.min_stock
    )  
    

    result = db_query.all()

    return result