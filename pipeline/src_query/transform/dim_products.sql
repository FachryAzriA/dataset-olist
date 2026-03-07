insert into final.dim_products(product_id_nk,
								product_category_name,
								product_category_name_english,
								start_date)
(select p.product_id ,
		p.product_category_name,
		pcnt.product_category_name_english,
		CURRENT_DATE
   from stg.products p,
		stg.product_category_name_translation pcnt 
  where p.product_category_name = pcnt.product_category_name);