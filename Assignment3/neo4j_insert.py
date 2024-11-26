import logging

from config import NEO4J_CONFIG, logger
from neo4j import GraphDatabase


def execute_cypher_query(driver, queryFile):
  """
  Execute Cypher queries stored in a .cypher file.

  Args:
      driver (neo4j.GraphDatabase.driver): Neo4j driver object
      queryFile (str): Path to the .cypher file containing the queries
  """
  with open(queryFile, "r") as f:
    queries = f.read().split(";")

  for query in queries:
    query = query.strip()
    if query:
      logger.debug(f"Executing query: {query}")
      result, summary, _ = driver.execute_query(query, database_="neo4j")

  logger.debug(f"Executed all queries from {queryFile}")


def importActors(driver):
  logger.info("Importing actors...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/actor.csv' AS row
    MERGE (a:Actor {id: toInteger(row.a_id), firstName: split(trim(row.a_name), ' ')[0], lastName: split(trim(row.a_name), ' ')[-1]})
    RETURN count(a) as actor_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Imported {result[0]['actor_count']} actors")


def importCountry(driver):
  logger.info("Importing countries...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/country.csv' AS row
    MERGE (c:Country {id: toInteger(row.c_id), name: row.c_name, code: row.c_code})
    RETURN count(c) as country_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Imported {result[0]['country_count']} countries")


def importLanguage(driver):
  logger.info("Importing languages...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/language.csv' AS row
    MERGE (l:Language {id: toInteger(row.l_id), name: row.l_name, code: row.l_code})
    RETURN count(l) as language_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Imported {result[0]['language_count']} languages")


def removeLanguages(driver):
  logger.info("Removing language nodes...")
  query = """
    MATCH (l:Language)
    DETACH DELETE l
    RETURN count(l) as language_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Removed {result[0]['language_count']} language nodes")


def importGenre(driver):
  logger.info("Importing genres...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/genre_type.csv' AS row
    MERGE (g:Genre {id: toInteger(row.gt_id), name: row.gt_type})
    RETURN count(g) as genre_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Imported {result[0]['genre_count']} genres")


def removeGenre(driver):
  logger.info("Removing genre nodes...")
  query = """
    MATCH (g:Genre)
    DETACH DELETE g
    RETURN count(g) as genre_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Removed {result[0]['genre_count']} genre nodes")


def importMovies(driver):
  logger.info("Importing movies...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/movie.csv' AS row
    MERGE (m:Movie {id: toInteger(row.m_id)})
    ON CREATE SET
      m.id = toInteger(row.m_id),
      m.watchmodeId = toInteger(row.m_watchmode_id),
      m.title = row.m_title, 
      m.plot = row.m_plot, 
      m.viewerRating = toFloat(row.m_viewer_rating), 
      m.releaseYear = toInteger(row.m_release_year), 
      m.crId = coalesce(toInteger(row.cr_id), 'None'), 
      m.aka = [], 
      m.genres = [], 
      m.languages = []
    RETURN count(m) as movie_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Imported {result[0]['movie_count']} movies")

  logger.info("Adding content ratings...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/content_rating.csv' AS row
    MATCH (m:Movie {crId: toInteger(row.cr_id)})
    SET m.contentRating = row.cr_rating
    REMOVE m.crId
    RETURN count(m) as movie_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Added {result[0]['movie_count']} content ratings to movies")

  importGenre(driver)  # Import genre nodes first
  logger.info("Adding movie genres...")
  query = """LOAD CSV WITH HEADERS FROM 'file:///dump/movie_genre.csv' AS row
    MATCH (m:Movie {id: toInteger(row.m_id)}), (g:Genre {id: toInteger(row.gt_id)})
    WHERE NOT g.name IN m.genres
    SET m.genres = m.genres + g.name
    RETURN count(row.m_id) as movie_genre_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Added {result[0]['movie_genre_count']} genres to movies")
  removeGenre(driver)  # Remove genre nodes

  importLanguage(driver)  # Import language nodes first
  logger.info("Adding movie languages...")
  query = """LOAD CSV WITH HEADERS FROM 'file:///dump/movie_language.csv' AS row
    MATCH (m:Movie {id: toInteger(row.m_id)}), (l:Language {id: toInteger(row.l_id)})
    WHERE NOT l.name IN m.languages
    SET m.languages = m.languages + l.name
    RETURN count(row.m_id) as movie_language_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Added {result[0]['movie_language_count']} languages to movies")
  removeLanguages(driver)  # Remove language nodes

  logger.info("Adding movie AKAs...")
  query = """LOAD CSV WITH HEADERS FROM 'file:///dump/aka.csv' AS row
    MATCH (m:Movie {id: toInteger(row.m_id)})
    WHERE NOT row.aka_title IN m.aka
    SET m.aka = m.aka + row.aka_title
    RETURN count(row.aka_title) as aka_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Added {result[0]['aka_count']} AKAs to movies")


def importMovieActorRelation(driver):
  logger.info("Mapping actors to movies...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/movie_actor.csv' AS row
    MATCH (m:Movie {id: toInteger(row.m_id)}), (a:Actor {id: toInteger(row.a_id)})
    MERGE (a)-[:ACTED_IN]->(m)
    RETURN count(row.m_id) as acted_in_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Related {result[0]['acted_in_count']} actors to movies")


def importMovieCountryRelation(driver):
  logger.info("Mapping movies to countries...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/movie_country.csv' AS row
    MATCH (m:Movie {id: toInteger(row.m_id)}), (c:Country {id: toInteger(row.c_id)})
    MERGE (m)-[:FILMED_IN]->(c)
    RETURN count(row.m_id) as filmed_in_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(f"Related {result[0]['filmed_in_count']} movies to countries")


def importKeyword(driver):
  logger.info("Importing keywords...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/keyword.csv' AS row
    MERGE (k:Keyword {id: toInteger(row.k_id), name: row.k_keyword})
    WITH k, row
    MATCH (m:Movie {id: toInteger(row.m_id)})
    MERGE (m)-[:HAS_KEYWORD]->(k)
    RETURN count(k) as keyword_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.debug(
    f"Imported {result[0]['keyword_count']} keywords and related them to movies"
  )


if __name__ == "__main__":
  logger.setLevel(logging.DEBUG)

  try:
    with GraphDatabase.driver(NEO4J_CONFIG["URI"], auth=NEO4J_CONFIG["auth"]) as driver:
      logger.debug("Verifying Neo4j connectivity...")
      driver.verify_connectivity()

      logger.info("Creating database constraints...")
      execute_cypher_query(driver, "constraints.cypher")

      importActors(driver)
      importCountry(driver)
      importMovies(driver)
      importMovieActorRelation(driver)
      importMovieCountryRelation(driver)
      importKeyword(driver)
      logger.info("Data import completed successfully")

      logger.info("Creating database indexes...")
      execute_cypher_query(driver, "indexes.cypher")
  except Exception as e:
    logger.error(f"Error during import: {str(e)}")
    exit(1)
