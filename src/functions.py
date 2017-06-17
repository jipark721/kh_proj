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
def convert_tw_to_dict(tw):
    dict = {}
    for index in range(tw.rowCount()):
        if tw.item(index, 0).checkState() == QtCore.Qt.Checked and int(tw.item(index, 1).text()) != 0:
            dict[tw.item(index, 0).text()] = int(tw.item(index, 1).text())
    return dict

#for diagnosed diseases, iterate through rows and return a string separated by ","
def convert_lw_to_str_set(lw):
    toReturn =  set()
    for i in range(lw.count()):
        ckbtn = lw.item(i)
        if ckbtn.checkState() == QtCore.Qt.Checked:
            toReturn.add(ckbtn.text())
    return toReturn

def render_checkbox_lw(lw, content_collection, content_field_name, checked_content):
    lw.clear()
    for item in content_collection:
        ckbtnitem = QtWidgets.QListWidgetItem(item[content_field_name])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        if checked_content and item[content_field_name] in checked_content:
            ckbtnitem.setCheckState(QtCore.Qt.Checked)
        lw.addItem(ckbtnitem)

def populate_checkbox_tw_from_dict(tw, content_collection):
    tw.setRowCount(len(content_collection))
    tw.setColumnCount(2)
    rowIndex = 0
    for item in content_collection.keys():
        ckbtnitem = QtWidgets.QTableWidgetItem(item)
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        levelitem = QtWidgets.QTableWidgetItem(str(content_collection[item]))
        tw.setItem(rowIndex, 0, ckbtnitem)
        tw.setItem(rowIndex, 1, levelitem)
        rowIndex+=1

def update_checkbox_state_and_level_tw(tw, checked_content_dict):
    for index in range(tw.rowCount()):
        field_name = tw.item(index, 0).text()
        if field_name in checked_content_dict:
            tw.item(index, 0).setCheckState(QtCore.Qt.Checked)
            tw.item(index, 1).setText(str(checked_content_dict[field_name]))
        else:
            tw.item(index, 0).setCheckState(QtCore.Qt.Unchecked)
            tw.item(index, 1).setText("0")


def remove_checked_items_from_tw(nutrient_tw, nutrient_dict):
    for i in range(nutrient_tw.rowCount()):
        if nutrient_tw.item(i,0).checkState():
            nutrient_dict.pop(nutrient_tw.item(i,0).text(), None)
    populate_checkbox_tw_from_dict(nutrient_tw, nutrient_dict)


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

def render_checkbox_level_tw(content_collection, tw, content_field_name, checked_content_dict):
    tw.setRowCount(content_collection.count())
    tw.setColumnCount(2)
    rowIndex = 0
    for item in content_collection:
        ckbtnitem = QtWidgets.QTableWidgetItem(item[content_field_name])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        levelitem = QtWidgets.QTableWidgetItem("0")
        if checked_content_dict and item[content_field_name] in checked_content_dict:
            ckbtnitem.setCheckState(QtCore.Qt.Checked)
            levelitem.setText(str(checked_content_dict[item[content_field_name]]))
        tw.setItem(rowIndex, 0, ckbtnitem)
        tw.setItem(rowIndex, 1, levelitem)
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

def get_first_checked_btn_text_in_tw(tw):
    for index in range(tw.rowCount()):
        if tw.item(index, 0).checkState() == QtCore.Qt.Checked:
            return tw.item(index, 0).text()
    return None

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