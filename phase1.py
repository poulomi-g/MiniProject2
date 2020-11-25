try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def populateColl(db, collectionName, jsonFile):

    try:
        collection = db[collectionName]
        with open(jsonFile) as f:
            data = json.load(f)[collectionName]["row"]
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
        return collection
    except:
        print("Error populating collections")


def LoadJSON(client):
    print("Loading...")
    startTime = time.time()

    db = client["291db"]

    collections = ['posts', 'tags', 'votes']
    files = ['Posts.json', 'Tags.json', 'Votes.json']

    for i in range(3):
        populateColl(db, collections[i], files[i])

    return db


def connectDatabase(port, startTime):
    os.system('clear')
    try:
        client = MongoClient(port=port)

        print("Dropping existing database if any...")
        if "291db" in client.list_database_names():
            client.drop_database("291db")

        db = LoadJSON(client)

        finalTime = time.time() - startTime
        print("Time taken to load JSON data: ")
        print(finalTime)

        print("Adding text indexing for search...")
        posts = db['posts']
        posts.create_index(
            [('Title', 'text'), ('Body', 'text'), ('Tags', 'text')])
        print("Done")
        finalfinaltime = time.time() - startTime
        print("Time taken in total: " + str(finalfinaltime))

    except:
        print("Error, database could not be remade. Hint: Make sure .json files are present in phase1.py directory")


if __name__ == "__main__":
    try:
        if len(sys.argv[1]) == 5:
            startTime = time.time()
            port = int(sys.argv[1])
            connectDatabase(port, startTime)

        else:
            exit(0)

    except:
        print("Invalid port number. Try starting phase 1 with the following format: ")
        print("python phase1.py <port no.>")
