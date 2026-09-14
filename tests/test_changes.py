import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


movie_id = 1434751

url = f"https://api.themoviedb.org/3/movie/{movie_id}"


params = {
    "api_key": api_key,
    "language": "en-US",
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

movie = response.json()


print("\nMovie details:\n")

print("ID:", movie["id"])
print("Title:", movie["title"])
print("Release date:", movie["release_date"])
print("Rating:", movie["vote_average"])