#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from typing import Generator, Dict


# Connect to MongoDB
client = MongoClient()
db = client['zhaw_matchmaking']
profile_data_collection = db['profile_data']
persons_collection = db["persons"]

# Define the MongoDB aggregation pipeline
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


def generate_profiles() -> Generator[Dict, None, None]:
    """
    Generate profiles by aggregating data from 'profile_data_collection' and
    'persons_collection'.

    Yields:
        Dict: A profile with raw data, shorthand symbol, and name.
    """
    for profile in profile_data_collection.aggregate(pipeline):
        yield profile
