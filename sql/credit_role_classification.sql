CREATE OR REPLACE VIEW cinema_data.credit_roles AS

SELECT
    credit_id,
    media_id,
    media_type,
    person_id,
    role_type,
    character_name,
    job,
    cast_order,

    CASE

        WHEN role_type = 'cast'
             AND cast_order <= 9
            THEN 'PRIMARY'

        WHEN role_type = 'cast'
            THEN 'SECONDARY'

        WHEN role_type = 'crew'
             AND job IN (
                'Director'
             )
            THEN 'PRIMARY'

        WHEN role_type = 'crew'
             AND job IN (
                'Writer',
                'Screenplay',
                'Story',
                'Producer',
                'Executive Producer',
                'Original Music Composer',
                'Music'
             )
            THEN 'SECONDARY'

        WHEN role_type = 'crew'
            THEN 'TECHNICAL'

        ELSE 'OTHER'

    END AS role_category

FROM cinema_data.credits;