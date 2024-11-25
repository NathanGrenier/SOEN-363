import logging

from config import NEO4J_CONFIG, logger
from neo4j import GraphDatabase, RoutingControl


def add_friend(driver, name, friend_name):
  driver.execute_query(
    "MERGE (a:Person {name: $name}) "
    "MERGE (friend:Person {name: $friend_name}) "
    "MERGE (a)-[:KNOWS]->(friend)",
    name=name,
    friend_name=friend_name,
    database_="neo4j",
  )


def print_friends(driver, name):
  records, _, _ = driver.execute_query(
    "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
    "RETURN friend.name ORDER BY friend.name",
    name=name,
    database_="neo4j",
    routing_=RoutingControl.READ,
  )
  for record in records:
    print(record["friend.name"])


if __name__ == "__main__":
  logger.setLevel(logging.DEBUG)
  with GraphDatabase.driver(NEO4J_CONFIG["URI"], auth=NEO4J_CONFIG["auth"]) as driver:
    add_friend(driver, "Arthur", "Guinevere")
    add_friend(driver, "Arthur", "Lancelot")
    add_friend(driver, "Arthur", "Merlin")
    print_friends(driver, "Arthur")
