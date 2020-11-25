try:
    import json
    import sys
    import time
    import os
    from pymongo import MongoClient
    from question import generatePostID
    from datetime import datetime

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def generateVoteId(db):

    allVotes = db['votes']

    maxVote = allVotes.aggregate([
        {"$group": {"_id": None, "voteid": {"$max": {"$toInt": "$Id"}}}}
    ])

    result = 0
    for i in maxVote:
        result = i['voteid']

    return int(result) + 1


def voteAnswer(db, user, pid):

    # Check if post exists:

    allPosts = db['posts']

    matchingPost = allPosts.find_one({"Id": str(pid)})

    if not matchingPost:
        os.system('clear')
        print("Post does not exist!")
        return False

    else:
        # Post exists, check if user has already voted

        if not user:
            newVoteId = generateVoteId(db)

            # Update score of post
            allPosts.update({"Id": str(pid)}, {"$inc": {"Score": 1}})

            # Add the vote dictionary to the votes collection

            # Create dictionary first:

            crdate = str(datetime.now().date())
            voteDict = {
                "Id": str(newVoteId),
                "PostId": str(pid),
                "VoteTypeId": "2",
                "CreationDate": crdate
            }

            # Insert into votes
            allVotes = db['votes']
            allVotes.insert_one(voteDict)

            return True

        else:
            # User is not anon

            # Check if user has casted vote on given post already:

            allVotes = db['votes']

            matchingVote = allVotes.find({"$and": [
                {'UserId': str(user)},
                {'PostId': str(pid)}
            ]
            })

            if not list(matchingVote):
                # User has not voted on this post yet
                # Make vote dict with username field:

                allPosts.update({"Id": str(pid)}, {"$inc": {"Score": 1}})

                newVoteId = generateVoteId(db)

                crdate = str(datetime.now().date())
                voteDict = {
                    "Id": str(newVoteId),
                    "PostId": str(pid),
                    "VoteTypeId": "2",
                    "UserId": str(user),
                    "CreationDate": crdate
                }

                # Insert into votes
                allVotes.insert_one(voteDict)

                return True

            else:
                os.system('clear')
                return False
