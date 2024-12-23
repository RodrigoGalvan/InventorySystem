
CREATE INDEX product_index
ON products(id_category);

CREATE INDEX min_stock
ON inventory(min_stock);

CREATE INDEX price
ON products(price);