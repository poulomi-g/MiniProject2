try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def findQuestion(db, keywords):

    allPosts = db['posts']

    stringofkeywords = ' '.join(keywords)

    # TODO: Remember to index in phase 1
    # TODO: display in a nice way
    matches = allPosts.find({"$text": {"$search": stringofkeywords}})

    print(list(matches))
    return matches


def searchQuestion(db, user):
    os.system('clear')
    while True:
        print("SEARCH")
        print('-----------------------------------------')
        keywords = input(
            "Enter keywords to search question posts with, separated by spaces: ")

        if keywords == '':
            os.system('clear')
            print("Keywords cannot be empty")
            continue

        else:
            # Conversion to set removes duplicates
            split_keywords = list(set(keywords.lower().split()))

            matches = findQuestion(db, split_keywords)

    return True
