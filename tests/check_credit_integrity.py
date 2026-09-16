import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


print("\nMOVIE CREDIT INTEGRITY:")

movie_orphans = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.credits c
    LEFT JOIN cinema_data.movies m
        ON c.media_id = m.id
    WHERE c.media_type = 'movie'
      AND m.id IS NULL
""").fetchone()[0]

print("Movie credits without matching movie:", movie_orphans)


print("\nTV CREDIT INTEGRITY:")

tv_orphans = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.credits c
    LEFT JOIN cinema_data.tv_shows t
        ON c.media_id = t.id
    WHERE c.media_type = 'tv'
      AND t.id IS NULL
""").fetchone()[0]

print("TV credits without matching TV show:", tv_orphans)


print("\nPEOPLE CREDIT INTEGRITY:")

person_orphans = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.credits c
    LEFT JOIN cinema_data.people p
        ON c.person_id = p.person_id
    WHERE p.person_id IS NULL
""").fetchone()[0]

print("Credits without matching person:", person_orphans)


print("\nCREDITS BY MEDIA TYPE:")

media_counts = con.execute("""
    SELECT
        media_type,
        COUNT(*) AS total_credits
    FROM cinema_data.credits
    GROUP BY media_type
    ORDER BY media_type
""").fetchall()

for row in media_counts:
    print(row)


con.close()