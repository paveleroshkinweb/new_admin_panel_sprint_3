from elasticsearch import Elasticsearch

import logging
import json
import os

from model import ESModel, ESMeta


logger = logging.getLogger(__name__)


class ESHandler:

    def __init__(self, es_client: Elasticsearch, schema_path: str) -> None:
        self.es_client = es_client
        self.schema_path = schema_path
        self.indexes_created_cache = {}

    def bulk(self, data: list[ESModel]) -> None:
        logger.info(f"Updating {len(data)} entries")
        if not data:
            return
        meta_info = data[0].get_meta_info()
        actions = []
        for model in data:
            logger.debug(f"Preparing document: {model.get_document_id()}")
            action = {
                'index': {
                    '_index': meta_info.index,
                    '_id': model.get_document_id()
                }
            }
            doc = model.dict()

            actions.append(action)
            actions.append(doc)

        self.es_client.bulk(index=meta_info.index, operations=actions)

    def create_index_if_not_exist(self, meta: ESMeta):
        logger.info(f"Creating index {meta.index} with a version: {meta.version}")
        file_path = os.path.join(os.getcwd(), self.schema_path, meta.index)
        schema_index_path_file = f'{file_path}.json'
        with open(schema_index_path_file, 'r') as schema_config:
            config = json.load(schema_config)
            self.es_client.indices.create(
                index=meta.index,
                body=config[meta.version],
                ignore=400
            )
