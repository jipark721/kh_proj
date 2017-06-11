from mongoengine import *
from models import *
import datetime
from pprint import pprint

connect('khdb')

print("\nPrinting mongodb configurations...\n")

print("There are %d many patients data" % Patient.objects.count())
print("There are %d many diseases data" % Disease.objects.count())
print("There are %d many ingredients data" % Ingredient.objects.count())
print("There are %d many nutrients data\n\n" % Nutrient.objects.count())


def reset_database():
    Patient.objects.all().delete()
    Ingredient.objects.all().delete()
    Disease.objects.all().delete()
    Nutrient.objects.all().delete()


def print_all_patients():
    for patient in Patient.objects.all():
        pprint(patient)


def print_all_diseases():
    for disease in Disease.objects.all():
        pprint(disease)


def print_all_ingredients():
    for ingredient in Ingredient.objects.all():
        pprint(ingredient)


def print_all_nutrients():
    for nutrient in Nutrient.objects.all():
        pprint(nutrient)


def add_dummy_patient():
    Patient(ID="ID_1", 이름="상현", 성별="남", 생년월일=datetime.date(1992, 9, 17)).save()
    Patient(ID="ID_2", 이름="지영", 성별="여", 생년월일=datetime.date(1993, 7, 21)).save()


def add_dummy_nutrient():
    Nutrient(영양소명="영양소명_1").save()
    Nutrient(영양소명="영양소명_2").save()
    Nutrient(영양소명="영양소명_3").save()
    Nutrient(영양소명="영양소명_4").save()
    Nutrient(영양소명="영양소명_5").save()

def add_dummy_ingredient():
    Ingredient(식품명="식품명_1").save()
    Ingredient(식품명="식품명_2").save()
    Ingredient(식품명="식품명_3").save()
    Ingredient(식품명="식품명_4").save()
    Ingredient(식품명="식품명_5").save()

def add_dummy_disease():
    Disease(질병명="질병_1").save()
    Disease(질병명="질병_2").save()
    Disease(질병명="질병_3").save()
    Disease(질병명="질병_4").save()
    Disease(질병명="질병_5").save()

reset_database()
add_dummy_patient()
add_dummy_nutrient()
add_dummy_disease()
add_dummy_ingredient()
print_all_patients()
print_all_diseases()
print_all_ingredients()
print_all_nutrients()