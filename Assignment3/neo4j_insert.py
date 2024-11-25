import logging

from config import DATA_DUMP_PATH, NEO4J_CONFIG, logger
from neo4j import GraphDatabase, RoutingControl


def importActors(driver):
  logger.info("Importing actors...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/actor.csv' AS row
    MERGE (a:Actor {name: row.a_name})
    RETURN count(a) as actor_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.info(f"Imported {result[0]['actor_count']} actors")


def importCountry(driver):
  logger.info("Importing countries...")
  query = """
    LOAD CSV WITH HEADERS FROM 'file:///dump/country.csv' AS row
    MERGE (c:Country {name: row.c_name, code: row.c_code})
    RETURN count(c) as country_count
    """
  result, summary, _ = driver.execute_query(query)
  logger.info(f"Imported {result[0]['country_count']} countries")


if __name__ == "__main__":
  logger.setLevel(logging.DEBUG)

  try:
    with GraphDatabase.driver(NEO4J_CONFIG["URI"], auth=NEO4J_CONFIG["auth"]) as driver:
      logger.debug("Verifying Neo4j connectivity...")
      driver.verify_connectivity()

      importActors(driver)
      logger.info("Data import completed successfully")

  except Exception as e:
    logger.error(f"Error during import: {str(e)}")
    exit(1)
