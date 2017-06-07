# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint
from utils import *

ID = "kihoproject"
PW = "!kiho1234"
CLUSTER_URL = "mongodb://"+ ID + ":" + PW + "@cluster0-shard-00-00-gugln.mongodb.net:27017,cluster0-shard-00-01-gugln.mongodb.net:27017,cluster0-shard-00-02-gugln.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
client = MongoClient(CLUSTER_URL)

print("\nPrinting mongodb configurations...\n")
print("Databases:\n\n%s\n" % client.database_names())
print("Collections under khdb:\n\n%s\n" % client.get_database("khdb").collection_names())

khdb = client.khdb
patients = khdb.patients
diseases = khdb.diseases
ingredients = khdb.ingredients
nutrients = khdb.nutrients

print("There are %d many patients data" % patients.count())
print("There are %d many diseases data" % diseases.count())
print("There are %d many ingredients data" % ingredients.count())
print("There are %d many nutrients data\n\n" % nutrients.count())

#gs_ingred = get_ingredients_guepsung()
#print("There are %d many ingredients data for guepsung allergy\n" % gs_ingred.count())


def print_all_patients():
    for patient in patients.find():
        pprint(patient)

def print_all_diseases():
    for disease in diseases.find():
        pprint(disease)

def print_all_ingredients():
    for ingredient in ingredients.find():
        pprint(ingredient)

def print_all_nutrients():
    for nutrient in nutrients.find():
        pprint(nutrient)

#print_all_patients()
#print_all_diseases()
#print_all_ingredients()

#reset_database()
#initialize_database()