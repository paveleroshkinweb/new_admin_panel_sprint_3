SELECT_UPDATED_MOVIES = """
SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null),
        '[]'
    ) as persons,
    array_agg(DISTINCT g.name) as genres,
    GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) AS last_modified
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw
        ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p
        ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw
        ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g
        ON g.id = gfw.genre_id
    GROUP BY fw.id
    HAVING GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified)) >= '{last_processed_time}'
    ORDER BY last_modified;
"""
