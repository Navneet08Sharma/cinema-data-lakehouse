import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        m.id,
        m.title,
        m.release_date,
        m.vote_average
    FROM cinema_data.credits c
    JOIN cinema_data.people p
        ON c.person_id = p.person_id
    JOIN cinema_data.movies m
        ON c.media_id = m.id
    WHERE c.media_type = 'movie'
      AND c.role_type = 'crew'
      AND c.job = 'Director'
      AND p.name = 'Christopher Nolan'
    ORDER BY m.release_date
""").fetchall()


print("\nMovies directed by Christopher Nolan:\n")


if results:

    for movie in results:
        print(movie)

else:

    print("No movies found.")


con.close()