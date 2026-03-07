DO $$
DECLARE
	-- cursor untuk filter kata-kata
	c_word_value cursor for 
		select upper(a.word) word,
			   a.value
 		  from final.dim_word_values a
 		 where a.end_date is null;
BEGIN
	FOR c_word in c_word_value
	LOOP
		insert into final.fct_review_value(review_value,
										   number_of_review_value,
										   order_date)
		(select c_word.value,
				count(c_word.value),
				o.order_purchase_timestamp::date
	 	   from stg.orders o,
		  		stg.order_reviews ors,
				final.dim_word_values dwv
		  where o.order_id = ors.order_id
				and upper(dwv.word) = c_word.word
				and upper(ors.review_comment_message) like '%'||c_word.word||'%'
 		  group by c_word.value,
				   o.order_purchase_timestamp::date);
	END LOOP;
END;
$$ LANGUAGE plpgsql;