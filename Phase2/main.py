try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from userReport import userReport
    from actions import actionsMenu

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def menu(db):
    while True:

        print('-----------------------------------------')
        print("")
        print("1. Continue with user id: ")
        print("2. Continue without user id: ")
        print("3. Exit")
        print("")
        print('-----------------------------------------')
        print("")
        action = input("Choose from one of the above: ")

        try:
            action = int(action)
        except:
            os.system('clear')
            print("Input could not be casted to integer. Please enter digit")
            continue

        # If input integer:

        if int(action) == 1:
            os.system('clear')
            user = input("Enter user id: ")
            userReport(db, user)

            actionsMenu(db, user)
            os.system('clear')
            continue

        elif int(action) == 2:
            actionsMenu(db, False)
            os.system('clear')
            continue

        elif int(action) == 3:
            print("Exiting...")
            break

        else:
            os.system('clear')
            print("Input not available! Try again")
            continue

    return True


def connectDatabase(port, startTime):
    os.system('clear')

    client = MongoClient(port=port)
    db = client['291db']

    print("Successfully connected to server on port: " + str(port))

    menu(db)

    print("Something went wrong, try again")


if __name__ == "__main__":

    if len(sys.argv[1]) == 5:
        startTime = time.time()
        port = int(sys.argv[1])
        connectDatabase(port, startTime)

    else:
        exit(0)

    print("Invalid command, try the following format: ")
    print("python Phase2/phase2.py <port no.> if working from root project directory")
