# -*- coding: utf-8 -*-
from utils import *
from pymongo import MongoClient
from pprint import pprint
import datetime

ID = "kihoproject"
PW = "!kiho1234"
CLUSTER_URL = "mongodb://"+ ID + ":" + PW + "@cluster0-shard-00-00-gugln.mongodb.net:27017,cluster0-shard-00-01-gugln.mongodb.net:27017,cluster0-shard-00-02-gugln.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
#client = MongoClient(CLUSTER_URL)
client = MongoClient()

print("\nPrinting mongodb configurations...\n")
print("Databases:\n\n%s\n" % client.database_names())
print("Collections under khdb:\n\n%s\n" % client.get_database("khdb").collection_names())

khdb = client.get_database("khdb")
patients = khdb.get_collection("Patient")
diseases = khdb.get_collection("diseases")
ingredients = khdb.get_collection("ingredients")
nutrients = khdb.get_collection("nutrients")

print("There are %d many patients data" % patients.count())
print("There are %d many diseases data" % diseases.count())
print("There are %d many ingredients data" % ingredients.count())
print("There are %d many nutrients data\n\n" % nutrients.count())


def print_all_patients():
    for patient in patients.find():
        pprint(patient)

def print_all_diseases():
    for disease in diseases.all():
        pprint(disease)

def print_all_ingredients():
    for ingredient in ingredients.all():
        pprint(ingredient)

def print_all_nutrients():
    for nutrient in nutrients.all():
        pprint(nutrient)


def add_dummy_patient():
    Patient(ID="ID_1", 이름="상현", 성별="남", 생년월일=datetime.datetime.utcnow()).save()
    Patient(ID="ID_2", 이름="지영", 성별="여", 생년월일=datetime.datetime.utcnow()).save()

#print_all_patients()
#print_all_diseases()
#print_all_ingredients()

#reset_database()
#initialize_database()
