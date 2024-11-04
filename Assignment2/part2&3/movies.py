import json
import os

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")
API_KEY_URL_PARAM = f"?apiKey={WATCHMODE_API_KEY}"
WATCHMODE_API_URL = "https://api.watchmode.com/v1/"

FREE_MOVIE_DB_URL = "https://imdb.iamidiotareyoutoo.com"


connection = psycopg.connect(
    dbname="db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

def appendParams(url, params):
    for key, value in params.items():
        url += f"&{key}={value}"
    return url

def getMovieList():
    url = f"{WATCHMODE_API_URL}{API_KEY_URL_PARAM}/list-titles/"
    params = {

    }
    url = appendParams(url, params)
    
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM content_rating")
    dataset = cursor.fetchall()
    for data in dataset:
        print(data)
        
    cursor.close()
    connection.close()

'''
cursor.execute(
    """
    INSERT INTO Movie (M_WATCHMODE_ID, M_IMDB, M_TMDB, M_TITLE, M_PLOT, M_RUNTIME, M_VIEWER_RATING, M_RELEASE_YEAR, CR_ID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING M_ID
    """,
    (
        movie_data["watchmode_id"],
        movie_data["imdb"],
        movie_data["tmdb"],
        movie_data["title"],
        movie_data["plot"],
        movie_data["runtime"],
        movie_data["viewer_rating"],
        movie_data["release_year"],
        movie_data["cr_id"]
    )
)
movie_id = cursor.fetchone()[0]

# Insert the AKA for the new movie
cursor.execute(
    """
    INSERT INTO AKA (M_ID, AKA_TITLE)
    VALUES (%s, %s)
    """,
    (movie_id, aka_title)
)
'''