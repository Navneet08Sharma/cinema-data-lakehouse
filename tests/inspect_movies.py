import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


result = con.execute("""
    SELECT
        id,
        title,
        release_date,
        vote_average,
        budget,
        revenue,
        runtime,
        status
    FROM cinema_data.movies
    ORDER BY id
    LIMIT 10
""").fetchall()


print("\nSample movies:\n")

for movie in result:
    print(movie)


con.close()