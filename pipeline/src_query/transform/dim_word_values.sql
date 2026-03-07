-- populate dimensi word
-- select * from stg.order_reviews where review_comment_message is not null;
/*
	Maravilha = menakjubkan (5)
	lindo = cantik sekali (5)
	no prazo = tepat waktu (3)
	com muita brevidade = sangat cepat (5)
	reembolso = pengembalian (1)
	Demorou de mais = pengiriman terlalu lama (2)
	Tudo certo = baik-baik saja (4)
	péssima = sangat buruk (1)
	corretamente = benar (3)
	excelente = sangat baik (5)
	recomendo = direkomendasikan (5)
	erro = rusak (1)
	Gostei = saya suka (5)
	
	--- nilai kata berdasarkan rating 
	1-2 = Buruk
	3 = netral
	4-5 baik
*/
insert into final.dim_word_values(word,value,start_date) values('Maravilha','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('lindo','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('no prazo','netral',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('com muita brevidade','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('reembolsoe','negatif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('Demorou de mais','negatif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('Tudo certo','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('péssima','negatif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('corretamente','netral',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('excelente','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('recomendo','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('erro','positif',CURRENT_DATE);
insert into final.dim_word_values(word,value,start_date) values('Gostei','positif',CURRENT_DATE);