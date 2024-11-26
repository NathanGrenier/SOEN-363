// Find the top 2 movies with largest number of keywords.

MATCH (m:Movie)-[:HAS_KEYWORD]->(k:Keyword)
RETURN m.title, count(k) AS keyword_count
 ORDER BY keyword_count DESC
LIMIT 2;
