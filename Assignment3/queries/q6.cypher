// Find the top 5 movies (ordered by rating) in a language of your choice.

MATCH (m:Movie)
WHERE 'German' IN m.languages
 ORDER BY m.viewerRating DESC
LIMIT 5
RETURN m.title, m.viewerRating, m.languages;
