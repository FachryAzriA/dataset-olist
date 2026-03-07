-- populate dimensi status order
insert into final.dim_order_status(keterangan,
								   start_date)
(select distinct o.order_status,
		(SELECT CURRENT_DATE)
   from stg.orders o);