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
    allVotes = db['votes']

    user = str(user)

    question_stats = allPosts.aggregate([
        {"$match": {"$and": [{"PostTypeId": "1"}, {"OwnerUserId": user}]}},
        {"$group": {"_id": "$OwnerUserId", "count": {
            "$sum": 1}, "avg": {"$avg": "$Score"}}}
    ])

    answer_stats = allPosts.aggregate([
        {"$match": {"$and": [{"PostTypeId": "2"}, {"OwnerUserId": user}]}},
        {"$group": {"_id": "$OwnerUserId", "count": {
            "$sum": 1}, "avg": {"$avg": "$Score"}}}
    ])

    vote_stats = allVotes.aggregate([
        {"$match": {"UserId": user}},
        {"$group": {"_id": "$UserId", "count": {
            "$sum": 1}}}
    ])

    for i in question_stats:
        print('-----------------------------------------')
        print("Number of questions: " + str(i['count']))
        print("Average question votes: " + str(i['avg']))

    for i in answer_stats:
        print('')
        print("Number of answers: " + str(i['count']))
        print("Average answer votes: " + str(i['avg']))

    for i in vote_stats:
        print('')
        print("No. of votes casted of all types: " + str(i['count']))

    print('-----------------------------------------')

    return
