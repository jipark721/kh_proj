from PyQt5 import QtGui, QtWidgets, QtCore
import datetime

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

#for allergy table widgets, iterate through rows and return a list of tuple(알레르기음식, level)
def convert_tw_to_tuple_list(tw):
    list = []
    for index in range(tw.rowCount()):
        if tw.item(index, 0).checkState() == QtCore.Qt.Checked and int(tw.item(index, 1).text()) != 0:
            mytup = tuple([tw.item(index, 0).text(), int(tw.item(index, 1).text())])
            list.append(mytup)
    return list

#for diagnosed diseases, iterate through rows and return a string separated by ","
def convert_lw_to_string(lw):
    toReturn = ""
    isFirstCheckedFound = False
    for i in range(lw.count()):
        ckbtn = lw.item(i)
        if ckbtn.checkState() == QtCore.Qt.Checked:
            if not isFirstCheckedFound:
                toReturn = ckbtn.text()
                isFirstCheckedFound = True
            else:
                toReturn = toReturn + "," + ckbtn.text()
    return toReturn

def populate_checkbox_lw(lw, content_collection, content_field_name):
    lw.clear()
    for item in content_collection:
        ckbtnitem = QtWidgets.QListWidgetItem(item[content_field_name])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        lw.addItem(ckbtnitem)

def update_checkbox_state_lw(lw, content_collection, content_field_name, checked_content):
    for i in range(lw.count()):
        if lw.item(i).text() in checked_content:
            lw.item(i).setCheckState(QtCore.Qt.Checked)
        else:
            lw.item(i).setCheckState(QtCore.Qt.Unchecked)

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
        if not isNewPatient and patientAllergyTupleList is not None:
            if len(patientAllergyTupleList) != 0:
                for allergicFoodLevelTuple in patientAllergyTupleList:
                    if item[content] == allergicFoodLevelTuple[0]:
                        ckbtnitem.setCheckState(QtCore.Qt.Checked)
                        levelitem = QtWidgets.QTableWidgetItem(str(allergicFoodLevelTuple[1]))
        tableWidget.setItem(rowIndex, 0, ckbtnitem)
        tableWidget.setItem(rowIndex, 1, levelitem)
        rowIndex = rowIndex + 1

def clear_checkbox_lw(lw):
    for index in range(lw.count()):
        lw.item(index).setCheckState(QtCore.Qt.Unchecked)

# def clear_ckbox_level_tw(tw):
#     for rowIndex in range(tw.rowCount):
#         tw.item(rowIndex, 0).setCheckState(QtCore.Qt.Unchecked)
#         tw.item(rowIndex, 1).text()

# iterate through listwidget and build a set of indices of checked diseases
def build_disease_index_set_from_lw(lw):
    s = set()
    for i in range(lw.count()):
        ckbtn = lw.item(i)
        if ckbtn.checkState() == QtCore.Qt.Checked:
            s.add(i)
    return s

# iterate through tablewidget and build a set of tuple(index, level) for each checked ingredient
def build_allergy_index_level_tuple_set_from_tw(tw):
    s = set()
    for rowIndex in range(tw.rowCount()):
        if tw.item(rowIndex, 0).checkState() == QtCore.Qt.Checked and int(tw.item(rowIndex, 1).text()) != 0:
            mytup = tuple([rowIndex, tw.item(rowIndex, 1).text()])
            s.add(mytup)
    return s

def convert_date_string_to_QDate_obj(dateStr):
    date = datetime.strptime(dateStr, '%Y/%m/%d')
    return QtCore.QDate(date.year, date.month, date.day)

def convert_DateEditWidget_to_string(dateEditWidget):
    return dateEditWidget.date().toString(format=QtCore.Qt.ISODate)

def calculate_age_from_birthdate_string(patient_birthdate):
    today = datetime.date.today()
    difference = today.year - patient_birthdate.year - ((today.month, today.day) < (patient_birthdate.month, patient_birthdate.day))
    return str(difference)

def create_warning_message(warnMsg):
    msgbox = QtWidgets.QMessageBox()
    msgbox.setIcon(QtWidgets.QMessageBox.Warning)
    msgbox.setText(warnMsg)
    msgbox.setWindowTitle("Error")
    msgbox.exec_()