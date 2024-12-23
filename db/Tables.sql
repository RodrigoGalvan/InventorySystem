--drop table inventory;
--drop table products;
--drop table categories;
--drop table stores;
--drop table movements;

CREATE TABLE categories(
	id_category UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name TEXT,
	description TEXT
);

CREATE TABLE products(
	id_product UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name TEXT,
	description TEXT,
	id_category UUID,
	price NUMERIC(10,2),
	sku TEXT,
	FOREIGN KEY (id_category) REFERENCES categories(id_category)
);

CREATE TABLE stores(
	id_store UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	name TEXT,
	comercial_name TEXT,
	address TEXT
);

CREATE TABLE inventory(
	id_inventory UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	id_product UUID,
	id_store UUID,
	quantity INT,
	min_stock INT,
	FOREIGN KEY (id_product) REFERENCES products(id_product),
	FOREIGN KEY (id_store) REFERENCES stores(id_store)
);


CREATE TABLE movements(
	id_movement UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	id_product UUID,
	id_store_source UUID,
	id_store_target UUID,
	quantity INT,
	date TIMESTAMP,
	type TEXT
);
