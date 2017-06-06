# -*- coding: utf-8 -*-

from pymongo import MongoClient
import json

client = MongoClient()
khdb = client.khdb
patients = khdb.patients
diseases = khdb.diseases
ingredients = khdb.ingredients


def reset_database():
    khdb.drop_collection("patients")
    khdb.drop_collection("diseases")
    khdb.drop_collection("ingredients")


def initialize_database_from_json():
    patients = json.load("json/patients")
    for patient in patients:
        print(patient)


def get_all_patients():
    return patients.find()


def get_patient_by_name(name):
    return patients.find({"성명": name})


def get_patient_by_id(id):
    return patients.find({"ID": id})


def get_patient_by_name_and_birthdate(name, birthdate):
    return patients.find(
        {"$and":
             [{"성명": name},
              {"생일": birthdate}]
         }
    )

def addOnePatient(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding, officeVisitDateList, diagDiseases):
    return patients.insert_one(
        {
            "ID": id,
            "성명": name,
            "성별": sex,
            "생년월일": birthdate,
            "주소": address,
            "키": height,
            "몸무게":weight,
            "임신여부": isPreg,
            "수유여부": isBFeeding,
            "진료일": officeVisitDateList,
            "진단명": diagDiseases
        }
    )



pprint([p for p in getPatientByName("John Lex")])
