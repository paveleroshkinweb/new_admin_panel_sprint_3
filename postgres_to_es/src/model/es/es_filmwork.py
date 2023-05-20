from typing import Any
from uuid import UUID

from settings import ElasticSettings
from .person import Person
from .es_model import ESModel, ESMeta


es_settings = ElasticSettings()
filmwork_meta = ESMeta(index=es_settings.movies_index_name, version=es_settings.movies_index_version)


class ESFilmwork(ESModel):

    id: UUID

    imdb_rating: float

    title: str

    description: str | None

    genre: list[str]

    director: list[str]

    actors_names: list[str]

    writers_names: list[str]

    actors: list[Person]

    writers: list[Person]

    @classmethod
    def get_meta_info(cls) -> ESMeta:
        return filmwork_meta

    def get_document_id(self) -> Any:
        return str(self.id)
