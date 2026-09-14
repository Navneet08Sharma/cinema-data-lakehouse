import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


tv_id = 108978

url = f"https://api.themoviedb.org/3/tv/{tv_id}/aggregate_credits"

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


print("\nTV series credits:")

print("Cast members:", len(cast))
print("Crew members:", len(crew))


print("\nFirst 10 cast members:\n")

for person in cast[:10]:

    roles = person.get("roles", [])

    character = roles[0].get("character") if roles else None

    print(
        person["id"],
        "-",
        person["name"],
        "-",
        character,
    )


print("\nDirectors:\n")

for person in crew:

    jobs = person.get("jobs", [])

    for job in jobs:

        if job.get("job") == "Director":

            print(
                person["id"],
                "-",
                person["name"],
            )

            break