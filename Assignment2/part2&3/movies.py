import json
import os

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": "db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")
API_KEY_URL_PARAM = f"?apiKey={WATCHMODE_API_KEY}"
WATCHMODE_API_URL = "https://api.watchmode.com/v1"

FREE_MOVIE_DB_URL = "https://imdb.iamidiotareyoutoo.com"

DUMP_DATA_PATH = "./data"

def appendParams(url, params, first=True):
    for key, value in params.items():
        if first:
            url += f"?{key}={value}"
            first = False
        else:
            url += f"&{key}={value}"
    return url

def loadJSON(file_path):
    """
    Load a JSON file and return the data as a Python object.

    :param file_path: Path to the JSON file.
    :return: Python object representing the JSON data.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def saveJSON(data, dumpPath):
    """
    Save the data to a JSON file.

    :param data: Data to be saved.
    :param dumpPath: Path to the JSON file.
    """
    os.makedirs(os.path.dirname(dumpPath), exist_ok=True)
    with open(dumpPath, "w") as f:
        json.dump(data, f)

def getMovieList(count = 250, DEBUG=False):
    '''
    List the specified number of movies from the Watchmode API and save the data to a JSON file.
    '''
    dumpPath = f"{DUMP_DATA_PATH}/watchmode/" + f"{count}_movies.json"
    if os.path.exists(dumpPath):
        if DEBUG:
            print(f"Data already exists at {dumpPath}")
        return dumpPath
    
    # TODO: Fetch all pages when count > 250
    if count > 250:
        raise ValueError("The maximum number of movies that can be listed is 250.")
    
    url = f"{WATCHMODE_API_URL}/list-titles/{API_KEY_URL_PARAM}"
    params = {
        "types": "movie",
        "release_date_start": 19900101,
        "release_date_end": 20220101,
        "limit": count,
        "page": 1
    }
    url = appendParams(url, params, first=False)
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    saveJSON(data, dumpPath)

    if DEBUG:
        print(f"Saved movie list to {dumpPath}")
    return dumpPath

def getMovieDetails(IMDB_ID, DEBUG=False):
    '''
    Get the details of a movie from the Free-Movie DB API.
    '''
    dumpPath = f"{DUMP_DATA_PATH}/fmdb/" + f"{IMDB_ID}_details.json"
    if os.path.exists(dumpPath):
        if DEBUG:
            print(f"Data already exists at {dumpPath}")
        return dumpPath
    
    url = f"{FREE_MOVIE_DB_URL}/search/"
    params = {
        "tt": IMDB_ID
    }
    url = appendParams(url, params)

    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    saveJSON(data, dumpPath)
    
    if DEBUG:
        print(f"Saved movie details to {dumpPath}")
    return dumpPath

def sanitizeString(value):
    """
    Sanitize a string by replacing or removing characters that might cause errors in PostgreSQL.
    """
    if not isinstance(value, str):
        return value
    # return value.replace(";", " ").replace("'", " ").replace('"', " ")
    return value.replace(";", " ")

def prepareMovieData(watchmodeData):
    preparedMovies = []
    for movie in watchmodeData["titles"]:
        fmdbData = loadJSON(f"{DUMP_DATA_PATH}/fmdb/" + f"{movie["imdb_id"]}_details.json")
        
        keywords = [sanitizeString(keyword) for keyword in fmdbData["short"]["keywords"].split(",")]
        aka = [sanitizeString(edge["node"]["text"]) for edge in fmdbData["main"]["akas"]["edges"]]
        
        originalTitle = sanitizeString(fmdbData["top"]["originalTitleText"]["text"])
        if movie["title"] != originalTitle:
            aka.append(sanitizeString(originalTitle))
        spokenLanguages = [
            {"name": sanitizeString(lang["text"]), "code": lang["id"]} for lang in fmdbData["main"]["spokenLanguages"]["spokenLanguages"]
        ]
        directors = [sanitizeString(director["name"]) for director in fmdbData["short"]["director"]]
        actors = [sanitizeString(actor["name"]) for actor in fmdbData["short"]["actor"]]
        countries = [
            {"name": sanitizeString(country["text"]), "code": country["id"]} for country in fmdbData["main"]["countriesOfOrigin"]["countries"]
        ]
        data = {
            "watchmode_id": movie["id"],
            "imdb": movie["imdb_id"],
            "tmdb": movie["tmdb_id"],
            "title":sanitizeString(movie["title"]),
            "plot": sanitizeString(fmdbData["short"]["description"]),
            "runtime": fmdbData["top"]["runtime"]["seconds"],
            "viewer_rating": fmdbData["short"]["aggregateRating"]["ratingValue"],
            "release_year": fmdbData["top"]["releaseYear"]["year"],
            "review_count": fmdbData["top"]["reviews"]["total"],
            "content_rating": sanitizeString(fmdbData["top"]["certificate"]["rating"]),
            "aka": aka,
            "keywords": keywords,
            "languages": spokenLanguages,
            "directors": directors,
            "countries": countries,
            "actors": actors,
            "genres": [sanitizeString(genre) for genre in fmdbData["short"]["genre"]],
        }

        preparedMovies.append(data)
    
    return preparedMovies

def createNewContentRating(cursor, contentRating):
    cursor.execute("SELECT CR_ID FROM content_rating WHERE CR_RATING = %s", (contentRating,))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute(
        "INSERT INTO content_rating (CR_RATING) VALUES (%s) RETURNING CR_ID",
        (contentRating,)
        )
        print(f"Created new content_rating: {contentRating}")
        return cursor.fetchone()[0]

def createNewLanguage(cursor, language):    
    cursor.execute("SELECT L_ID FROM language WHERE L_CODE = %s", (language["code"],))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO language (L_NAME, L_CODE) VALUES (%s, %s) RETURNING L_ID", (language["name"], language["code"]))
        print(f"Created new language '{language["name"]}': {language['code']}")
        return cursor.fetchone()[0]

def createNewDirector(cursor, director):
    cursor.execute("SELECT D_ID FROM director WHERE D_NAME = %s", (director,))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO director (D_NAME) VALUES (%s) RETURNING D_ID", (director,))
        print(f"Created new director: {director}")
        return cursor.fetchone()[0]

def createNewCountry(cursor, country):
    cursor.execute("SELECT C_ID FROM country WHERE C_CODE = %s", (country["code"],))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO country (C_NAME, C_CODE) VALUES (%s, %s) RETURNING C_ID", (country["name"], country["code"]))
        print(f"Created new country '{country["name"]}': {country['code']}")
        return cursor.fetchone()[0]

def createNewActor(cursor, actor):
    cursor.execute("SELECT A_ID FROM actor WHERE A_NAME = %s", (actor,))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO actor (A_NAME) VALUES (%s) RETURNING A_ID", (actor,))
        print(f"Created new actor: {actor}")
        return cursor.fetchone()[0]

def createNewGenre(cursor, genre):
    cursor.execute("SELECT GT_ID FROM genre_type WHERE GT_TYPE = %s", (genre,))
    row = cursor.fetchone()

    if row:
        return row[0]
    else:
        cursor.execute("INSERT INTO genre_type (GT_TYPE) VALUES (%s) RETURNING GT_ID", (genre,))
        print(f"Created new genre: {genre}")
        return cursor.fetchone()[0]

def insertMovie(movieData, conn):
    cursor = conn.cursor()

    # Create new contentRating if it doesn't exist (and return the new id)
    contentRatingId = createNewContentRating(cursor, movieData["content_rating"])
    
    # Create new language if it doesn't exist (and return the new id)
    languageIds = []
    for language in movieData["languages"]:
        id = createNewLanguage(cursor, language)
        languageIds.append(id)

    # Create new director if it doesn't exist (and return the new id)
    directorIds = []
    for director in movieData["directors"]:
        id = createNewDirector(cursor, director)
        directorIds.append(id)

    # Create new country if it doesn't exist (and return the new id)
    countryIds = []
    for country in movieData["countries"]:
        id = createNewCountry(cursor, country)
        countryIds.append(id)

    # Create new actor if it doesn't exist (and return the new id)
    actorIds = []
    for actor in movieData["actors"]:
        id = createNewActor(cursor, actor)
        actorIds.append(id)

    # Create new genre if it doesn't exist (and return the new id)
    genreIds = []
    for genre in movieData["genres"]:
        id = createNewGenre(cursor, genre)
        genreIds.append(id)

    # Insert movie
    cursor.execute(
        """
        INSERT INTO Movie (M_WATCHMODE_ID, M_IMDB, M_TMDB, M_TITLE, M_PLOT, M_RUNTIME, M_VIEWER_RATING, M_RELEASE_YEAR, M_REVIEW_COUNT, CR_ID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING M_ID
        """,
        (
            movieData["watchmode_id"],
            movieData["imdb"],
            movieData["tmdb"],
            movieData["title"],
            movieData["plot"],
            movieData["runtime"],
            movieData["viewer_rating"],
            movieData["release_year"],
            movieData["review_count"],
            contentRatingId
        )
    )
    movieId = cursor.fetchone()[0]

    # Insert akas
    for aka in movieData["aka"]:
        cursor.execute("INSERT INTO aka (M_ID, AKA_TITLE) VALUES (%s, %s)", (movieId, aka))

    # Insert keywords (Note: There are a lot duplicate of keywords. Might be more optimal to store them in a dedicated table.)
    for keyword in movieData["keywords"]:
        cursor.execute("INSERT INTO keyword (M_ID, K_KEYWORD) VALUES (%s, %s)", (movieId, keyword))

    # Insert movieLanguages
    for languageId in languageIds:
        cursor.execute("INSERT INTO movie_language (M_ID, L_ID) VALUES (%s, %s)", (movieId, languageId))
    
    # Insert movieDirectors
    for directorId in directorIds:
        cursor.execute("INSERT INTO movie_director (M_ID, D_ID) VALUES (%s, %s)", (movieId, directorId))

    # Insert movieCountries
    for countryId in countryIds:
        cursor.execute("INSERT INTO movie_country (M_ID, C_ID) VALUES (%s, %s)", (movieId, countryId))
    
    # Insert movieActors
    for actorId in actorIds:
        cursor.execute("INSERT INTO movie_actor (M_ID, A_ID) VALUES (%s, %s)", (movieId, actorId))

    # Insert movieGenres
    for genreId in genreIds:
        cursor.execute("INSERT INTO movie_genre (M_ID, GT_ID) VALUES (%s, %s)", (movieId, genreId))

    cursor.close()

if __name__ == "__main__":
    DEBUG = False
    
    dumpPath = getMovieList(200, DEBUG=DEBUG)
    watchmodeData = loadJSON(dumpPath)

    # Get all movie details from fmdb
    for movie in watchmodeData["titles"]:
        getMovieDetails(movie["imdb_id"], DEBUG=DEBUG)
    
    preparedMovies = prepareMovieData(watchmodeData)

    with psycopg.connect(**DB_CONFIG) as conn:
        for movie in preparedMovies:
            insertMovie(movie, conn)
        # Set the IMDB ids of some movies to NULL
        cursor = conn.cursor()
        cursor.execute("UPDATE movie SET M_IMDB = NULL WHERE M_ID IN (4, 26, 34, 67, 99, 120, 136, 177, 188, 191)")
        cursor.close()

