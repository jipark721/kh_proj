from pymongo import MongoClient
from pprint import pprint

client = MongoClient()

print("Printing mongodb configurations...\n")
print("Databases:\n%s\n" %client.database_names())
print("Collections under khdb:\n%s\n" %client.get_database("khdb").collection_names())

khdb = client.get_database("khdb")

patients = khdb.get_collection("patients")

for patient in patients.find():
    pprint(patient)