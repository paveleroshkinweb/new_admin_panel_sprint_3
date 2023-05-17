get_changed_rows_query = f"""
            with changed_rows_in_film_work as (
                SELECT fw.id, fw.rating, fw.title, fw.description, fw.modified, g.name genre,
                       pfw.role, p.id person_id, p.full_name person_full_name
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.modified > '{modified}'
            )
            ,changed_rows_in_genre as (
                SELECT fw.id, fw.rating, fw.title, fw.description, g.modified, g.name genre,
                       pfw.role, p.id person_id, p.full_name person_full_name
                  FROM content.genre g
                  JOIN content.genre_film_work gfw on gfw.genre_id = g.id
                  JOIN content.film_work fw on fw.id = gfw.film_work_id
                  left join content.person_film_work pfw on pfw.film_work_id = fw.id
                  left join content.person p on p.id = pfw.person_id
                 WHERE g.modified > '{modified}'
            )
            ,changed_rows_in_person as (
                SELECT fw.id, fw.rating, fw.title, fw.description, p.modified, g.name genre,
                       pfw.role, p.id person_id, p.full_name person_full_name
                  FROM content.person p
                  JOIN content.person_film_work pfw on pfw.person_id = p.id
                  JOIN content.film_work fw on fw.id = pfw.film_work_id
                  LEFT JOIN content.genre_film_work gfw on gfw.film_work_id = fw.id
                  LEFT JOIN content.genre g on g.id = gfw.genre_id
                 WHERE p.modified > '{modified}'
            )
            ,all_changed_rows as (
                SELECT * FROM changed_rows_in_film_work UNION ALL
                SELECT * FROM changed_rows_in_genre UNION ALL
                SELECT * FROM changed_rows_in_person
            )
            ,all_changed_rows_deduplicated AS (
                SELECT id, rating, title, description, max(modified) as modified, genre,
                       role, person_id, person_full_name
                  FROM all_changed_rows
                 GROUP BY id, rating, title, description, genre, role, person_id, person_full_name
            )
            ,aggregate_genres_and_roles_to_json as (
                SELECT id, rating, title, description, modified,
                       array_agg(DISTINCT genre) as genre,
                       COALESCE (
                           json_agg(
                               DISTINCT jsonb_build_object(
                                   'person_role', role,
                                   'person_id', person_id,
                                   'person_name', person_full_name
                               )
                           ) FILTER (WHERE person_id is not null),
                       '[]'
                   ) as persons
                  FROM all_changed_rows_deduplicated
                 GROUP BY id, rating, title, description, modified
            )
            
            select id, rating, title, description, modified, persons, genre
              from aggregate_genres_and_roles_to_json;
            """