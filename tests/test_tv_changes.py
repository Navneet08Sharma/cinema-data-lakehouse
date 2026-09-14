import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


url = "https://api.themoviedb.org/3/tv/changes"


params = {
    "api_key": api_key,
    "page": 1,
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()

changes = data["results"]


print("Changed TV shows received:", len(changes))

print("\nFirst 10 changed TV IDs:\n")


for show in changes[:10]:
    print(show["id"])