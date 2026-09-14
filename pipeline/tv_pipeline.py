import os

import dlt
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


url = "https://api.themoviedb.org/3/tv/popular"


def get_tv_shows():
    all_shows = []

    for page in range(1, 6):

        params = {
            "api_key": api_key,
            "language": "en-US",
            "page": page,
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        shows = data["results"]

        all_shows.extend(shows)

        print(f"Page {page}: {len(shows)} TV shows received")

    return all_shows


shows = get_tv_shows()

print(f"\nTotal TV shows received: {len(shows)}")


tv_resource = dlt.resource(
    shows,
    name="tv_shows",
    primary_key="id",
    write_disposition="merge",
)


pipeline = dlt.pipeline(
    pipeline_name="cinema_pipeline",
    destination="duckdb",
    dataset_name="cinema_data",
)


load_info = pipeline.run(tv_resource)


print("\nTV pipeline completed!")
print(load_info)