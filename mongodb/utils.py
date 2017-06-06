# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient()
khdb = client.get_database("khdb")
patients_collection = khdb.get_collection("patients")
diseases_collection = khdb.get_collection("diseases")
ingredients_collection = khdb.get_collection("ingredients")


def reset_database():
    khdb.drop_collection("patients")
    khdb.drop_collection("diseases")
    khdb.drop_collection("ingredients")

def initialize_database():
    with open("json/patients.json") as patient_data:
        patients = json.load(patient_data)
        for patient in patients:
            patient["알레르기음식"] = convert_list_2_tuple(patient["알레르기음식"])
            patients_collection.insert_one(patient)

    with open("json/diseases.json") as diseases_data:
        diseases = json.load(diseases_data)
        for disease in diseases:
            disease["질병식품관계"] = convert_list_2_tuple(disease["질병식품관계"])
            disease["질병영양소관계"] = convert_list_2_tuple(disease["질병영양소관계"])
            diseases_collection.insert_one(disease)

    with open("json/ingredients.json") as ingredients_data:
        ingredients = json.load(ingredients_data)
        for ingredient in ingredients:
            ingredient["식품영양소관계"] = convert_list_2_tuple(ingredient["식품영양소관계"])
            ingredients_collection.insert_one(ingredient)

def get_all_patients():
    return patients_collection.find()


def get_patient_by_name(name):
    return patients_collection.find({"성명": name})


def get_patient_by_id(id):
    return patients_collection.find({"ID": id})


def get_patient_by_name_and_birthdate(name, birthdate):
    return patients_collection.find(
        {"$and":
             [{"성명": name},
              {"생일": birthdate}]
         }
    )

def add_one_patient(patient):
    return patients_collection.insert_one(
        {
        #"Num": 1.0,
        "ID": patient['ID'],
        "이름": patient['이름'],
        "성별": patient['성별'],
        "생년월일": patient['생년월일'],
        "주소": patient['주소'],
        "진단명": patient['진단명'],
        "진료일": patient['진료일'],
        "방문횟수": patient['방문횟수'],
        "키": patient['키'],
        "몸무게": patient['몸무게'],
        "임신여부": patient['임신여부'],
        "수유여부": patient['수유여부'],
        "알레르기음식": patient["알레르기음식"]
        }
    )

# Convert list of entry-defined (val_1, val_2) objects to list of tuples
def convert_list_2_tuple(entry_list):
    if entry_list == "" or entry_list is None:
        return None
    entries = [entry.strip() for entry in entry_list.split(",")]
    return [convert_entry_2_tuple(tuple) for tuple in entries]

# (val_1:val_2) -> tup(val_1,val_2)
def convert_entry_2_tuple(entry):
    if entry == "" or entry is None:
        return None
    entry = entry.strip()[1:-1]
    name, value = entry.split(":")
    return tuple([name, int(value)])