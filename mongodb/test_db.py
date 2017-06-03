from pymongo import MongoClient
client = MongoClient()

print("Printing mongodb configurations...\n")
print("Databases:\n%s\n" %client.database_names())
print("Collections under khdb:\n%s\n" %client.get_database("khdb").collection_names())


