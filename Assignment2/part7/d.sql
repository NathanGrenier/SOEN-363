SELECT COUNT(*) AS movies_in_more_than_1_language
FROM (
		SELECT ml.m_id, COUNT(ml.l_id) AS language_count
		FROM public.movie_language AS ml
		GROUP BY ml.m_id
		HAVING COUNT(ml.l_id) > 1
		ORDER BY 1
	) AS m;