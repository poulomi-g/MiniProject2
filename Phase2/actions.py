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
                os.system('clear')
                print('Question not posted')

            else:
                os.system('clear')
                print('Question posted!')
            continue

        elif int(action) == 3:
            break

        elif int(action) == 2:
            result = searchQuestion(db, user)

            os.system('clear')

            continue

        else:
            os.system('clear')
            print("Invalid response")
            continue
