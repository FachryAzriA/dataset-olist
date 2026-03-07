-- populate dimensi rating
insert into final.dim_reviews(review,
							  keterangan,
							  start_date)
(select distinct t.review_score,
	    (case
	     	when t.review_score = 1 then 'Sangat Buruk'
	     	when t.review_score = 2 then 'Buruk'
	     	when t.review_score = 3 then 'Cukup'
	     	when t.review_score = 4 then 'Baik'
	     	when t.review_score = 5 then 'Sangat Baik'
	     end) keterangan,
	     (SELECT CURRENT_DATE)
   from stg.order_reviews t);