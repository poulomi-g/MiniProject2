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

        if not body:
            os.system('clear')
            print("Body cannot be empty!")
            continue

        crdate = str(datetime.now().date())
        apid = str(generatePostID(db))
        os.system('clear')

        print("THE FOLLOWING QUESTION WILL BE ADDED: ")
        print('-----------------------------------------')
        if user:
            poster = user
            print("User: " + poster)
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


def displayAnswer(db, matches, questionPost):
    # Separately print the accepted answer first and store its id:
    allPosts = db['posts']
    try:
        for j in questionPost:
            acceptedAnswerId = j['AcceptedAnswerId']

        allPosts = db['posts']
        acceptedAnswer = allPosts.find({"Id": str(acceptedAnswerId)})

        for i in acceptedAnswer:
            print("* ACCEPTED ANSWER")
            print('-----------------------------------------')
            print('Id: ' + str(i['Id']))
            if len(str(i['Body'])) < 80:
                print('Body: ' + str(i['Body']))
            else:
                print('Body: ' + str(i['Body'])[:80])
            print('Creation date: ' + str(i['CreationDate']))
            print('Score: ' + str(i['Score']))

    except:
        print("NO ACCEPTED ANSWERS YET")
        AcceptedAnswerId = None

    # Post the rest
    for i in matches:

        if str(i['Id']) != str(AcceptedAnswerId):
            print('-----------------------------------------')
            print('Id: ' + str(i['Id']))
            if len(str(i['Body'])) < 80:
                print('Body: ' + str(i['Body']))
            else:
                print('Body: ' + str(i['Body'])[:80])
            print('Creation date: ' + str(i['CreationDate']))
            print('Score: ' + str(i['Score']))
    print('-----------------------------------------')
    print("End of results")
    return


def listAnswers(db, pid, user):
    print("Listing answers for: " + str(pid))
    print('-----------------------------------------')

    allPosts = db['posts']

    matchingAnswers = allPosts.find({"ParentId": pid})
    questionPost = allPosts.find({"Id": pid})

    displayAnswer(db, list(matchingAnswers), list(questionPost))

    action = input(
        'Enter answer id you want to vote (Press enter to return to menu: ')

    if action == '':
        return False

    elif not action.isdigit():
        os.system('clear')
        print("Answer id must be an integer")
        return False

    else:
        result = voteAnswer(db, user, action)

        allPosts.update({"Id": str(action)}, {"$inc": {"ViewCount": 1}})

        if not result:
            os.system('clear')
            print("Vote didnt go through")

        else:
            os.system('clear')
            print("Vote successful")

    return
