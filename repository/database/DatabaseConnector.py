from datetime import datetime

from pymongo.results import InsertOneResult, UpdateResult

from environment.EnvironmentParser import EnvironmentParser
from repository.database.MongoDBInstance import MongoDBInstance


class DatabaseConnector:
    db_connection: MongoDBInstance
    collection_name: str
    environment_parser: EnvironmentParser

    def __init__(self, collection_name: str, environment_parser: EnvironmentParser=EnvironmentParser()):
        self.environment_parser = environment_parser
        self.db_connection = MongoDBInstance(self.environment_parser.db_uri, self.environment_parser.database_name)
        self.collection_name = collection_name

    def get(self, _id: str):
        return self.db_connection.get(self.collection_name, _id)

    def create(self, entry: dict) -> InsertOneResult:
        entry["created_at"] = str(datetime.now())
        entry["updated_at"] = str(datetime.now())
        return self.db_connection.create(self.collection_name, entry)

    def update(self, entry: dict) -> UpdateResult:
        entry["updated_at"] = str(datetime.now())
        return self.db_connection.update(self.collection_name, entry["_id"], entry)