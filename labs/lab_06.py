import pymongo
from datetime import datetime
import insert_aggregation_sample_data as iasd

mongodb_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongodb_url)

db_name = "agg_test_db"
db = client[db_name]

# books_collect = db['books']

def print_cursor(cursor):
    for document in cursor:
        print(document, end="\n\n")

# .aggregate with $match and .find() generate cursor
match_cursor = db.products.aggregate([
    {"$match": {"name": "Pens"}}
])

# print_cursor(match_cursor)

# .aggregate with $match and .find() generate cursor
match_cursor = db.products.aggregate([
    {"$match": 
     {"$or": [
         {
             "tags": "Home"
         },
         {
             "tags": 'Beauty'
         }
         
     ]}
    }
])

# print_cursor(match_cursor)

# projection and aliasing
projection_cursor = db.products.aggregate([
    {
        "$project": {"_id": 0, "product_name":"$name", "seller_id": 1}
    }
])

# print_cursor(projection_cursor)
# projection and alias for tag (array) 0'th element
# use of arrayElemAt and first
# unset

proj_alias_cursor = db.products.aggregate([
    {"$match": 
     {"$or": [
         {
             "tags": "Home"
         },
         {
             "tags": 'Beauty'
         }
         
     ]}
    },
    {
        "$project": {
            "_id": 0, 
            "product_name" : "$name",
            "seller_id": 1,
            "num_tags": {"$size": "$tags"},
            "first_tag": {"$arrayElemAt": ["$tags", 0]},
            "first": {"$first": "$tags"}}
    },
    {
        "$unset": "first"
    },
    {
        "$limit": 3
    }
])

print_cursor(proj_alias_cursor)

