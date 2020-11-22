try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient

except ImportError as args:
    print("Import Error:", args)
    exit(1)

DATABASE_NAME = "291db"
COLLECTION_NAMES = {
    "tags": "Tags.json",
    "posts": "Posts.json",
    "votes": "Votes.json"
}


def populateColl(db, collectionName, jsonFile):
    collection = db[collectionName]
    with open(jsonFile) as f:
        data = json.load(f)[collectionName]["row"]
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    return collection


def resetDB(client):
    print("Resetting " + DATABASE_NAME + " database...")
    startTime = time.time()

    db = client[DATABASE_NAME]

    collections = ['posts', 'tags', 'votes']
    files = ['Posts.json', 'Tags.json', 'Votes.json']

    for i in range(3):
        populateColl(db, collections[i], files[i])

    timeTaken = time.time() - startTime
    print("Sucessfully reset (" + str(timeTaken) + " seconds)")


def connectDatabase(port):
    os.system('clear')
    try:
        client = MongoClient(port=port)
        if DATABASE_NAME in client.list_database_names():
            client.drop_database(DATABASE_NAME)
        resetDB(client)
    except:
        print("Connection failed, try again")


if __name__ == "__main__":
    try:
        if len(sys.argv[1]) == 5:
            port = int(sys.argv[1])
            connectDatabase(port)

        else:
            exit(0)

    except:
        print("Invalid port number. Try starting phase 1 with the following format: ")
        print("python phase1.py <port no.>")
