import os
from datetime import datetime, timedelta, timezone

import dlt
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


CHANGES_URL = "https://api.themoviedb.org/3/tv/changes"
TV_URL = "https://api.themoviedb.org/3/tv"

MAX_SHOWS = 20


def get_changed_tv_ids(start_date, end_date):
    params = {
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "page": 1,
    }

    response = requests.get(CHANGES_URL, params=params)

    response.raise_for_status()

    data = response.json()

    shows = data["results"]

    tv_ids = [show["id"] for show in shows]

    tv_ids = list(dict.fromkeys(tv_ids))

    return tv_ids[:MAX_SHOWS]


def get_tv_details(tv_id):
    url = f"{TV_URL}/{tv_id}"

    params = {
        "api_key": api_key,
        "language": "en-US",
    }

    response = requests.get(url, params=params)

    if response.status_code == 404:
        print(f"TV show not found, skipping: {tv_id}")
        return None

    response.raise_for_status()

    return response.json()


@dlt.resource(
    name="tv_shows",
    primary_key="id",
    write_disposition="merge",
)
def changed_tv_shows():

    state = dlt.current.resource_state()

    today = datetime.now(timezone.utc).date()

    last_checked = state.get("last_checked_date")

    if last_checked:
        start_date = last_checked
    else:
        start_date = (today - timedelta(days=1)).isoformat()

    end_date = today.isoformat()

    print(
        f"Checking TMDB TV changes "
        f"from {start_date} to {end_date}"
    )

    tv_ids = get_changed_tv_ids(
        start_date,
        end_date,
    )

    print(f"Processing {len(tv_ids)} changed TV IDs")

    successful_shows = 0

    for tv_id in tv_ids:

        show = get_tv_details(tv_id)

        if show is not None:

            print(f"Fetched TV show: {tv_id}")

            successful_shows += 1

            yield show

    state["last_checked_date"] = end_date

    print(f"\nTV shows fetched successfully: {successful_shows}")

    print(f"Checkpoint saved: {end_date}")


pipeline = dlt.pipeline(
    pipeline_name="cinema_pipeline",
    destination="duckdb",
    dataset_name="cinema_data",
)


load_info = pipeline.run(changed_tv_shows())


print("\nTV incremental pipeline completed!")

print(load_info)