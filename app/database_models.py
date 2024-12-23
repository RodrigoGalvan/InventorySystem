from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, UUID, Float
from uuid import uuid4  

class Category(Base):
    __tablename__ = "categories"

    id_category = Column(UUID,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)

class Product(Base):
    __tablename__ = "products"

    id_product = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    id_category = Column(UUID, nullable=False)
    price = Column(Float, nullable=False)
    sku = Column(String, nullable=False)

class Store(Base):
    __tablename__ = "stores"

    id_store = Column(UUID,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    comercial_name = Column(String,nullable=False)
    address = Column(String,nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"

    id_inventory = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_product = Column(UUID, nullable=False)
    id_store = Column(UUID, nullable=False)
    quantity = Column(Integer, nullable=False)
    min_stock = Column(Integer, nullable=False)

class Movement(Base):
    __tablename__ = "movements"

    id_movement = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    id_product = Column(UUID, nullable=False)
    id_store_source = Column(UUID, nullable=False)
    id_store_target = Column(UUID, nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(TIMESTAMP, nullable=False)    
    type = Column(String, nullable=False)
