import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


url = "https://api.themoviedb.org/3/tv/popular"


params = {
    "api_key": api_key,
    "language": "en-US",
    "page": 1,
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Number of TV shows:", len(data["results"]))

print("\nFirst 5 TV shows:\n")


for show in data["results"][:5]:
    print(
        show["id"],
        "-",
        show["name"],
        "-",
        show["first_air_date"],
        "-",
        show["vote_average"],
    )