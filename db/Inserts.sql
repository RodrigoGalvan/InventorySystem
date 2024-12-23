INSERT INTO products(name, description, id_category, price, sku) VALUES ('T-Shirt', 'T-Shirt for the holidays', '65cfb839-f6aa-460e-884d-6b570ae2c55d', 19.20, null)

INSERT INTO products(name, description, id_category, price, sku) VALUES ('Jeans', 'Jeans for the holidays', '65cfb839-f6aa-460e-884d-6b570ae2c55d', 20, null)


INSERT INTO inventory (id_product, id_store, quantity, min_stock) VALUES ('9a778169-950a-4ab4-b911-fa1d0dd3c1f6', '9e297fc9-fc2b-4459-b385-29b6a752d5c1', 10, 1)
INSERT INTO inventory (id_product, id_store, quantity, min_stock) VALUES ('9f964643-bd3e-4742-880c-f71145acc905', '9e297fc9-fc2b-4459-b385-29b6a752d5c1', 10, 1)

insert into stores(name, comercial_name, address) values ('Austin', 'Austin Shop', 'Austin, Texas')

insert into stores(name, comercial_name, address) values ('San Antonio', 'San Antonio Shop', 'San Antonio, Texas')

INSERT INTO categories (name, description)
VALUES ('clothing', 'Category for clothing');
