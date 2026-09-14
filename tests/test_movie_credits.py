import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


movie_id = 27205

url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

params = {
    "api_key": api_key,
    "language": "en-US",
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()


cast = data["cast"]
crew = data["crew"]


print("\nMovie credits:")

print("Cast members:", len(cast))
print("Crew members:", len(crew))


print("\nFirst 10 cast members:\n")

for person in cast[:10]:
    print(
        person["id"],
        "-",
        person["name"],
        "-",
        person.get("character"),
    )


print("\nDirectors:\n")

for person in crew:

    if person.get("job") == "Director":
        print(
            person["id"],
            "-",
            person["name"],
        )