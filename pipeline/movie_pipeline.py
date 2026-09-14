import os

import dlt
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


url = "https://api.themoviedb.org/3/movie/popular"


def get_movies():
    all_movies = []

    for page in range(1, 6):

        params = {
            "api_key": api_key,
            "language": "en-US",
            "page": page,
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        movies = data["results"]

        all_movies.extend(movies)

        print(f"Page {page}: {len(movies)} movies received")

    return all_movies


movies = get_movies()

print(f"\nTotal movies received: {len(movies)}")


movies_resource = dlt.resource(
    movies,
    name="movies",
    primary_key="id",
    write_disposition="merge",
)


pipeline = dlt.pipeline(
    pipeline_name="cinema_pipeline",
    destination="duckdb",
    dataset_name="cinema_data",
)


load_info = pipeline.run(movies_resource)


print("\nPipeline completed!")
print(load_info)