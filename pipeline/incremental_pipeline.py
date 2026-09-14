import os
from datetime import datetime, timedelta, timezone

import dlt
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


CHANGES_URL = "https://api.themoviedb.org/3/movie/changes"
MOVIE_URL = "https://api.themoviedb.org/3/movie"

MAX_MOVIES = 20


def get_changed_movie_ids(start_date, end_date):
    params = {
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "page": 1,
    }

    response = requests.get(CHANGES_URL, params=params)

    response.raise_for_status()

    data = response.json()

    results = data["results"]

    movie_ids = [movie["id"] for movie in results]

    movie_ids = list(dict.fromkeys(movie_ids))

    return movie_ids[:MAX_MOVIES]


def get_movie_details(movie_id):
    url = f"{MOVIE_URL}/{movie_id}"

    params = {
        "api_key": api_key,
        "language": "en-US",
    }

    response = requests.get(url, params=params)

    if response.status_code == 404:
        print(f"Movie not found, skipping: {movie_id}")
        return None

    response.raise_for_status()

    return response.json()


@dlt.resource(
    name="movies",
    primary_key="id",
    write_disposition="merge",
    columns={
        "belongs_to_collection": {
            "data_type": "text"
        }
    },
)
def changed_movies():
    state = dlt.current.resource_state()

    today = datetime.now(timezone.utc).date()

    last_checked = state.get("last_checked_date")

    if last_checked:
        start_date = last_checked
    else:
        start_date = (today - timedelta(days=1)).isoformat()

    end_date = today.isoformat()

    print(f"Checking TMDB changes from {start_date} to {end_date}")

    movie_ids = get_changed_movie_ids(
        start_date,
        end_date,
    )

    print(f"Processing {len(movie_ids)} changed movie IDs")

    successful_movies = 0

    for movie_id in movie_ids:
        movie = get_movie_details(movie_id)

        if movie is not None:
            print(f"Fetched movie: {movie_id}")

            successful_movies += 1

            yield movie

    state["last_checked_date"] = end_date

    print(f"\nMovies fetched successfully: {successful_movies}")
    print(f"Checkpoint saved: {end_date}")


pipeline = dlt.pipeline(
    pipeline_name="cinema_pipeline",
    destination="duckdb",
    dataset_name="cinema_data",
)


load_info = pipeline.run(changed_movies())


print("\nIncremental pipeline completed!")
print(load_info)