SELECT m.m_title, m.m_viewer_rating AS rating, gt.gt_type 
FROM public.movie AS m
JOIN public.movie_genre AS mg ON mg.m_id = m.m_id
JOIN public.genre_type AS gt ON gt.gt_id = mg.gt_id
WHERE gt.gt_TYPE ilike 'comedy'
ORDER BY m.m_viewer_rating DESC
LIMIT 2;