# -*- coding: utf-8 -*-
from mongodb.models import *
import json


def reset_database():
    Patient.objects.filter().delete()
    Disease.objects.filter().delete()
    Ingredient.objects.filter().delete()
    Nutrient.objects.filter().delete()


# def initialize_database():
#     with open("json/patients.json") as patient_data:
#         patients = json.load(patient_data)
#         for patient in patients.all():
#             patient.급성알레르기음식 = convert_list_2_tuple(patient.급성알레르기음식)
#             patient.만성알레르기음식 = convert_list_2_tuple(patient.만성알레르기음식)
#             patient.만성lgG4과민반응음식 = convert_list_2_tuple(patient.만성lgG4과민반응음식)
#             patients_collection.insert_one(patient)
#
#     with open("json/diseases.json") as diseases_data:
#         diseases = json.load(diseases_data)
#         for disease in diseases:
#             disease.질병식품관계 = convert_list_2_tuple(disease.질병식품관계)
#             disease.질병영양소관계 = convert_list_2_tuple(disease.질병영양소관계)
#             diseases_collection.insert_one(disease)
#
#     with open("json/ingredients.json") as ingredients_data:
#         ingredients = json.load(ingredients_data)
#         for ingredient in ingredients:
#             ingredient.식품영양소관계 = convert_list_2_tuple(ingredient.식품영양소관계)
#             ingredients_collection.insert_one(ingredient)
#
#     with open("json/nutrients.json") as nutrients_data:
#         nutrients = json.load(nutrients_data)
#         for nutrient in nutrients:
#             nutrients_collection.insert_one(nutrient)


def update_patient_basic_info(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding):
    patient = Patient.objects.get(ID=id)
    patient.ID = id
    patient.이름 = name
    patient.성별 = sex
    patient.생년월일 = birthdate
    patient.주소 = address
    patient.키 = height
    patient.몸무게 = weight
    patient.임신여부 = isPreg
    patient.수유여부 = isBFeeding
    patient.save()


def update_patient_detail_second_page(id, diagDiseasesStr, ingredients_gs, ingredients_ms, ingredients_lgg4):
    patient = Patient.objects(ID=id)
    tempName = patient.이름
    tempSex = patient.성별
    tempBirthdate = patient.생년월일
    tempAddress = patient.주소
    tempHeight = patient.키
    tempWeight = patient.몸무게
    tempIsPreg = patient.임신여부
    tempIsBFeeding = patient.수유여부
    tempOfficeVisitDateList = patient.진료일

    return patient.update(
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
                # "진단명": diagDiseasesStr,
                # "급성알레르기음식": ingredients_gs,
                # "만성알레르기음식": ingredients_ms,
                # "만성lgG4과민반응음식": ingredients_lgg4
            }
        }
    )


#####################
# Diseases Related  #
#####################


#######################
# Ingredients Related #
#######################
def get_ingredients_guepsung():
    return Ingredient.objects(급성알레르기가능여부 = True)


def get_ingredients_mansung():
    return Ingredient.objects(만성알레르기가능여부 = True)


def get_ingredients_mansung_lgg4():
    return Ingredient.objects(만성lgG4과민반응가능여부 = True)


#####################
# Nutrients Related #
#####################


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
