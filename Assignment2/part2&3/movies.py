import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_URL_PARAM = f"?apiKey={API_KEY}"
API_URL = "https://api.watchmode.com/v1/"

def appendParams(url, params):
    for key, value in params.items():
        url += f"&{key}={value}"
    return url

def getMovieList():
    url = f"{API_URL}{API_KEY_URL_PARAM}/list-titles/"
    params = {

    }
    url = appendParams(url, params)
    
    response = requests.get(url)
    response.raise_for_status()
    return response.json()