from pydantic import BaseModel


class DBMetaInfo(BaseModel):

    postgres_table_name: str

    postgres_schema: str
