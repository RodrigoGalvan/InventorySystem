from fastapi import APIRouter, FastAPI, Depends
from uuid import UUID
from app.database import get_db
from sqlalchemy.orm import Session

from app.Products.GetProducts import get_products as get_products_endpoint
from app.Products.PostProduct import post_product as post_product_endpoint
from app.Inventories.GetInventoryAlert import get_inventory_alert as get_inventory_alert_endpoint
from app.Inventories.PostTransfertInventory import transfer_inventory as post_transfer_products_endpoint
from app.Products.GetProductDetail import get_product_detail as get_product_detail_endpoint
from app.Products.PutProduct import put_product as put_product_endpoint
from app.Products.DeleteProduct import delete_product as delete_product_endpoint
from app.Inventories.GetStoreInventory import get_store_inventory as get_store_inventory_endpoint

from app.StandardModels.StandardResponse import StandardResponse
from app.StandardModels.Pagination import Pagination, PaginatedResponse 
from app.StandardModels.SuccessCodes import SuccessStatus

from app.Products.Models.CreateProductRequest import CreateProductRequest
from app.Inventories.Models.InventoryResponse import InventoryResponse
from app.Products.Models.ProductResponse import ProductResponse
from app.Inventories.Models.LowStockResponse import LowStockResponse
from app.Inventories.Models.TransferProduct import TransferProduct,MovementResponse

app = FastAPI(title="Inventory Management API",
   description="API to get products and inventory as well as to transfer products between stores and get the inventory of the stores. It is a simple API to get information from the stores and their products",
   version="1.0.0")

prefix_router = APIRouter(prefix="/api")



@prefix_router.get("/products", 
response_model=StandardResponse[PaginatedResponse[list[ProductResponse]]],
summary="Get all products based on filters",
description="Retrieves products based onf ilters of price, stock and category. It also paginates the results",
status_code=200
)
async def get_products(
        category: UUID = None,
        price: float = None,
        stock: int = None,  
        items: int = 10,
        page: int = 1,
        db: Session = Depends(get_db)
    ):  
    result, total_products, total_pages, current_page = await get_products_endpoint(db, category, price, stock, items, page)
    return StandardResponse[PaginatedResponse[list[ProductResponse]]](
       success=True,
       response=PaginatedResponse[list[ProductResponse]](result=result, pagination=Pagination(total_products=total_products, total_pages=total_pages, current_page=current_page))
   )



@prefix_router.get("/products/{id}", response_model=StandardResponse[ProductResponse], summary="Get details of a product",
description="Get the details of a product based on its id",
status_code=200
)
async def get_product_details(id:str, db: Session = Depends(get_db)):
    result = await get_product_detail_endpoint(db, id)
    return StandardResponse[ProductResponse](success=True, response=result)
    


@prefix_router.post("/products", response_model=StandardResponse[ProductResponse], summary="Add new product",
description="Adds a new product to the database",
status_code=201)
async def post_product(product: CreateProductRequest, db: Session = Depends(get_db)):
    result = await post_product_endpoint(db, product)
    return StandardResponse[ProductResponse](success=True, response=result)



@prefix_router.put("/products/{id}", response_model=StandardResponse[ProductResponse], summary="Update a product", description="Updates a product based on its id", status_code=200)
async def put_product(id:str, product: CreateProductRequest, db: Session = Depends(get_db)):  
    result = await put_product_endpoint(db, id, product)
    return StandardResponse[ProductResponse](success=True, response=result)
    

@prefix_router.delete("/products/{id}", response_model=StandardResponse[ProductResponse], summary="Delete a product", description="Deletes a product based on its id", status_code=200)
async def delete_product(id:str, db: Session = Depends(get_db)):
    result = await delete_product_endpoint(db, id)  
    return StandardResponse[ProductResponse](success=True, response=result)

#Gestion de stock

@prefix_router.get("/stores/{id}/inventory", response_model=StandardResponse[list[InventoryResponse]], summary="Get the inventory of a store", description="Get the inventory of a store based on its id", status_code=200)
async def get_store_inventory(id: str, db: Session = Depends(get_db)):
    result = await get_store_inventory_endpoint(db, id)
    return StandardResponse[list[InventoryResponse]](success=True, response=result)

    

@prefix_router.post("/inventory/transfer", response_model=StandardResponse[TransferProduct], summary="Transfer products between stores", description="Transfer products between stores based on the type of transfer", status_code=200)
async def post_transfer_products(transfer:TransferProduct, db: Session = Depends(get_db)):
    result = await post_transfer_products_endpoint(db, transfer)
    return StandardResponse[MovementResponse](success=True, response=result)


@prefix_router.get("/inventory/alerts", response_model=StandardResponse[list[LowStockResponse]], summary="Get the inventory alerts", description="Get the inventory alerts based on the minimum stock", status_code=200)
async def get_inventory_alert(db: Session = Depends(get_db)):
    result = await get_inventory_alert_endpoint(db)
    return StandardResponse[list[LowStockResponse]](success=True, response=result)


app.include_router(prefix_router)
