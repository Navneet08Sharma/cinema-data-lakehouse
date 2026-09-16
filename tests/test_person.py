import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


person_id = 525

url = f"https://api.themoviedb.org/3/person/{person_id}"

params = {
    "api_key": api_key,
    "language": "en-US",
}


response = requests.get(url, params=params)

print("HTTP status:", response.status_code)

response.raise_for_status()

person = response.json()


print("\nPerson details:")

print("ID:", person["id"])
print("Name:", person["name"])
print("Known for department:", person.get("known_for_department"))
print("Birthday:", person.get("birthday"))
print("Place of birth:", person.get("place_of_birth"))
print("Biography length:", len(person.get("biography", "")))