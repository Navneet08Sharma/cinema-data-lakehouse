import os

import dlt
import duckdb
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

if not api_key:
    raise ValueError("TMDB_API_KEY is not set in .env")


DB_PATH = "cinema_pipeline.duckdb"

MOVIE_CREDITS_URL = "https://api.themoviedb.org/3/movie/{}/credits"
TV_CREDITS_URL = "https://api.themoviedb.org/3/tv/{}/aggregate_credits"

MAX_MOVIES = 5
MAX_TV_SHOWS = 5


def get_media_ids():

    con = duckdb.connect(DB_PATH)

    movies = con.execute(
        f"""
        SELECT id
        FROM cinema_data.movies
        ORDER BY id
        LIMIT {MAX_MOVIES}
        """
    ).fetchall()

    tv_shows = con.execute(
        f"""
        SELECT id
        FROM cinema_data.tv_shows
        ORDER BY id
        LIMIT {MAX_TV_SHOWS}
        """
    ).fetchall()

    con.close()

    movie_ids = [row[0] for row in movies]
    tv_ids = [row[0] for row in tv_shows]

    return movie_ids, tv_ids


def get_movie_credits(movie_id):

    url = MOVIE_CREDITS_URL.format(movie_id)

    params = {
        "api_key": api_key,
        "language": "en-US",
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def get_tv_credits(tv_id):

    url = TV_CREDITS_URL.format(tv_id)

    params = {
        "api_key": api_key,
        "language": "en-US",
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def create_person_record(person):

    return {
        "person_id": person["id"],
        "name": person["name"],
        "known_for_department": person.get(
            "known_for_department"
        ),
        "profile_path": person.get("profile_path"),
    }


def process_movie(movie_id):

    data = get_movie_credits(movie_id)

    people = []
    credits = []

    for person in data.get("cast", []):

        people.append(create_person_record(person))

        credits.append(
            {
                "credit_id": person.get("credit_id"),
                "media_id": movie_id,
                "media_type": "movie",
                "person_id": person["id"],
                "role_type": "cast",
                "character_name": person.get("character"),
                "job": None,
                "cast_order": person.get("order"),
            }
        )

    for person in data.get("crew", []):

        people.append(create_person_record(person))

        credits.append(
            {
                "credit_id": person.get("credit_id"),
                "media_id": movie_id,
                "media_type": "movie",
                "person_id": person["id"],
                "role_type": "crew",
                "character_name": None,
                "job": person.get("job"),
                "cast_order": None,
            }
        )

    return people, credits


def process_tv(tv_id):

    data = get_tv_credits(tv_id)

    people = []
    credits = []

    for person in data.get("cast", []):

        people.append(create_person_record(person))

        roles = person.get("roles", [])

        for role in roles:

            credits.append(
                {
                    "credit_id": role.get("credit_id"),
                    "media_id": tv_id,
                    "media_type": "tv",
                    "person_id": person["id"],
                    "role_type": "cast",
                    "character_name": role.get("character"),
                    "job": None,
                    "cast_order": person.get("order"),
                }
            )

    for person in data.get("crew", []):

        people.append(create_person_record(person))

        jobs = person.get("jobs", [])

        for job in jobs:

            credits.append(
                {
                    "credit_id": job.get("credit_id"),
                    "media_id": tv_id,
                    "media_type": "tv",
                    "person_id": person["id"],
                    "role_type": "crew",
                    "character_name": None,
                    "job": job.get("job"),
                    "cast_order": None,
                }
            )

    return people, credits


movie_ids, tv_ids = get_media_ids()

print("Movies selected:", movie_ids)
print("TV shows selected:", tv_ids)


all_people = []
all_credits = []


for movie_id in movie_ids:

    print(f"\nProcessing movie: {movie_id}")

    people, credits = process_movie(movie_id)

    all_people.extend(people)
    all_credits.extend(credits)


for tv_id in tv_ids:

    print(f"\nProcessing TV show: {tv_id}")

    people, credits = process_tv(tv_id)

    all_people.extend(people)
    all_credits.extend(credits)


unique_people = {}

for person in all_people:

    unique_people[person["person_id"]] = person


unique_credits = {}

for credit in all_credits:

    credit_id = credit["credit_id"]

    if credit_id:
        unique_credits[credit_id] = credit


people_resource = dlt.resource(
    list(unique_people.values()),
    name="people",
    primary_key="person_id",
    write_disposition="merge",
)


credits_resource = dlt.resource(
    list(unique_credits.values()),
    name="credits",
    primary_key="credit_id",
    write_disposition="merge",
)


pipeline = dlt.pipeline(
    pipeline_name="cinema_pipeline",
    destination="duckdb",
    dataset_name="cinema_data",
)


load_info = pipeline.run(
    [
        people_resource,
        credits_resource,
    ]
)


print("\nCredits pipeline completed!")

print(load_info)