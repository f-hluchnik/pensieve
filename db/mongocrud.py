import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

class MongoCRUD:
    def __init__(self):
        load_dotenv()
        self.client = MongoClient(os.getenv('MONGO_URI'))
        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available.")
        else:
            cursor = self.client[os.getenv('DB_NAME')]
            self.collection = cursor[os.getenv('COLLECTION_NAME')]

    def read(self, count=1):
        """
        read ... Function reads data from the database. It reads them descending by time.
        The default amount is 1 row, it is possible to change it by providing an integer parameter.
        """
        documents = self.collection.find(limit=count).sort('time', -1)
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, newDocument):
        """
        write ... Function inserts one row in the database. It expects JSON object as input.
        """
        print('Writing Data')
        print(newDocument)
        response = self.collection.insert_one(newDocument)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self, objectId, updatedQuestion):
        """
        update ... Function updates existing document based on ObjectId. It expects objectId as
        a string and newQuestion as a dictionary as arguments.
        """
        filter = {"_id": ObjectId(objectId)}
        updatedValue = {"$set": updatedQuestion}
        response = self.collection.update_one(filter, updatedValue)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, objectId):
        """
        delete ... Function deletes an existing document based on ObjectId. It expects objectId as
        a string as argument.
        """
        filter = {"_id": ObjectId(objectId)}
        response = self.collection.delete_one(filter)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
