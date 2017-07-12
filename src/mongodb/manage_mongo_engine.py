# -*- coding: utf-8 -*-
import sys
import os
if not os.getcwd().endswith("mongodb"):
    sys.path.insert(0, os.getcwd() + "/mongodb")
from models import *
from bson import json_util
import datetime
import random

def reset_database():
    Patient.objects.all().delete()
    Ingredient.objects.all().delete()
    Disease.objects.all().delete()
    Nutrient.objects.all().delete()

def export_db(path):
    try:
        print("Exporting db to " + path)
        collections = [(Patient.objects(), path + "patient.json"), (Ingredient.objects(), path +"ingredient.json"), (Disease.objects(), path + "disease.json"), (Nutrient.objects(), path + "nutrient.json")]
        for collection, file_name in collections:
            with open(file_name, 'w') as f:
                f.write(json_util.dumps(collection._collection_obj.find(collection._query), ensure_ascii=False, indent=4))
        print_db_stats()
        print("...done!\n")
        return True
    except:
        return False

def import_db(path):
    try:
        print("Importing db from " + path)
        reset_database()
        json_collections = [(Patient, path + "patient.json"), (Ingredient, path + "ingredient.json"), (Disease, path + "disease.json"), (Nutrient, path + "nutrient.json")]
        for obj, file_name in json_collections:
            with open(file_name, 'r') as f:
                for i in json_util.loads(f.read()):
                    obj(**i).save()
        print_db_stats()
        print("...done!\n")
        return True
    except:
        return False

def print_collection(collection):
    print(json_util.dumps(collection._collection_obj.find(collection._query), ensure_ascii=False, indent=4))


def print_all_patients():
    print_collection(Patient.objects())


def print_all_diseases():
    print_collection(Disease.objects())


def print_all_ingredients():
    print_collection(Ingredient.objects())


def print_all_nutrients():
    print_collection(Nutrient.objects())


def add_dummy_patient():
    Patient(ID="ID_1", 이름="안상현", 성별="남", 생년월일=datetime.date(1992, 9, 17),
            주소="서울시 종로구 부암동", 방문횟수=1, 키=150, 몸무게=50, 임신여부=False, 수유여부=False,
            급성알레르기음식={str(datetime.date(2017, 6, 10)): {"식품명_1": -3, "식품명_2": -1}},
            만성알레르기음식={str(datetime.date(2017, 6, 10)): {"식품명_1": -2, "식품명_2": -4, "식품명_4": -1}},
            만성lgG4과민반응음식={str(datetime.date(2017, 6, 10)): {"식품명_5": -1}},
            진단={str(datetime.date(2017, 6, 10)): {"질병명_3"}}, 진료일=[datetime.date(2017, 6, 10)]) \
        .save()

    Patient(ID="ID_2", 이름="박지영", 성별="여", 생년월일=datetime.date(1993, 7, 21),
            주소="서울시 송파구 잠실", 방문횟수=2, 키=170, 몸무게=49, 임신여부=False, 수유여부=False,
            급성알레르기음식={str(datetime.date(2017, 6, 5)): {"식품명_1": -3, "식품명_3": -1},
                      str(datetime.date(2017, 6, 8)): {"식품명_1": -3}},
            만성알레르기음식={str(datetime.date(2017, 6, 5)): {"식품명_2": -2, "식품명_4": -1},
                      str(datetime.date(2017, 6, 8)): {"식품명_2": -2, "식품명_5": -4, "식품명_4": -1}},
            만성lgG4과민반응음식={str(datetime.date(2017, 6, 5)): {"식품명_1": -1},
                          str(datetime.date(2017, 6, 8)): {"식품명_1": -1}},
            진단={str(datetime.date(2017, 6, 5)): {"질병명_4"},
                str(datetime.date(2017, 6, 8)): {"질병명_5"}},
            진료일=[datetime.date(2017, 6, 8), datetime.date(2017, 6, 5)]) \
        .save()

nut_cat_list = ["탄수화물", "단백질", "지방", "미네랄", "비타민", "플라보노이드", "카로테노이드", "기타1", "기타2", "기타3","기타4"]

def add_dummy_nutrient(i):
    Nutrient(
        영양소명="영양소명_" + str(i),
        영양소분류=nut_cat_list[random.randint(0, 10)],
        하루권장량RDA=random.uniform(0, 50),
        최대권장량WHO=random.uniform(0, 50),
        최대권장량식약처=random.uniform(0, 50),
        설명="설명_" + str(i),
        조리시주의할점="조리시주의할점_" + str(i),
        이야기거리="이야기거리_" + str(i),
        이야기1="이야기1_" + str(i),
        이야기2="이야기2_" + str(i),
        이야기3="이야기3_" + str(i),
        이야기4="이야기4_" + str(i),
        영양소명중국어="영양소명중국어_" + str(i),
        영양소명영어="영양소명영어_" + str(i),
        영양소명일본어="영양소명일본어_" + str(i),
        영양소명러시아어="영양소명러시아어_" + str(i),
        영양소명몽골어="영양소명몽골어_" + str(i),
        영양소명아랍어="영양소명아랍어_" + str(i),
        영양소명스페인어="영양소명스페인어_" + str(i),
        영양소명외국어8="영양소명외국어8_" + str(i),
        영양소명외국어9="영양소명외국어9_" + str(i),
        영양소명외국어10="영양소명외국어10_" + str(i),
        영양소명외국어11="영양소명외국어11_" + str(i),
        영양소명외국어12="영양소명외국어12_" + str(i)).save()


