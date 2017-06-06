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
