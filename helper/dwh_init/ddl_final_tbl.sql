CREATE SCHEMA final;

create table final.dim_reviews(review integer primary key,
							   keterangan char(50),
							   start_date date,
							   end_date date);

create table final.fct_review_rating(fct_review_rating_id BIGSERIAL primary key,
									 review integer REFERENCES final.dim_reviews(review),
									 number_of_orders integer,
									 order_date date);

create table final.dim_order_status(order_status_id SMALLSERIAL primary key,
									keterangan char(150),
									start_date date,
									end_date date);

create table final.fct_order_status(fct_order_status_id BIGSERIAL PRIMARY key,
									order_status_id integer REFERENCES final.dim_order_status(order_status_id),
									order_status_quantity integer,
									ordered_date date);

create table final.dim_products(product_id bigserial primary key,
								product_id_nk text,
								product_category_name char(150),
								product_category_name_english char(150),
								start_date date,
								end_date date);

create table final.fct_item_ordered_per_day(fct_item_ordered_per_day_id bigserial primary key,
											product_id integer REFERENCES final.dim_products(product_id),
											ordered_quantity integer,
											ordered_date date);

create table final.fct_item_ordered_per_month(fct_item_ordered_per_month_id bigserial primary key,
											  product_id integer REFERENCES final.dim_products(product_id),
											  ordered_quantity int,
											  month char(25),
											  year char(25));

create table final.dim_word_values(word_value_id serial primary key,
								   word char(150),
								   value char(150),
								   start_date date,
								   end_date date);

create table final.fct_review_value(fct_review_value_id bigserial primary key,
									review_value char(50),
									number_of_review_value integer,
									order_date date);

ALTER TABLE final.fct_item_ordered_per_month ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES final.dim_products(product_id);
