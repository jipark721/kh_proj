from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import datetime, date

def make_tw_str_item(content):
    return QtWidgets.QTableWidgetItem(content)

def make_tw_checkbox_item(content, isChecked):
    item = QtWidgets.QTableWidgetItem(content)
    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    if isChecked:
        item.setCheckState(QtCore.Qt.Checked)
    else:
        item.setCheckState(QtCore.Qt.Unchecked)
    return item

def make_lw_str_item(content):
    return QtWidgets.QListWidgetItem(content)

def make_lw_checkbox_item(content, isChecked):
    item = QtWidgets.QListWidgetItem(content)
    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    if isChecked:
        item.setCheckState(QtCore.Qt.Checked)
    else:
        item.setCheckState(QtCore.Qt.Unchecked)
    return item

def create_checkbox_lw(cursorToCollection, lw, content, isNewPatient, patientDiseaseSet):
    for item in cursorToCollection:
        ckbtnitem = QtWidgets.QListWidgetItem(item[content])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if (isNewPatient):
            ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        else:
            if item[content] in patientDiseaseSet:
                ckbtnitem.setCheckState(QtCore.Qt.Checked)
            else:
                ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        lw.addItem(ckbtnitem)

def create_checkbox_level_tw(cursorToCollection, tableWidget, content, isNewPatient, patientAllergyTupleList):
    tableWidget.setRowCount(cursorToCollection.count())
    tableWidget.setColumnCount(2)
    rowIndex = 0
    for item in cursorToCollection:
        ckbtnitem = QtWidgets.QTableWidgetItem(item[content])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        levelitem = QtWidgets.QTableWidgetItem("0")
        if not isNewPatient:
            for allergicFoodLevelTuple in patientAllergyTupleList:
                if item[content] == allergicFoodLevelTuple[0]:
                    ckbtnitem.setCheckState(QtCore.Qt.Checked)
                    levelitem = QtWidgets.QTableWidgetItem(str(allergicFoodLevelTuple[1]))
        tableWidget.setItem(rowIndex, 0, ckbtnitem)
        tableWidget.setItem(rowIndex, 1, levelitem)
        rowIndex = rowIndex + 1


def convert_date_string_to_QDate_obj(dateStr):
    date = datetime.strptime(dateStr, '%Y-%m-%d')
    return QtCore.QDate(date.year, date.month, date.day)

def calculate_age_from_birthdate_string(birthdateStr):
    today = date.today()
    birthdate = datetime.strptime(birthdateStr, '%Y-%m-%d')
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
