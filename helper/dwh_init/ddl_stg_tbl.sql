CREATE SCHEMA stg;

CREATE TABLE stg.product_category_name_translation (
	product_category_name text NOT NULL,
	product_category_name_english text NULL,
	CONSTRAINT pk_product_category_name_translation PRIMARY KEY (product_category_name)
);

CREATE TABLE stg.products (
	product_id text NOT NULL,
	product_category_name text NULL,
	product_name_lenght float4 NULL,
	product_description_lenght float4 NULL,
	product_photos_qty float4 NULL,
	product_weight_g float4 NULL,
	product_length_cm float4 NULL,
	product_height_cm float4 NULL,
	product_width_cm float4 NULL,
	CONSTRAINT pk_products PRIMARY KEY (product_id)
);

ALTER TABLE stg.products ADD CONSTRAINT fk_products_product_category FOREIGN KEY (product_category_name) REFERENCES stg.product_category_name_translation(product_category_name);

CREATE TABLE stg.orders (
	order_id text NOT NULL,
	customer_id text NULL,
	order_status text NULL,
	order_purchase_timestamp text NULL,
	order_approved_at text NULL,
	order_delivered_carrier_date text NULL,
	order_delivered_customer_date text NULL,
	order_estimated_delivery_date text NULL,
	CONSTRAINT pk_orders PRIMARY KEY (order_id)
);

CREATE TABLE stg.order_items (
	order_id text NOT NULL,
	order_item_id int4 NOT NULL,
	product_id text NULL,
	seller_id text NULL,
	shipping_limit_date text NULL,
	price float4 NULL,
	freight_value float4 NULL,
	CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id)
);

ALTER TABLE stg.order_items ADD CONSTRAINT fk_order_items_orders FOREIGN KEY (order_id) REFERENCES stg.orders(order_id);

CREATE TABLE stg.order_reviews (
	review_id text NOT NULL,
	order_id text NOT NULL,
	review_score int4 NULL,
	review_comment_title text NULL,
	review_comment_message text NULL,
	review_creation_date text NULL,
	CONSTRAINT pk_order_reviews PRIMARY KEY (review_id, order_id)
);

ALTER TABLE stg.order_reviews ADD CONSTRAINT fk_order_reviews_orders FOREIGN KEY (order_id) REFERENCES stg.orders(order_id);

ALTER TABLE stg.order_items 
ADD CONSTRAINT fk_product_id
FOREIGN KEY (product_id) REFERENCES stg.products(product_id);