SELECT 
    COUNT(CASE WHEN m_imdb IS NOT NULL THEN 1 END) AS movies_with_imdb_id,
    COUNT(CASE WHEN m_imdb IS NULL THEN 1 END) AS movies_without_imdb_id
FROM 
    public.movie;