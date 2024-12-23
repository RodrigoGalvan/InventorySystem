from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import app.database_models as models
import pytest
import multipart
from app.Products.Models.CreateProductRequest import CreateProductRequest
from sqlalchemy.orm import Session
from app.Inventories.Models.TransferProduct import TransferProduct, TransferType

client = TestClient(app)

@pytest.fixture
def test_db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

#------------------------------
# GET PRODUCTS
#------------------------------
def test_get_products_ok(capsys):
    response = client.get("/api/products")
    assert response.status_code == 200

def test_get_products_no_content():
    response = client.get("/api/products?category=9f964643-bd3e-4742-880c-f71145acc905")
    assert response.status_code == 204

def test_get_products_bad_request_price():
    response = client.get("/api/products?price=-1")
    assert response.status_code == 400

def test_get_products_bad_request_stock():
    response = client.get("/api/products?stock=-1")
    assert response.status_code == 400

def test_get_products_bad_request_pagination():
    response = client.get("/api/products?items=-1&page=-1")
    assert response.status_code == 400

#------------------------------
# GET PRODUCT DETAILS
#------------------------------
def test_get_product_detail_ok():
    products = client.get("/api/products")
    product_id = products.json()["response"]["result"][0]["id_product"]

    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200

def test_get_product_detail_not_found():
    response = client.get("/api/products/9f964643-bd3e-4742-880c-f71145aac905")
    assert response.status_code == 400

#------------------------------
# POST PRODUCT
#------------------------------
def test_post_product_ok():
    product = CreateProductRequest(name="Test Product", description="A test product", price=99.99, stock=10, id_category="65cfb839-f6aa-460e-884d-6b570ae2c55d", sku="1234567890")

    response = client.post("/api/products", json=product.model_dump(mode="json"))
    assert response.status_code == 201

def test_post_product_bad_request_price():
    product = CreateProductRequest(name="Test Product", description="A test product", price=-99.99, stock=10, id_category="65cfb839-f6aa-460e-884a-6b570ae2c55d", sku="1234567890")
        
    response = client.post("/api/products", json=product.model_dump(mode="json"))
    assert response.status_code == 400

def test_post_product_bad_request_category():
    product = CreateProductRequest(name="Test Product", description="A test product", price=99.99, stock=10, id_category="65cfb839-f6aa-460e-884a-6b570ae2c55d", sku="1234567890")
        
    response = client.post("/api/products", json=product.model_dump(mode="json"))
    assert response.status_code == 400

#------------------------------
# DELETE PRODUCT
#------------------------------
def test_delete_product_ok():
    product = CreateProductRequest(name="Test Product", description="A test product", price=99.99, stock=10, id_category="65cfb839-f6aa-460e-884d-6b570ae2c55d", sku="1234567890")
    
    createdProduct = client.post("/api/products", json=product.model_dump(mode="json"))

    product_id = createdProduct.json()["response"]["id_product"]

    response = client.delete(f"/api/products/{product_id}")
    assert response.status_code == 200

def test_delete_product_not_found():
    response = client.delete("/api/products/9f964643-bd3e-4742-880c-f71145aac9a5")
    assert response.status_code == 400

#------------------------------
# PUT PRODUCT
#------------------------------
def test_put_product_ok(capsys):
    product = CreateProductRequest(name="Test Product", description="A test product", price=99.99, stock=10, id_category="65cfb839-f6aa-460e-884d-6b570ae2c55d", sku="1234567890")
    
    getProducts = client.get("/api/products")
    product_id = getProducts.json()["response"]["result"][0]["id_product"]

    response = client.put(f"/api/products/{product_id}", json=product.model_dump(mode="json"))
    assert response.status_code == 200

def test_put_product_not_found():
    product = CreateProductRequest(
        name="Test Product",
        description="Test Description",
        id_category="9f964643-bd3e-4742-880c-f71145acc905",
        price=10.99,
        sku="TEST-SKU"
    )
    response = client.put("/api/products/9f964643-bd3e-4742-880a-f71145aac9a5", json=product.model_dump(mode="json"))
    assert response.status_code == 204

def test_put_product_bad_request_price():
    getProducts = client.get("/api/products")
    product_id = getProducts.json()["response"]["result"][0]["id_product"]

    product = CreateProductRequest(name="Test Product", description="A test product", price=-99.99, stock=10, id_category="65cfb839-f6aa-460e-884d-6b570ae2c55d", sku="1234567890")
        
    response = client.put(f"/api/products/{product_id}", json=product.model_dump(mode="json"))
    assert response.status_code == 400

#------------------------------
# GET STORE INVENTORY
#------------------------------

def test_get_store_inventory_ok(test_db: Session, capsys):
    getProducts = client.get("/api/products")
    product_id = getProducts.json()["response"]["result"][0]["id_product"]

    response = client.get(f"/api/stores/{product_id}/inventory")
    assert response.status_code == 200

def test_get_store_product_id_not_exists_not_found():
    response = client.get("/api/stores/9f964643-bd3e-4742-880c-f71145aacaa5/inventory")
    assert response.status_code == 400

#------------------------------
# INVENTORY ALERTS
#------------------------------
def test_inventory_alert_ok():
    response = client.get("/api/inventory/alerts")
    assert response.status_code == 200

#------------------------------
# INVENTORY TRANSFER
#------------------------------
def test_inventory_transfer_in_ok(test_db: Session):
    inventory = test_db.query(models.Inventory).first()

    transfer = TransferProduct(
        id_product=inventory.id_product,
        id_store_source=None,
        id_store_target=inventory.id_store,
        quantity=10,
        type=TransferType.IN.value
    )

    response = client.post("/api/inventory/transfer", json=transfer.model_dump(mode="json"))

    print(response.json())
    
    assert response.status_code == 200

def test_inventory_transfer_out_ok(test_db: Session):
    inventory = test_db.query(models.Inventory).first()

    transfer = TransferProduct(
        id_product=inventory.id_product,
        id_store_source=None,
        id_store_target=inventory.id_store,
        quantity=5,
        type=TransferType.OUT.value
    )
    response = client.post("/api/inventory/transfer", json=transfer.model_dump(mode="json"))
    assert response.status_code == 200

def test_inventory_tranfer_transfer_ok(test_db: Session):
    inventory = test_db.query(models.Inventory).first()

    store = test_db.query(models.Store).filter(models.Store.id_store != inventory.id_store).first()

    transfer = TransferProduct(
        id_product=inventory.id_product,
        id_store_source=inventory.id_store,
        id_store_target=store.id_store,
        quantity=5,
        type=TransferType.TRANSFER.value
    )
    response = client.post("/api/inventory/transfer", json=transfer.model_dump(mode="json"))
    assert response.status_code == 200