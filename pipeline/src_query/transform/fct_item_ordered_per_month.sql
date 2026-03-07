insert into final.fct_item_ordered_per_month(product_id,
											 ordered_quantity,
											 month,
										     year)
(select a.product_id,
		sum(a.ordered_quantity),
		CAST(EXTRACT(MONTH FROM a.ordered_date) AS text) mon,
		CAST(EXTRACT(YEAR FROM a.ordered_date) AS text) yr
   from final.fct_item_ordered_per_day a
  group by TO_CHAR(a.ordered_date,'YYYY-MM'),
		   a.product_id,
		   CAST(EXTRACT(MONTH FROM a.ordered_date) AS text),
		   CAST(EXTRACT(YEAR FROM a.ordered_date) AS text)); 