import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


results = con.execute("""
    SELECT
        p.name,
        COUNT(DISTINCT m.id) AS movies_acted_in,
        ROUND(AVG(m.vote_average), 2) AS average_rating,
        ROUND(MAX(m.vote_average), 2) AS highest_rating
    FROM cinema_data.credits cr
    JOIN cinema_data.people p
        ON cr.person_id = p.person_id
    JOIN cinema_data.movies m
        ON cr.media_id = m.id
    WHERE cr.media_type = 'movie'
      AND cr.role_type = 'cast'
      AND cr.cast_order <= 9
    GROUP BY p.person_id, p.name
    HAVING COUNT(DISTINCT m.id) >= 2
    ORDER BY movies_acted_in DESC, average_rating DESC
    LIMIT 20
""").fetchall()


print("\nTop actors by number of primary-cast movies:\n")


for row in results:
    print(row)


con.close()
