import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        m.title,
        p.name,
        cr.character_name,
        cr.cast_order
    FROM cinema_data.credit_roles cr
    JOIN cinema_data.people p
        ON cr.person_id = p.person_id
    JOIN cinema_data.movies m
        ON cr.media_id = m.id
    WHERE cr.media_type = 'movie'
      AND cr.role_category = 'PRIMARY'
      AND cr.role_type = 'cast'
      AND m.id = 155
    ORDER BY cr.cast_order
""").fetchall()


print("\nPrimary cast of The Dark Knight:\n")


for row in results:
    print(row)


con.close()