import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        m.title,
        p.name,
        c.character_name,
        c.cast_order
    FROM cinema_data.credits c
    JOIN cinema_data.people p
        ON c.person_id = p.person_id
    JOIN cinema_data.movies m
        ON c.media_id = m.id
    WHERE c.media_type = 'movie'
      AND c.role_type = 'cast'
    ORDER BY c.media_id, c.cast_order
    LIMIT 15
""").fetchall()


print("\nCast ordered by TMDB billing order:\n")


for row in results:
    print(row)


con.close()