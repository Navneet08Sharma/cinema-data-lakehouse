import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


tv_id = 108978

url = f"https://api.themoviedb.org/3/tv/{tv_id}"

params = {
    "api_key": api_key,
    "language": "en-US",
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

show = response.json()


print("\nTV show details:\n")

print("ID:", show["id"])
print("Name:", show["name"])
print("First air date:", show["first_air_date"])
print("Rating:", show["vote_average"])
print("Number of seasons:", show["number_of_seasons"])
print("Number of episodes:", show["number_of_episodes"])
print("Status:", show["status"])