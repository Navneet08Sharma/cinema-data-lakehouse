import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


result = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT id) AS unique_movie_ids
    FROM cinema_data.movies
""").fetchone()


print("Total rows in DuckDB:", result[0])
print("Unique movie IDs:", result[1])


con.close()