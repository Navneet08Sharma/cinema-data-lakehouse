import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


with open("sql/director_movie_stats.sql", "r", encoding="utf-8") as file:
    sql = file.read()


con.execute(sql)


results = con.execute("""
    SELECT
        director_name,
        movies_directed,
        average_rating,
        highest_rating
    FROM cinema_data.director_movie_stats
    ORDER BY movies_directed DESC, average_rating DESC
    LIMIT 20
""").fetchall()


print("\nDirector movie statistics:\n")


for row in results:
    print(row)


con.close()