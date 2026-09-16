import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        person_id,
        name,
        known_for_department,
        profile_path
    FROM cinema_data.people
    ORDER BY name
    LIMIT 20
""").fetchall()


print("\nPeople currently stored:\n")


for row in results:
    print(row)


con.close()