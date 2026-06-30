# from pymongo import MongoClient
import pymongo

client = pymongo.MongoClient("localhost", 27017)
# MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)

db_names = client.list_database_names()
print(db_names)

db = client['store']
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'store')
print(db)

user_collect = db['users']
print(user_collect)

'''
new_user = {
    "name": "Qasim",
    "age": 29
}

update_user = {
    "name": "Dinakar",
    "age": 40
}

user_collect.insert_one(new_user)
user_collect.insert_one(update_user)


user_qasim = user_collect.find_one({"name" : "Qasim"})
print(user_qasim)

# user_collect.update_one(new_user, {'$set': update_user})
user_collect.update_one(
    {"name": "Dinakar"},
    {"$set": {"name": "Tifano"}}
)
'''

prod_collect = db['products']


iphone_15 = {'name': 'iphone15',
    'price': 1299,
    'storage': 128
}
'''
iphone_15_pro = {'name': 'iphone15_pro',
    'price': 1899,
    'storage': 256
}

iphone_16 = {'name': 'iphone16',
    'price': 1399,
    'storage': 128
}
iphone_16_pro = {'name': 'iphone16_pro',
    'price': 1999,
    'storage': 256
}

iphone_17 = {'name': 'iphone16',
    'price': 1399,
    'storage': 128
}
iphone_17_pro = {'name': 'iphone17_pro',
    'price': 2099,
    'storage': 256
}
'''

# prod_collect.insert_one(iphone_15_pro)
list_collect = db.list_collection_names()

# list = [iphone_15, iphone_15_pro, iphone_16, iphone_16_pro, iphone_17, iphone_17_pro]

# prod_collect.insert_many(list)

i15_a = prod_collect.find_one({'name': 'iphone15'})
# print(i15_a)

# print(i15_a['storage'])

# cursor is exhaustible, but object is not exhaustible
# both cursor and objects are iterable but cursor can be iterated only once
# even in stored in a variable, it will still disappear
# result of the 'find' is the cursor

print('\nSorted values on the basis of price are:')
for doc in prod_collect.find().sort('price', -1):
    print(f'{doc}')

print('\n')
for doc in prod_collect.find().sort([('price', -1), ('name', 1)]):
    print(f'Multi-level sorted values are {doc}')

print('\nTop 3 prices are:')
for doc in prod_collect.find().sort('price', -1).limit(3):
    print(f'{doc}')

print('\n')
for doc in prod_collect.find().sort('price', -1).limit(3).skip(2).limit(1):
    print(f'3rd Highest Price is {doc}')


'''
iphone_cursor = prod_collect.find({'storage': 128})
print(iphone_cursor.alive)

for doc in iphone_cursor.sort("price", pymongo.DESCENDING):
    print(doc)
'''

count_storage_128 = prod_collect.count_documents({'storage': 128})
print(f'Number of documents where storage is 128 are {count_storage_128}')

print('\nDistinct Storage Values are:')
for doc in prod_collect.find().distinct('storage'):
    print(f'{doc}')

print('\nDisplaying only price of those items where storage is 128')
for doc in prod_collect.find({'storage': 128}, {'price': 1, '_id': 0}):
    print(doc)

print('\nDisplaying the items where storage is greater than 128 AND price not equal to 1000')
for doc in prod_collect.find({'storage': {'$gt': 128}, 'price' : {'$ne': '1000'}}):
    print(doc)

print('\nDisplaying the items where storage is greater than 128 OR price not equal to 1000')
query = {
    "$or": [
        {"storage": {"$gt": 128}},
        {"price": {"$ne": "1000"}}
    ]
}
for doc in prod_collect.find(query):
    print(doc)


print('\nDisplaying Records where storage is an integer:')
for doc in prod_collect.find({'storage': {'$type': 'int'}}):
    print(f'{doc}')

print('\nDisplaying Records where a certain attribute exists or not:')
for doc in prod_collect.find({'storage': {'$exists': True}}):
    print(f'{doc}')


print('\nDisplaying record whos name conatains iphone without case-sensitivity')
for doc in prod_collect.find({'name': {'$regex': 'Iphone', '$options': 'i'}}):
    print(f'{doc}')

prod_collect.update_one(iphone_15, {'$set': {'category': 'iphone'}}, upsert=True)