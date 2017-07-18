# -*- coding: utf-8 -*-
import sys
import os
if not os.getcwd().endswith("mongodb"):
    sys.path.insert(0, os.getcwd() + "/mongodb")
from models import *
from manage_mongo_engine import reset_database, print_db_stats
import ast
import xlrd
import pandas as pd
import sys

def read_xlsx_db(xls_file_name):
    if not xls_file_name.endswith(".xlsx"):
        print("Invalid file.\n")
        return False

    reset_database()

    workbook = xlrd.open_workbook(xls_file_name, encoding_override="utf_8")

    # Patients
    worksheet = workbook.sheet_by_name("patient")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
            print(cell.value)
        row_data["급성알레르기음식"] = convert_to_datastructure(row_data, "급성알레르기음식")
        row_data["만성lgG4과민반응음식"] = convert_to_datastructure(row_data, "만성lgG4과민반응음식")
        row_data["만성알레르기음식"] = convert_to_datastructure(row_data, "만성알레르기음식")
        row_data["진단"] = convert_to_datastructure(row_data, "진단")
        row_data["생년월일"] = pd.to_datetime(row_data["생년월일"])
        dates = convert_to_datastructure(row_data, "진료일")
        row_data["진료일"] = [d.date() for d in pd.to_datetime(dates)] if dates else []
        Patient(**row_data).save()


    # Nutrient
    worksheet = workbook.sheet_by_name("nutrient")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "":
                print(cell.value)
                row_data[keys[col_number]] = cell.value
        Nutrient(**row_data).save()

    # Ingredient
    worksheet = workbook.sheet_by_name("ingredient")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "":
                print(cell.value)

                row_data[keys[col_number]] = cell.value
        Ingredient(**row_data).save()


    # Disease
    worksheet = workbook.sheet_by_name("disease")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "":
                print(cell.value)

                row_data[keys[col_number]] = cell.value
        Disease(**row_data).save()


    # 식품영양소관계
    worksheet = workbook.sheet_by_name("식품영양소관계")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "" and cell.value != "-":
                print(cell.value)

                row_data[keys[col_number]] = cell.value
        ingredient = Ingredient.objects.get(식품명=row_data["식품영양소관계식품명"])
        del row_data["식품영양소관계식품명"]
        for nutrient_name, quantity in row_data.items():
            if quantity:
                ingredient.식품영양소관계[nutrient_name] = quantity
                nutrient = Nutrient.objects.get(영양소명=nutrient_name)
                nutrient.포함식품리스트[ingredient.식품명] = quantity
                nutrient.save()
        ingredient.save()


    # 질병식품관계
    worksheet = workbook.sheet_by_name("질병식품관계")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "" and cell.value != "-":
                print(cell.value)

                row_data[keys[col_number]] = cell.value
        disease = Disease.objects.get(질병명=row_data["질병식품관계질병명"])
        del row_data["질병식품관계질병명"]
        for ingredient_name, quantity in row_data.items():
            if quantity:
                disease.질병식품관계[ingredient_name] = quantity
        disease.save()


    # 질병영양소관계
    worksheet = workbook.sheet_by_name("질병영양소관계")
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(1, worksheet.nrows):
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            if cell.value and cell.value != "" and cell.value != "-":
                print(cell.value)

                row_data[keys[col_number]] = cell.value
        disease = Disease.objects.get(질병명=row_data["질병영양소관계질병명"])
        del row_data["질병영양소관계질병명"]
        for nutrient_name, quantity in row_data.items():
            if quantity:
                disease.질병영양소관계[nutrient_name] = quantity
        disease.save()


    print_db_stats()
    return True


# print("[Error in %s 식품영양소관계]: Nutrient [%s] does not exist in the nutrients list" %(row_data["식품명"], nutrient))
# print("[Error in %s 질병식품관계]: Ingredient [%s] does not exist in the ingredient list" %(row_data["질병명"], ingredient))

def convert_to_datastructure(row_data, field):
    try:
        return ast.literal_eval(row_data[field])
    except:
        print("Parse error for " + field)
        return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python read_from_xlsx.py $data.xlsx")
    elif str.endswith(sys.argv[1],".xlsx"):
        print("Importing database from xlsx file...")
        read_xlsx_db(sys.argv[1])
        print("...done!\n")
    else:
        print("Invalid file.\n")
