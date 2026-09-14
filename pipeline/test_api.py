import os

import requests
from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv()

# Get the TMDB API key
api_key = os.getenv("TMDB_API_KEY")

# Make sure the API key exists
if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


# TMDB endpoint for popular movies
url = "https://api.themoviedb.org/3/movie/popular"

# Parameters we send to TMDB
params = {
    "api_key": api_key,
    "language": "en-US",
    "page": 1,
}


# Send the request
response = requests.get(url, params=params)

# Show the HTTP status
print("HTTP status:", response.status_code)

# Stop if TMDB returned an error
response.raise_for_status()

# Convert the JSON response into a Python dictionary
data = response.json()

# Show how many movies we received
print("Number of movies:", len(data["results"]))

print("\nFirst 5 movies:\n")

# Display the first 5 movies
for movie in data["results"][:5]:
    print(
        movie["id"],
        "-",
        movie["title"],
        "-",
        movie["release_date"],
        "-",
        movie["vote_average"],
    )