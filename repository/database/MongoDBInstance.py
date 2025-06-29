from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class MongoDBInstance:
    uri: str
    client: MongoClient
    database: any
    database_name: str

    def __init__(self, uri: str, database_name: str):
        self.uri = uri
        self.database_name = database_name
        self.client = MongoClient(uri)
        self.database = self.client[self.database_name]

    def get(self, collection_name: str, _id: str):
        collection = self.database[collection_name]
        query = {"_id": ObjectId(_id)}

        return collection.findOne(query)

    def create(self, collection_name: str, entry: dict) -> InsertOneResult:
        collection = self.database[collection_name]
        return collection.insert_one(entry)

    def update(self, collection_name: str, _id: str, entry: dict) -> UpdateResult:
        collection = self.database[collection_name]
        query = {"_id": ObjectId(_id)}
        updated_data = {
            "$set": entry,
        }

        return collection.update_one(query, updated_data)

    def delete(self, collection_name: str, _id: str) -> DeleteResult:
        collection = self.database[collection_name]
        query = {"_id": ObjectId(_id)}
        return collection.delete_one(query)


