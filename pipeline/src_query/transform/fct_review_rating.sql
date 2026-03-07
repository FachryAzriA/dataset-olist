insert into final.fct_review_rating(review,
									number_of_orders,
									order_date)
(select t.review_score, 
		count(t.review_score),
		o.order_purchase_timestamp::date
   from stg.order_reviews t,
   		stg.orders o
  where t.order_id = o.order_id
 group by t.review_score,
 		  o.order_purchase_timestamp::date);