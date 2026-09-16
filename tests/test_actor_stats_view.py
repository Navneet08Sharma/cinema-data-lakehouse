import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


with open("sql/actor_movie_stats.sql", "r", encoding="utf-8") as file:
    sql = file.read()


con.execute(sql)


results = con.execute("""
    SELECT
        actor_name,
        movies_acted_in,
        average_rating,
        highest_rating
    FROM cinema_data.actor_movie_stats
    ORDER BY movies_acted_in DESC, average_rating DESC
    LIMIT 20
""").fetchall()


print("\nActor movie statistics:\n")


for row in results:
    print(row)


con.close()