# -*- coding: utf-8 -*-
import sys
import os
if not os.getcwd().endswith("mongodb"):
    sys.path.insert(0, os.getcwd() + "/mongodb")
from mongoengine import *
import datetime
connect('khdb')


class Patient(Document):
    _id = DynamicField()
    ID = StringField(required=True, max_length=100)
    이름 = StringField(required=True, max_length=10)
    성별 = StringField(required=True, max_length=1)
    생년월일 = DateTimeField(default=datetime.date.today())
    주소 = StringField(max_length=200)
    방문횟수 = IntField(default=0)
    키 = DecimalField(default=0.0)
    몸무게 = DecimalField(default=0.0)
    임신여부 = BooleanField(default=False)
    수유여부 = BooleanField(default=False)
    급성알레르기음식 = DictField() # Map of DateTimeField to Map of Alg:lvl { 진료일 : { 알레르기음식: 레벨 } }
    만성알레르기음식 = DictField()
    만성lgG4과민반응음식 = DictField()
    진단 = DictField() # Map of DateTimeField to set of strings { 진료일 : { 질병명 } }
    진료일 = SortedListField(DateTimeField())

    def __str__(self):
        return "ID: " + str(self.ID) + "\n" + "이름: " + str(self.이름) + "\n" + "성별: " + str(self.성별) + "\n" + "생년월일: " + str(self.생년월일) + "\n" + "주소: " + str(self.주소) + "\n" + "방문횟수: " + str(self.방문횟수) + "\n" + "키: " + str(self.키) + "\n" + "몸무게: " + str(self.몸무게) + "\n" + "임신여부: " + str(self.임신여부) + "\n" + "수유여부: " + str(self.수유여부) + "\n" + "급성알레르기음식: " + str(self.급성알레르기음식) + "\n" + "만성알레르기음식: " + str(self.만성알레르기음식) + "\n" + "만성lgG4과민반응음식: " + str(self.만성lgG4과민반응음식) + "\n" + "진단: " + str(self.진단) + "\n" + "진료일: " + str(self.진료일)

class Disease(Document):
    _id = DynamicField()
    질병명 = StringField(required=True, max_length=50)
    질병명영어 = StringField(max_length=50)
    질병식품관계 = DictField()
    질병영양소관계 = DictField()

    def __str__(self):
        return self.질병명


class Ingredient(Document):
    _id = DynamicField()
    식품명 = StringField(required=True, max_length=100)
    식품명영어 = StringField(max_length=100)
    식품영양소관계 = DictField() # { 영양소명 : 함량 }
    식품분류1 = StringField(max_length=100)
    식품분류2 = StringField(max_length=100)
    식품분류3 = StringField(max_length=100)
    식품분류4 = StringField(max_length=100)
    식품분류5 = StringField(max_length=100)
    식품설명 = StringField(max_length=100)
    식품명중국어 = StringField(max_length=100)
    식품명일본어 = StringField(max_length=100)
    식품명러시아어 = StringField(max_length=100)
    식품명몽골어 = StringField(max_length=100)
    식품명아랍어 = StringField(max_length=100)
    식품명스페인어 = StringField(max_length=100)
    식품명외국어8 = StringField(max_length=100)
    식품명외국어9 = StringField(max_length=100)
    식품명외국어10 = StringField(max_length=100)
    식품명외국어11 = StringField(max_length=100)
    학명 = StringField(max_length=100)
    이야기거리 = StringField(max_length=100)
    특징 = StringField(max_length=100)
    보관법 = StringField(max_length=100)
    조리시특성 = StringField(max_length=100)
    도정상태 = StringField(max_length=100)
    가공상태 = StringField(max_length=100)
    즉시섭취 = BooleanField()
    출력대표성등급 = IntField(max_value=5, min_value=1)
    단일식사분량 = DecimalField(min_value=0)
    단일식사분량설명 = StringField(max_length=100)
    폐기율 = DecimalField()
    단백질가식부 = DecimalField()
    가성알레르기등급 = IntField(max_value=0, min_value=-5)
    급성알레르기가능여부 = BooleanField()
    만성알레르기가능여부 = BooleanField()
    만성lgG4과민반응가능여부 = BooleanField()
    멸종등급 = IntField(max_value=5, min_value=0)
    원산지분류1 = StringField(max_length=100)
    원산지분류2 = StringField(max_length=100)
    원산지분류3 = StringField(max_length=100)
    원산지분류4 = StringField(max_length=100)
    원산지분류5 = StringField(max_length=100)
    특산지분류1 = StringField(max_length=100)
    특산지분류2 = StringField(max_length=100)
    특산지분류3 = StringField(max_length=100)
    특산지분류4 = StringField(max_length=100)
    특산지분류5 = StringField(max_length=100)
    항상비권고식품여부 = BooleanField()

    def __str__(self):
        return self.식품명

class Nutrient(Document):
    _id = DynamicField()
    영양소명 = StringField(required=True, max_length=100)
    영양소분류 = StringField(max_length=100)
    하루권장량RDA = DecimalField(max_length=100)
    최대권장량WHO = DecimalField(max_length=100)
    최대권장량식약처 = DecimalField(max_length=100)
    설명 = StringField(max_length=100)
    조리시주의할점 = StringField(max_length=100)
    이야기거리 = StringField(max_length=100)
    이야기1 = StringField(max_length=100)
    이야기2 = StringField(max_length=100)
    이야기3 = StringField(max_length=100)
    이야기4 = StringField(max_length=100)
    이야기5 = StringField(max_length=100)
    영양소명중국어 = StringField(max_length=100)
    영양소명영어 = StringField(max_length=100)
    영양소명일본어 = StringField(max_length=100)
    영양소명러시아어 = StringField(max_length=100)
    영양소명몽골어 = StringField(max_length=100)
    영양소명아랍어 = StringField(max_length=100)
    영양소명스페인어 = StringField(max_length=100)
    영양소명외국어8 = StringField(max_length=100)
    영양소명외국어9 = StringField(max_length=100)
    영양소명외국어10 = StringField(max_length=100)
    영양소명외국어11 = StringField(max_length=100)
    영양소명외국어12 = StringField(max_length=100)
    포함식품리스트 = DictField()

    def __str__(self):
        return self.영양소명