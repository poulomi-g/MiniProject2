try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from datetime import datetime

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def generateTags(tags):

    tagsList = tags.split()

    openBracket = '<'
    closeBracket = '>'

    editedTags = [openBracket + sub + closeBracket for sub in tagsList]

    result = ''

    for i in editedTags:
        result += i

    return result


def generatePostID(db):

    allPosts = db['posts']

    maxPost = allPosts.aggregate([
        {"$group": {"_id": None, "postid": {"$max": {"$toInt": "$Id"}}}}
    ])

    result = 0
    for i in maxPost:
        result = i['postid']

    return int(result) + 1


def updateTags(tags, db):

    # Check if tag exists in tags collections

    allTags = db['tags']

    for i in tags:
        matching_tag = allTags.find_one({"TagName": i})

        if not matching_tag:
            # No matches found

            tagID = generateTagID(db)
            newTag = {
                "Id": tagID,
                "TagName": i,
                "Count": 1
            }

            allTags.insert_one(newTag)
            # print("Tag added")

        else:
            allTags.update({"TagName": i}, {"$inc": {"Count": 1}})


def generateTagID(db):

    allTags = db['tags']

    maxTag = allTags.aggregate([
        {"$group": {"_id": None, "tagid": {"$max": {"$toInt": "$Id"}}}}
    ])

    result = 0
    for i in maxTag:
        result = i['tagid']

    return int(result) + 1


def postQuestion(db, user):
    os.system('clear')

    while True:
        print("ADD A QUESTION")
        print('-----------------------------------------')
        title = input("Title: ")
        if not title:
            os.system('clear')
            print('Title cannot be empty!')
            continue
        body = input("Body: ")
        if not body:
            os.system('clear')
            print('Title cannot be empty!')
            continue
        tags = input("Tags (Separated by space): ")
        formattedTags = generateTags(tags)
        crdate = str(datetime.now().date())
        pid = str(generatePostID(db))
        if user:
            poster = user
        os.system('clear')

        print("THE FOLLOWING QUESTION WILL BE ADDED: ")
        print('-----------------------------------------')
        print("Title: " + title)
        print("Body: " + body)
        print("Tags: " + formattedTags)
        print("Post ID: " + pid)
        print("Date: " + crdate)
        print('-----------------------------------------')
        confirmation = input("Confirm? y/n: ")

        if confirmation == 'n':
            return False

        elif confirmation == 'y':
            if not user:
                postDict = {
                    "Id": pid,
                    "PostTypeId": "1",
                    "CreationDate": crdate,
                    "Score": 0,
                    "ViewCount": 0,
                    "Body": body,
                    "Title": title,
                    "AnswerCount": 0,
                    "CommentCount": 0,
                    "ContentLicense": "CC BY-SA 2.5"
                }

            else:
                postDict = {
                    "Id": pid,
                    "PostTypeId": "1",
                    "CreationDate": crdate,
                    "Score": 0,
                    "ViewCount": 0,
                    "Body": body,
                    "OwnerUserId": user,
                    "Title": title,
                    "AnswerCount": 0,
                    "CommentCount": 0,
                    "ContentLicense": "CC BY-SA 2.5"
                }

            if formattedTags != '':
                postDict['Tags'] = formattedTags

                updateTags(tags.split(), db)

            allPosts = db['posts']

            allPosts.insert_one(postDict)

            return True

        else:
            os.system('clear')
            print("Invalid entry")
            return False

    return
