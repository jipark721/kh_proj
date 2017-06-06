# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint
from utils import *

reset_database()
initialize_database()

client = MongoClient()

print("Printing mongodb configurations...\n")
print("Databases:\n%s\n" % client.database_names())
print("Collections under khdb:\n%s\n" % client.get_database("khdb").collection_names())

client = MongoClient()
khdb = client.khdb
patients = khdb.patients
diseases = khdb.diseases
ingredients = khdb.ingredients
nutrients = khdb.nutrients

print("There are %d many patients data" % patients.count())
print("There are %d many diseases data" % diseases.count())
print("There are %d many ingredients data\n" % ingredients.count())


def print_all_patients():
    for patient in patients.find():
        pprint(patient["알레르기음식"])

def print_all_diseases():
    for disease in diseases.find():
        pprint(disease["질병명"])

def print_all_ingredients():
    for ingredient in ingredients.find():
        pprint(ingredient["식품명"])

def print_all_nutrients():
    for nutrient in nutrients.find():
        pprint(nutrient["영양소명"])

print_all_patients()