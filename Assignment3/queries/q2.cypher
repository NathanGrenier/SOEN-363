// Find the number of movies with and without a watch-mode info.

MATCH (m:Movie)
WHERE m.watchmodeId IS null
WITH count(m) AS movies_without_watchmodeId
MATCH (m:Movie)
WHERE m.watchmodeId IS NOT null
RETURN movies_without_watchmodeId, count(m) AS movies_with_watchmodeId;
