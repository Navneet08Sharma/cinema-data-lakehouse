import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


print("\nMovie relationships:\n")

movie_results = con.execute("""
    SELECT
        m.title,
        p.name,
        c.role_type,
        c.character_name,
        c.job
    FROM cinema_data.credits c
    JOIN cinema_data.people p
        ON c.person_id = p.person_id
    JOIN cinema_data.movies m
        ON c.media_id = m.id
    WHERE c.media_type = 'movie'
    ORDER BY m.title, p.name
    LIMIT 15
""").fetchall()


for row in movie_results:
    print(row)


print("\nTV relationships:\n")

tv_results = con.execute("""
    SELECT
        t.name,
        p.name,
        c.role_type,
        c.character_name,
        c.job
    FROM cinema_data.credits c
    JOIN cinema_data.people p
        ON c.person_id = p.person_id
    JOIN cinema_data.tv_shows t
        ON c.media_id = t.id
    WHERE c.media_type = 'tv'
    ORDER BY t.name, p.name
    LIMIT 15
""").fetchall()


for row in tv_results:
    print(row)


con.close()