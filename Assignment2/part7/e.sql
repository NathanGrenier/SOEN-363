SELECT l.l_name AS language, l.l_code AS code, ml.l_id, COUNT(ml.m_id) AS movies_in_language
FROM public.movie_language AS ml
JOIN public.language as l ON ml.l_id = l.l_id
GROUP BY l.l_name, l.l_code, ml.l_id
ORDER BY 4 DESC;