// Find all movies that are played by a sample actor.

MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
WHERE toLower(a.firstName) CONTAINS toLower("Robert") AND toLower(a.lastName) CONTAINS toLower("Pattinson")
RETURN a, m;
