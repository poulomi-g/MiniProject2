try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def userReport(db, user):
    os.system('clear')
    print("User report for: " + str(user))

    allPosts = db['posts']

    user = str(user)

    question_stats = allPosts.aggregate([
        {"$match": {"$and": [{"PostTypeId": "1"}, {"OwnerUserId": user}]}},
        {"$group": {"_id": "$OwnerUserId", "count": {
            "$sum": 1}, "avg": {"$avg": "$Score"}}}
    ])

    for i in question_stats:
        print('************************************')
        print("Number of questions: " + str(i['count']))
        print("Average votes: " + str(i['avg']))
        print('************************************')

    return
