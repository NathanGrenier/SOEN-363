import logging

import psycopg

from config import (
  POSTGRES_CONFIG,
  logger,
)

if __name__ == "__main__":
  logger.setLevel(logging.DEBUG)

  with psycopg.connect(**POSTGRES_CONFIG) as conn:
    pass
