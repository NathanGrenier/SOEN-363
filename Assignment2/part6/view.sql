CREATE VIEW public.movie_summary AS
SELECT
    m.m_tmdb,
    m.m_imdb,
    m.m_title,
    m.m_plot,
    cr.cr_rating AS content_rating,
    m.m_runtime,
    (SELECT COUNT(*) FROM public.keyword AS k WHERE k.m_id = m.m_id) AS number_of_keywords,
    (SELECT COUNT(*) FROM public.movie_country AS mc WHERE mc.m_id = m.m_id) AS number_of_countries
FROM
    public.movie as m
JOIN
    public.content_rating cr ON cr.cr_id = m.cr_id;