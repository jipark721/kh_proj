# -*- coding: utf-8 -*-
from mongoengine import *
import datetime
connect('khdb')


class Patient(Document):
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
    급성알레르기음식 = ListField(StringField(max_length=100))
    만성알레르기음식 = ListField(StringField(max_length=100))
    만성lgG4과민반응음식 = StringField()
    진료 = DictField(default={})  # {진료일 : 진단명}

    def __str__(self):
        return self.ID + ", " + self.이름 + ", " + self.성별 + ", " + self.생년월일.strftime('%Y/%m/%d')

class Disease(Document):
    질병명 = StringField(required=True, max_length=50)
    질병명영어 = StringField(max_length=50)
    질병식품관계 = DictField(default={})
    질병영양소관계 = DictField(default={})

    def __str__(self):
        return self.질병명


class Ingredient(Document):
    식품명 = StringField(required=True, max_length=100)
    식품명영어 = StringField(max_length=100)
    식품영양소관계 = StringField(max_length=100)
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
    가성알레르기등급 = IntField(max_value=5, min_value=1)
    급성알레르기가능여부 = BooleanField()
    만성알레르기가능여부 = BooleanField()
    만성lgG4과민반응가능여부 = BooleanField()
    멸종등급 = IntField(max_value=5, min_value=1)
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
    영양소명 = StringField(required=True, max_length=100)
    거대영양소분류 = StringField(max_length=100)
    영양소분류 = StringField(max_length=100)
    하루권장량RDA = StringField(max_length=100)
    최대권장량WHO = StringField(max_length=100)
    최대권장량식약처 = StringField(max_length=100)
    설명 = StringField(max_length=100)
    조리시주의할점 = StringField(max_length=100)
    이야기거리 = StringField(max_length=100)
    이야기1 = StringField(max_length=100)
    이야기2 = StringField(max_length=100)
    이야기3 = StringField(max_length=100)
    이야기4 = StringField(max_length=100)
    이야기5 = StringField(max_length=100)
    영양소명한국어 = StringField(max_length=100)
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

    def __str__(self):
        return self.영양소명