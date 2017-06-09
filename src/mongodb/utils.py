# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint
import json

ID = "kihoproject"
PW = "!kiho1234"
CLUSTER_URL = "mongodb://" + ID + ":" + PW + "@cluster0-shard-00-00-gugln.mongodb.net:27017,cluster0-shard-00-01-gugln.mongodb.net:27017,cluster0-shard-00-02-gugln.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
# client = MongoClient(CLUSTER_URL)
client = MongoClient()

khdb = client.get_database("khdb")
patients_collection = khdb.get_collection("patients")
diseases_collection = khdb.get_collection("diseases")
ingredients_collection = khdb.get_collection("ingredients")
nutrients_collection = khdb.get_collection("nutrients")


def reset_database():
    khdb.drop_collection("patients")
    khdb.drop_collection("diseases")
    khdb.drop_collection("ingredients")
    khdb.drop_collection("nutrients")


def initialize_database():
    with open("json/patients.json") as patient_data:
        patients = json.load(patient_data)
        for patient in patients:
            patient["급성알레르기음식"] = convert_list_2_tuple(patient["급성알레르기음식"])
            patient["만성알레르기음식"] = convert_list_2_tuple(patient["만성알레르기음식"])
            patient["만성lgG4과민반응음식"] = convert_list_2_tuple(patient["만성lgG4과민반응음식"])
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

    with open("json/nutrients.json") as nutrients_data:
        nutrients = json.load(nutrients_data)
        for nutrient in nutrients:
            nutrients_collection.insert_one(nutrient)

def get_empty_patient_obj():
    return dict.fromkeys([field for field in patients_collection.find_one()])

def get_all_patients():
    return patients_collection.find()


def get_patients_by_name(name):
    return patients_collection.find({"이름": name})


def get_patient_by_id(id):
    return patients_collection.find_one({"ID": id})

def get_patients_by_name_and_birthdate(name, birthdate):
    return patients_collection.find(
        {"$and":
             [{"이름": name},
              {"생년월일": birthdate}]
         }
    )


def add_one_patient(patient):
    return patients_collection.insert_one(
        {
            # "Num": 1.0,
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
            "급성알레르기음식": patient["급성알레르기음식"],
            "만성알레르기음식": patient["만성알레르기음식"],
            "만성lgG4과민반응음식": patient["만성lgG4과민반응음식"]
        }
    )


def update_patient_detail_first_page(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding, officeVisitDateList):
    patient = get_patient_by_id(id)
    tempDiagDis = patient["진단명"]
    tempGSIng = patient["급성알레르기음식"]
    tempMSIng = patient["만성알레르기음식"]
    tempLGG4Ing = patient["만성lgG4과민반응음식"]
    return patients_collection.update(
        {"ID": id},
        {"$set":
             {
                 "ID": id,
                 "이름": name,
                "성별": sex,
                "생년월일": birthdate,
                "주소": address,
                "키": height,
                "몸무게": weight,
                "임신여부": isPreg,
                "수유여부": isBFeeding,
                "진료일": officeVisitDateList,
                 "진단명": tempDiagDis,
                 "급성알레르기음식": tempGSIng,
                 "만성알레르기음식": tempMSIng,
                 "만성lgG4과민반응음식": tempLGG4Ing
              }
        }
    )

def update_patient_detail_second_page(id, diagDiseasesStr, ingredients_gs, ingredients_ms, ingredients_lgg4):
    patient = get_patient_by_id(id)
    tempName = patient["이름"]
    tempSex = patient["성별"]
    tempBirthdate = patient["생년월일"]
    tempAddress = patient["주소"]
    tempHeight = patient["키"]
    tempWeight = patient["몸무게"]
    tempIsPreg = patient["임신여부"]
    tempIsBFeeding = patient["수유여부"]
    tempOfficeVisitDateList = patient["진료일"]

    return patients_collection.update(
        {"ID": id},
        {"$set":
             {
                 "ID": id,
                 "이름": tempName,
                 "성별": tempSex,
                 "생년월일": tempBirthdate,
                 "주소": tempAddress,
                 "키": tempHeight,
                 "몸무게": tempWeight,
                 "임신여부": tempIsPreg,
                 "수유여부": tempIsBFeeding,
                 "진료일": tempOfficeVisitDateList,
                "진단명": diagDiseasesStr,
                "급성알레르기음식": ingredients_gs,
                "만성알레르기음식": ingredients_ms,
                "만성lgG4과민반응음식": ingredients_lgg4
             }
        }
    )


#####################
# Diseases Related  #
#####################
def get_empty_disease_obj():
    return dict.fromkeys([field for field in diseases_collection.find_one()])


def get_all_diseases():
    return diseases_collection.find()


#######################
# Ingredients Related #
#######################
def get_empty_ingredient_obj():
    return dict.fromkeys([field for field in ingredients_collection.find_one()])


def get_all_ingredients():
    return ingredients_collection.find()


def get_ingredients_guepsung():
    return ingredients_collection.find({"급성알레르기가능여부": "y"})


def get_ingredients_mansung():
    return ingredients_collection.find({"만성알레르기가능여부": "y"})


def get_ingredients_mansung_lgg4():
    return ingredients_collection.find({"만성 lgG4 과민반응가능여부": "y"})


#####################
# Nutrients Related #
#####################
def get_empty_nutrient_obj():
    return dict.fromkeys([field for field in nutrients_collection.find_one()])

def get_all_nutrients():
    return nutrients_collection.find()


def get_nutrients_by_level(level):
    pass


#####################
# Helper functions  #
#####################
# Convert string "val_1, val_2" to [val_1, val_2]
def convert_string_2_list(str):
    if str == "" or str is None:
        return None
    return [entry.strip() for entry in str.split(",")]

def convert_string_2_set(str):
    if str == "" or str is None:
        return None
    s = set()
    for entry in str.split(','):
        s.add(entry.strip())
    return s

def convert_list_2_set(l):
    if len(l) == 0 or l is None:
        return None
    s = set()
    for entry in l:
        s.add(entry)
    return s

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
