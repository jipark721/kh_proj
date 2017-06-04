from pymongo import MongoClient
from pprint import pprint

client = MongoClient()

print("Printing mongodb configurations...\n")
print("Databases:\n%s\n" %client.database_names())
print("Collections under khdb:\n%s\n" %client.get_database("khdb").collection_names())

khdb = client.get_database("khdb")
patients = khdb.get_collection("patients")
diseases = khdb.get_collection("diseases")
ingredients = khdb.get_collection("ingredients")

print("There are %d many patients data" %patients.count())
print("There are %d many diseases data" %diseases.count())
print("There are %d many ingredients data\n" %ingredients.count())
