try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from question import generatePostID
    from datetime import datetime
    from vote import voteAnswer

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def addAnswer(db, pid, user):

    while True:
        print("ADD AN ANSWER TO POST " + pid)
        print('-----------------------------------------')
        body = input("Body: ")
        crdate = str(datetime.now().date())
        apid = str(generatePostID(db))
        if user:
            poster = user
        os.system('clear')

        print("THE FOLLOWING QUESTION WILL BE ADDED: ")
        print('-----------------------------------------')
        print("Body: " + body)
        print("Post ID: " + apid)
        print("Date: " + crdate)
        print('-----------------------------------------')
        confirmation = input("Confirm? y/n: ")

        if confirmation == 'n':
            return False

        if not user:
            postDict = {
                "Id": apid,
                "PostTypeId": "2",
                "CreationDate": crdate,
                "Score": 0,
                "ViewCount": 0,
                "Body": body,
                "ParentId": pid,
                "CommentCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }

        else:
            postDict = {
                "Id": apid,
                "PostTypeId": "2",
                "CreationDate": crdate,
                "Score": 0,
                "ViewCount": 0,
                "Body": body,
                "OwnerUserId": user,
                "ParentId": pid,
                "CommentCount": 0,
                "ContentLicense": "CC BY-SA 2.5"
            }

        allPosts = db['posts']

        allPosts.insert_one(postDict)

        allPosts.update({"Id": str(pid)}, {"$inc": {"AnswerCount": 1}})

        return True

    return


def listAnswers(db, pid, user):
    print("Listing answers for: " + str(pid))
    print('-----------------------------------------')

    allPosts = db['posts']

    matchingAnswers = allPosts.find({"ParentId": pid})

    print(list(matchingAnswers))

    # TODO display answers properly
    # TODO limit initial display to 80 characters

    action = input(
        'Enter answer you want to vote (Press enter to return to menu: ')

    if action == '':
        return False

    else:
        result = voteAnswer(db, user, action)

        allPosts.update({"Id": str(action)}, {"$inc": {"ViewCount": 1}})

        if not result:
            print("Vote didnt go through")

        else:
            print("Vote successful")

    return
