SELECT m_title, m_review_count
FROM public.movie
ORDER BY m_review_count DESC
LIMIT 3;