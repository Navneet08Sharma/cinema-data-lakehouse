import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        p.name,
        m.title,
        m.release_date,
        cr.role_type,
        cr.character_name,
        cr.job
    FROM cinema_data.credits cr
    JOIN cinema_data.people p
        ON cr.person_id = p.person_id
    JOIN cinema_data.movies m
        ON cr.media_id = m.id
    WHERE cr.media_type = 'movie'
      AND (
          (p.name = 'Christopher Nolan' AND cr.role_type = 'crew' AND cr.job = 'Director')
          OR
          (p.name = 'Christian Bale' AND cr.role_type = 'cast')
      )
    ORDER BY p.name, m.release_date
""" ).fetchall()


print("\nPerson filmography:\n")


for row in results:
    print(row)


con.close()