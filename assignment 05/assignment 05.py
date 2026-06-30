import pymongo
from datetime import datetime

client = pymongo.MongoClient("localhost", 27017)

db = client['qasim_db']

books_collect = db['books']


books_collect.insert_many(
    [
        { "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "price": 49.99, "genre": "Technology", "publishedAt": datetime(2019, 9, 13), "inStock": True },
        { "title": "Clean Code", "author": "Robert C. Martin", "price": 39.99, "genre": "Technology", "publishedAt": datetime(2008, 8, 1), "inStock": True },
        { "title": "Dune", "author": "Frank Herbert", "price": 14.99, "genre": "Sci-Fi", "publishedAt": datetime(1965, 8, 1), "inStock": False },
        { "title": "1984", "author": "George Orwell", "price": 12.99, "genre": "Dystopian", "publishedAt": datetime(1949, 6, 8), "inStock": True },
        { "title": "Atomic Habits", "author": "James Clear", "price": 27.99, "genre": "Self-Help", "publishedAt": datetime(2018, 10, 16), "inStock": True },
        { "title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 15.99, "genre": "Fantasy", "publishedAt": datetime(1937, 9, 21), "inStock": True },
        { "title": "Deep Work", "author": "Cal Newport", "price": 22.99, "genre": "Self-Help", "publishedAt": datetime(2016, 1, 5), "inStock": False },
        { "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "price": 59.99, "genre": "Technology", "publishedAt": datetime(2017, 3, 16), "inStock": True },
        { "title": "The Alchemist", "author": "Paulo Coelho", "price": 11.99, "genre": "Fiction", "publishedAt": datetime(1988, 1, 1), "inStock": True },
        { "title": "Sapiens", "author": "Yuval Noah Harari", "price": 18.99, "genre": "History", "publishedAt": datetime(2011, 1, 1), "inStock": False }
    ]
)



for book in books_collect.find():
  print(f'{book['title']} by {book['author']} — $ {book['price']}')



for book in books_collect.find({'author': 'James Clear'}, {'author' : 1, 'price': 1, '_id': 0}):
  print(book)



# $gt — books priced greater than $20
books_gt = books_collect.find({ 'price': { '$gt': 20 } })

# $in — books in specific genres
books_genre = books_collect.find(
    {
        "genre": {
            "$in": [
                "Technology", 
                "Self-Help"
            ]
        }
    }
)


# $and — technology books that are in stock
books_and = books_collect.find(
    {
        "$and": [
            {"genre": "Technology"},
            {"inStock": True}
        ]
    }
)

# $regex — books whose title contains "the" (case-insensitive)
books_case = books_collect.find(
    {
        "title": {
            "$regex": "the",
            "$options": "i"
        }
    }
)

for query in [books_gt, books_genre, books_and, books_case]:
    for book in query:
        print(book)



books_collect.update_one(
    { "title": "The Lean Startup" },
    {
        "$set": {
            "title": "The Lean Startup",
            "author": "Eric Ries",
            "price": 29.99,
            "genre": "Business",
            "inStock": True,
            "publishedAt": datetime(2011, 9, 13)
        }
    },
    upsert=True
)

for book in books_collect.find({
  "publishedAt": { "$gt": datetime(2000, 1, 1)}
}):
    print(book)