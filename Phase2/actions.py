try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from question import postQuestion
    from search import searchQuestion

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def actionsMenu(db, user):

    while True:
        print("ACTIONS")
        print('-----------------------------------------')
        print("")
        print("1. Post a question")
        print("2. Search for questions")
        print("3. Go Back")
        print("")
        print('-----------------------------------------')
        print("")
        action = input("Choose from one of the above: ")

        if int(action) == 1:
            result = postQuestion(db, user)

            if not result:
                print('Question not posted')

            else:
                print('Question posted!')
            continue

        if int(action) == 3:
            break

        if int(action) == 2:
            result = searchQuestion(db, user)

            continue
