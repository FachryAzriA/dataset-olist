-- populate jumlah order sesuai statusnya
insert into final.fct_order_status(order_status_id,
								   order_status_quantity,
								   ordered_date)
(select a.order_status_id,
		count(b.order_id) jml_jenis_order,
		b.order_purchase_timestamp::date
   from final.dim_order_status a,
		stg.orders b
  where b.order_status = a.keterangan 
  group by a.order_status_id,
		   b.order_purchase_timestamp::date);