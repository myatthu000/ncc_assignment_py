from pymongo import MongoClient


# Connect to MongoDB
def connect_to_mongodb(connect_str):
    try:
        # Replace 'mongodb://localhost:27017/' with your MongoDB connection string
        client = MongoClient(connect_str)
        # print("Database connection success ..... ")
        return client
    except Exception as e:
        print("Error connecting to MongoDB:", str(e))


# Create a new document in a collection
def create_document(client, db_name, collection_name, document):
    try:
        db = client[db_name]
        collection = db[collection_name]
        result = collection.insert_one(document)
        print("Document created with ID:", result.inserted_id)
    except Exception as e:
        print("Error creating document:", str(e))


# Read documents from a collection
def read_documents(client, db_name, collection_name, filter_cols):
    data = {}
    try:
        db = client[db_name]
        collection = db[collection_name]
        documents = collection.find({},filter_cols)
        for document in documents:
            id = len(data)
            data.update({id:document})
            # print(document)
        return data
    except Exception as e:
        print("Error reading documents:", str(e))


# Update a document in a collection
def update_document(client, db_name, collection_name, filter_query, update_query):
    try:
        db = client[db_name]
        collection = db[collection_name]
        result = collection.update_one(filter_query, update_query)
        print("Matched documents:", result.matched_count)
        print("Modified documents:", result.modified_count)
    except Exception as e:
        print("Error updating document:", str(e))


# Delete documents from a collection
def delete_documents(client, db_name, collection_name, filter_query):
    try:
        db = client[db_name]
        collection = db[collection_name]
        result = collection.delete_many(filter_query)
        print("Deleted documents count:", result.deleted_count)
    except Exception as e:
        print("Error deleting documents:", str(e))


# Usage
# connection_string = 'mongodb://localhost:27017/'
# client = connect_to_mongodb(connection_string)

# Create a document
# db_name = 'ncc_dip22'
# collection_products_auction = 'products_auction'
# collection_observer_info = 'observer_info'
# collection_user_info = 'user_info'
# document = {'name': 'John Doe', 'age': 30}
# create_document(client, db_name, collection_name, document)

# Read documents
# rr = read_documents(client, db_name, collection_observer_info, {"_id":0})
# print('rr' ,rr)

# # Update a document
# filter_query = {'name': 'John Doe'}
# update_query = {'$set': {'age': 35}}
# update_document(client, db_name, collection_name, filter_query, update_query)

# Delete documents
# delete_query = {'name': 'John Doe'}
# delete_documents(client, db_name, collection_name, delete_query)

# Close the MongoDB connection
# client.close()
