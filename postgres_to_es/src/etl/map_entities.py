from typing import Dict, Any

from model import AggregatedFilmwork, ESFilmwork, PersonRole, RoleType, Person


def map_dbfilmwork_to_es(db_filmwork: AggregatedFilmwork) -> ESFilmwork:
    person_information = get_person_information(db_filmwork.persons)
    return ESFilmwork(
        id=db_filmwork.id,
        imdb_rating=db_filmwork.rating,
        title=db_filmwork.title,
        description=db_filmwork.description,
        genre=db_filmwork.genres,
        director=person_information['director'],
        actors_names=person_information['actors_names'],
        writers_names=person_information['writers_names'],
        actors=person_information['actors'],
        writers=person_information['writers']
    )


def get_person_information(persons: list[PersonRole]) -> Dict[str, Any]:
    director = []
    actors_names = []
    writers_names = []
    actors = []
    writers = []

    for person in persons:
        if person.person_role == RoleType.DIRECTOR:
            director.append(person.person_name)
        elif person.person_role == RoleType.ACTOR:
            actors_names.append(person.person_name)
            actors.append(Person(id=person.person_id, name=person.person_name))
        elif person.person_role == RoleType.WRITER:
            writers_names.append(person.person_name)
            writers.append(Person(id=person.person_id, name=person.person_name))

    return {
        'director': director,
        'actors_names': actors_names,
        'writers_names': writers_names,
        'actors': actors,
        'writers': writers
    }
