import pymongo

class CheckLatestDraw:
    #Initialise the database
    def check_draws():
        try:
            connection = pymongo.MongoClient(
                "localhost",
                27017
            )
            print("Connected Successfully")
        except:
            print("Could not connect to MongoDB:")
        db = connection.sgtoto
        collection = db.toto_draws

        valid = True
        last_stored_draw = collection.find_one()
        latest_stored_draw = last_stored_draw['latestdraw']
        return latest_stored_draw

print (CheckLatestDraw.check_draws())
