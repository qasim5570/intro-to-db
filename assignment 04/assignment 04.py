from pymongo import MongoClient

client = MongoClient("localhost", 27017)
# MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

db_names = client.list_database_names()
# print(db_names)

db = client['qasim_db']
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'store')
# print(db)

user_collect = db['qasim_collect']
# print(user_collect)


new_user = {
    "name": "Qasim",
    "age": 29
}

# print(user_collect.insert_one(new_user))

new_user = {
    "name": "Dinakar",
    "age": 40
}

# print(user_collect.insert_one(new_user))

update_user = {
    "name": "Sherzod",
    "age": 40
}

print(f'Updated User {user_collect.insert_one(update_user)} has been added also')


user_qasim = user_collect.find_one({"name" : "Qasim"})
print(user_qasim)


# user_collect.update_one(new_user, {'$set': update_user})
user_collect.update_one(
    {"name": "Dinakar"},
    {"$set": {"name": "Tifano"}}
)

user_collect.delete_one({"name": "Tifano"})