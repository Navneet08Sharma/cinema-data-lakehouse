CREATE OR REPLACE VIEW cinema_data.person_achievements AS

SELECT
    p.person_id,
    p.name,
    p.known_for_department,

    COUNT(DISTINCT CASE
        WHEN cr.media_type='movie'
        THEN m.id
    END) AS movies_involved,

    COUNT(DISTINCT CASE
        WHEN cr.media_type='movie'
         AND cr.role_type='cast'
         AND cr.cast_order<=9
        THEN m.id
    END) AS primary_cast_movies,

    COUNT(DISTINCT CASE
        WHEN cr.media_type='movie'
         AND cr.job='Director'
        THEN m.id
    END) AS directed_movies,

    ROUND(AVG(CASE
        WHEN cr.media_type='movie'
        THEN m.vote_average
    END),2) AS average_movie_rating,

    ROUND(MAX(CASE
        WHEN cr.media_type='movie'
        THEN m.vote_average
    END),2) AS highest_movie_rating

FROM cinema_data.people p

LEFT JOIN cinema_data.credits cr
    ON p.person_id = cr.person_id

LEFT JOIN cinema_data.movies m
    ON cr.media_id = m.id
   AND cr.media_type='movie'

GROUP BY
    p.person_id,
    p.name,
    p.known_for_department;