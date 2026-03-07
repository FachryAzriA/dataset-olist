insert into final.fct_item_ordered_per_day(product_id ,
										   ordered_quantity,
										   ordered_date)
(select dp.product_id,
		count(oi.product_id),
		o.order_purchase_timestamp::date
   from final.dim_products dp,
		stg.products p,
		stg.order_items oi,
		stg.orders o
  where p.product_id = dp.product_id_nk
		and oi.product_id = dp.product_id_nk
		and o.order_id = oi.order_id
  group by dp.product_id,
		   o.order_purchase_timestamp::date);