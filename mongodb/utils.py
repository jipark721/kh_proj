from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
khdb = client.get_database("khdb")
patients = khdb.get_collection("patients")
diseases = khdb.get_collection("diseases")
ingredients = khdb.get_collection("ingredients")


def getAllPatients():
    return patients.find()


def getPatientByName(name):
    return patients.find({"성명": name})


def getPatientById(id):
    return patients.find({"ID": id})


def getPatientByNameAndBirthDate(name, birthdate):
    return patients.find(
        {"$and":
             [{"성명": name},
              {"생일": birthdate}]
         }
    )

pprint([p for p in getPatientByName("John Lex")])