def add_dummy_ingredient(i):
    Ingredient(
        식품명="식품명_" + str(i),
        식품명영어="식품명영어_" + str(i),
        식품영양소관계={},
        식품분류1="식품분류1_" + str(i),
        식품분류2="식품분류2_" + str(i),
        식품분류3="식품분류3_" + str(i),
        식품분류4="식품분류4_" + str(i),
        식품분류5="식품분류5_" + str(i),
        식품설명="식품설명_" + str(i),
        식품명중국어="식품명중국어_" + str(i),
        식품명일본어="식품명일본어_" + str(i),
        식품명러시아어="식품명러시아어_" + str(i),
        식품명몽골어="식품명몽골어_" + str(i),
        식품명아랍어="식품명아랍어_" + str(i),
        식품명스페인어="식품명스페인어_" + str(i),
        식품명외국어8="식품명외국어8_" + str(i),
        식품명외국어9="식품명외국어9_" + str(i),
        식품명외국어10="식품명외국어10_" + str(i),
        식품명외국어11="식품명외국어11_" + str(i),
        학명="학명_" + str(i),
        이야기거리="이야기거리_" + str(i),
        특징="특징_" + str(i),
        보관법="보관법_" + str(i),
        조리시특성="조리시특성_" + str(i),
        도정상태="도정상태_" + str(i),
        가공상태="가공상태_" + str(i),
        즉시섭취="즉시섭취_" + str(i),
        출력대표성등급=random.randint(1, 5),
        단일식사분량=random.uniform(1, 5),
        단일식사분량설명="단일식사분량설명_" + str(i),
        폐기율=random.uniform(0, 100),
        단백질가식부=random.uniform(0, 100),
        가성알레르기등급=random.randint(-5, 0),
        급성알레르기가능여부=random.uniform(0, 1) < 0.03,
        만성알레르기가능여부=random.uniform(0, 1) < 0.03,
        만성lgG4과민반응가능여부=random.uniform(0, 1) < 0.01,
        멸종등급=random.randint(1, 5),
        원산지분류1="원산지분류1_" + str(i),
        원산지분류2="원산지분류2_" + str(i),
        원산지분류3="원산지분류3_" + str(i),
        원산지분류4="원산지분류4_" + str(i),
        원산지분류5="원산지분류5_" + str(i),
        특산지분류1="특산지분류1_" + str(i),
        특산지분류2="특산지분류2_" + str(i),
        특산지분류3="특산지분류3_" + str(i),
        특산지분류4="특산지분류4_" + str(i),
        특산지분류5="특산지분류5_" + str(i),
        항상비권고식품여부=random.uniform(0, 1) < 0.01).save()


def add_dummy_disease(i):
    Disease(
        질병명="질병명_" + str(i),
        질병명영어="disease_name" + str(i),
        질병식품관계={},
        질병영양소관계={},
    ).save()


def add_dummy_relations():
    for disease in Disease.objects:
        for i in range(random.randint(2, 5)):
            disease.질병식품관계[
                Ingredient.objects[
                    random.randint(1, Ingredient.objects.count()-1)
                ].식품명
            ] = random.randint(-5, 5)

            disease.질병영양소관계[
                Nutrient.objects[
                    random.randint(1, Nutrient.objects.count()-1)
                ].영양소명
            ] = random.randint(-5, 5)
        disease.save()

    for ingredient in Ingredient.objects:
        for i in range(random.randint(3, 7)):
            ingredient.식품영양소관계[
                Nutrient.objects[
                    random.randint(1, Nutrient.objects.count()-1)
                ].영양소명
            ] = random.uniform(0, 100)
        ingredient.save()

        for nutrient, quant in ingredient.식품영양소관계.items():
            target_nutrient = Nutrient.objects.get(영양소명=nutrient)
            target_nutrient.포함식품리스트[ingredient.식품명] = quant
            target_nutrient.save()

def print_db_stats():
    print("\n\nThere are %d many patients data" % Patient.objects.count())
    print("There are %d many diseases data" % Disease.objects.count())
    print("There are %d many ingredients data" % Ingredient.objects.count())
    print("There are %d many nutrients data\n\n" % Nutrient.objects.count())

def populate_dummy():
    reset_database()
    add_dummy_patient()
    for i in range(100):
        add_dummy_nutrient(i)
    for i in range(300):
        add_dummy_ingredient(i)
    for i in range(100):
        add_dummy_disease(i)
    add_dummy_relations()

# reset_database()
# populate_dummy()