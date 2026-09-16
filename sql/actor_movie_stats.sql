CREATE OR REPLACE VIEW cinema_data.actor_movie_stats AS
SELECT
    p.person_id,
    p.name AS actor_name,
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
GROUP BY
    p.person_id,
    p.name;