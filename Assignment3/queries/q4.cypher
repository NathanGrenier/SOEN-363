// Find all movies with two countries of your choice. Make sure your query returns more than one movie. List movies that may be associated with either of the countries (not necessarily both).

MATCH (m:Movie)-[:FILMED_IN]-(c:Country)
WHERE c.name IN ['Canada', 'Australia']
RETURN m, c;
