CREATE OR REPLACE VIEW cinema_data.director_movie_stats AS
SELECT
    p.person_id,
    p.name AS director_name,
    COUNT(DISTINCT m.id) AS movies_directed,
    ROUND(AVG(m.vote_average), 2) AS average_rating,
    ROUND(MAX(m.vote_average), 2) AS highest_rating
FROM cinema_data.credits cr
JOIN cinema_data.people p
    ON cr.person_id = p.person_id
JOIN cinema_data.movies m
    ON cr.media_id = m.id
WHERE cr.media_type = 'movie'
  AND cr.role_type = 'crew'
  AND cr.job = 'Director'
GROUP BY
    p.person_id,
    p.name;