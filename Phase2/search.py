try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from answer import addAnswer, listAnswers
    from vote import voteAnswer

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def questionActionMenu(db, user, pid):

    print('-----------------------------------------')
    print('Question actions for post no.: ' + pid)
    allPosts = db['posts']

    matches = allPosts.find({"Id": str(pid)})

    # Update view count
    allPosts.update({"Id": str(pid)}, {"$inc": {"ViewCount": 1}})

    for i in list(matches):
        print('-----------------------------------------')
        print('_id: ' + str(i['_id']))
        print('id: ' + str(i['Id']))
        print('Post Type ID: ' + str(i['PostTypeId']))
        print('View Count: ' + str(i['ViewCount']) + ' (New)')
        print('Comment Count: ' + str(i['CommentCount']))
        print()
        print('Title: ' + str(i['Title']))
        print('Body: ' + str(i['Body']))
        print('Tags: ' + str(i['Tags']))
        print('Creation date: ' + str(i['CreationDate']))
        print('Score: ' + str(i['Score']))
        print('Answer Count: ' + str(i['AnswerCount']))
        print('Content License: ' + str(i['ContentLicense']))
        print('-----------------------------------------')

    print('1. Answer')
    print('2. List answers')
    print('3. Vote this question')
    print('4. Back')

    action = input("Choose from one of the above: ")

    if int(action) == 1:
        os.system('clear')
        result = addAnswer(db, pid, user)

        if result:
            os.system('clear')
            print("Answer added!")

            return

        else:
            print("Answer not added")
            return

    elif int(action) == 2:
        os.system('clear')
        result = listAnswers(db, pid, user)
        return

    elif int(action) == 3:
        result = voteAnswer(db, user, pid)

        if result:
            os.system('clear')
            print('Question voted!')
            return

        else:
            os.system('clear')
            print('Vote did not go through')
            return

    elif int(action) == 4:
        return

    else:
        os.system('clear')
        print("Invalid entry")
        return


def displayQuestion(matches):
    for i in matches:
        if i['PostTypeId'] == "1":
            print('-----------------------------------------')
            print('Id: ' + str(i['Id']))
            print('Title: ' + str(i['Title']))
            print('Body: ' + str(i['Body']))
            print('Creation date: ' + str(i['CreationDate']))
            print('Score: ' + str(i['Score']))
            print('Answer Count: ' + str(i['AnswerCount']))

    print('-----------------------------------------')
    print("End of results")
    return


def findQuestion(db, keywords):

    allPosts = db['posts']

    stringofkeywords = ' '.join(keywords)

    # TODO: Remember to index in phase 1
    matches = allPosts.find({"$text": {"$search": stringofkeywords}})

    displayQuestion(list(matches))
    return


def searchActionSelector(db, user):
    print('-----------------------------------------')
    action = input(
        "Choose a post by entering its id (Press enter to go back): ")

    # TODO: Error checking

    if action == '':
        os.system('clear')
        print("Results cleared")
        return

    if not action.isdigit():
        os.system('clear')
        print("Post id must be an integer")
        return

    allPosts = db['posts']

    pid = action

    # Check if post exists:
    try:
        matchingPost = allPosts.find_one({"Id": str(pid)})
    except:
        os.system('clear')
        print("no such post!")
        return

    else:
        if matchingPost['PostTypeId'] == "1":
            os.system('clear')
            questionActionMenu(db, user, str(pid))
            return

        else:
            os.system('clear')
            print('Selected post is an answer: ')
            allPosts.update({"Id": str(pid)}, {"$inc": {"ViewCount": 1}})
            print('View count updated')

            # TODO: Display answer nicely

            print('-----------------------------------------')
            print('Id: ' + str(matchingPost['Id']))
            print('Body: ' + str(matchingPost['Body']))
            print('Creation date: ' + str(matchingPost['CreationDate']))
            print('ViewCount: ' + str(matchingPost['ViewCount']))
            print('Score: ' + str(matchingPost['Score']))

            try:
                print('User: ' + str(matchingPost['OwnerUserId']))

            except:
                print("User: None")

            action = input("Do you wish to vote this answer? [y/n]: ")

            if action == 'n':
                return

            elif action == 'y':
                result = voteAnswer(db, user, str(pid))

                if result:
                    os.system('clear')
                    print("Voted")
                    return

                else:
                    os.system('clear')
                    print('Vote did not go through')
                    return

            else:
                os.system('clear')
                print("Not a valid response")
                return

    return


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

            findQuestion(db, split_keywords)

            searchActionSelector(db, user)

            break

    return True
