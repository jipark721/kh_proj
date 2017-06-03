from pymongo import MongoClient
client = MongoClient()

rest = client.test.restaurants

#for i in rest.find():
    #print(i['name'])

test1_db = client.test1.test_col

for i in test1_db.find():
    print(i)

test1_db.insert_one(
    {
        "name" : "alex",
        "age" : 100
    }
)