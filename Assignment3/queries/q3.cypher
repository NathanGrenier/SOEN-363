// Find all movies that are released after the year 2023 and has a viewer rating of at least 5.

MATCH (m:Movie)
WHERE m.releaseYear > 2023 AND m.viewerRating >= 5
RETURN m;
