from pymongo import MongoClient

client = MongoClient()
db = client['zhaw_matchmaking']
profile_data_collection = db['profile_data']
persons_collection = db["persons"]

pipeline = [
    {
        "$lookup": {
            "from": "persons",
            "localField": "person_id",
            "foreignField": "_id",
            "as": "person_data"
        }
    },
    {
        "$unwind": "$person_data"
    },
    {
        "$project": {
            "raw_data": 1,
            "shorthandSymbol": "$person_data.shorthandSymbol",
            "name": "$person_data.name"
        }
    }
]


def generate_profiles():
    for profile in profile_data_collection.aggregate(pipeline):
        yield profile
