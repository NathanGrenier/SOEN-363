SELECT m_tmdb, m_imdb, m_title, m_release_year, m_watchmode_id
FROM public.movie as m
JOIN (
		SELECT M_ID
		FROM public.movie_actor AS ma
		JOIN public.actor AS a ON ma.a_id = a.a_id
		WHERE a.a_name ilike 'Tom Holland'
	) as ac
ON m.m_id = ac.m_id
WHERE m_release_year BETWEEN 2000 AND 2020
ORDER BY m.m_release_year DESC;