try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def menu():
    while True:

        print("********************************")
        print("")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("")
        print("********************************")
        print("")
        action = input("Choose from one of the above: ")

        try:
            action = int(action)
        except:
            os.system('clear')
            print("Input could not be casted to integer. Please enter digit")
            continue

        # If input integer:

        if action == 1:
            register()
            return

        elif action == 2:
            login()
            return

        elif action == 3:
            print("Exiting...")
            return

        else:
            os.system('clear')
            print("Input not available! Try again")
            continue


def connectDatabase(port, startTime):
    os.system('clear')
    try:
        client = MongoClient(port=port)

        print("Successfully connected to server on port: " + str(port))

        menu()

        return

    except:
        print("Connection failed")


if __name__ == "__main__":
    try:
        if len(sys.argv[1]) == 5:
            startTime = time.time()
            port = int(sys.argv[1])
            connectDatabase(port, startTime)

        else:
            exit(0)

    except:
        print("Invalid command, try the following format: ")
        print("python Phase2/phase2.py <port no.> if working from root project directory")
