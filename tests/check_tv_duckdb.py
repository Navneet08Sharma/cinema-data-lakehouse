import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


result = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT id) AS unique_tv_ids
    FROM cinema_data.tv_shows
""").fetchone()


print("Total TV shows in DuckDB:", result[0])
print("Unique TV IDs:", result[1])


con.close()