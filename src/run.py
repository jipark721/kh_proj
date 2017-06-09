# -*- coding: utf-8 -*-

import sys
from ui import UI
from PyQt5 import QtGui, QtWidgets, QtCore
from mongodb.utils import *
from decimal import Decimal
from functions import *


class MyFoodRecommender(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyFoodRecommender, self).__init__(parent)
        self.ui = UI()
        self.ui.setupUi(self)
        self.setupLogic()

    def setupLogic(self):
        # page_3
        self.ui.btn_checkUniqID_3.clicked.connect(self.check_unique_ID)
        # page 4
        self.ui.btn_registerClient_4.clicked.connect(self.register_client)
        # page_5
        self.ui.btn_findbyID_5.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_5.text()))
        self.ui.btn_findbyName_5.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_5.text()))
        self.ui.btn_confirmClient_5.clicked.connect(lambda x: self.populate_selected_patient())
        # page_6
        self.ui.btn_save_6.clicked.connect(lambda x: self.update_existing_patient_data_first_page())
        self.ui.btn_save_next_6.clicked.connect(lambda x: self.go_2_existing_patient_detail_second_page(self.ui.lineEdit_ID_6.text()))
        # page_7
        self.ui.btn_save_7.clicked.connect(lambda x: self.update_existing_patient_data_second_page())
        self.ui.btn_save_next_7.clicked.connect(lambda x: self.save_and_go_2_nutrients_edit_page(self.ui.lineEdit_ID_7.text()))

    def find_patients_by_name(self, name):
        if not name:
            found_patients = get_all_patients()
        else:
            found_patients = get_patients_by_name(name)
        self.populate_found_patients(found_patients)

    def find_patients_by_id(self, id):
        if not id:
            found_patients = patients_collection.find()
            #found_patients = get_all_patients()
        else:
            found_patients = patients_collection.find_one({'ID': id})
            #found_patients = get_patient_by_id(id)
        self.populate_found_patients(found_patients)

    def populate_found_patients(self, found_patients):
        print(found_patients.count())
        self.ui.tableWidget_clientCandidates_5.setRowCount(found_patients.count())
        i=0
        for patient in found_patients:
            print("index at "+str(i)+" id found " + patient["ID"])
            self.ui.tableWidget_clientCandidates_5.setItem(i, 0, make_tw_checkbox_item(patient['ID'], False))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 1, make_tw_str_item(patient['이름']))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 2, make_tw_str_item(patient['생년월일']))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 3, make_tw_str_item(patient['주소']))
            i += 1

    def get_selected_patient_id(self):
        for patient_idx in range(self.ui.tableWidget_clientCandidates_5.rowCount()):
            if self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).checkState() == QtCore.Qt.Checked:
                return self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).text()
        return None

    def populate_selected_patient(self):
        self.ui.stackedWidget.setCurrentIndex(6)
        selected_patient_id = self.get_selected_patient_id()
        print(selected_patient_id)
        if selected_patient_id:
            patient = patients_collection.find_one({'ID': selected_patient_id})
            self.ui.lineEdit_ID_6.setText(patient['ID'])
            self.ui.lineEdit_name_6.setText(patient['이름'])
            if patient['성별'] == "남":
                self.ui.radioBtn_male_6.setChecked(True)
                self.ui.radioBtn_female_6.setChecked(False)
            else:
                self.ui.radioBtn_male_6.setChecked(False)
                self.ui.radioBtn_female_6.setChecked(True)
            self.ui.dateEdit_birthdate_6.setDate(convert_date_string_to_QDate_obj(patient['생년월일']))
            self.ui.lineEdit_address_6.setText(patient['주소'])
            self.ui.lineEdit_height_6.setText(str(patient['키']))
            self.ui.lineEdit_weight_6.setText(str(patient['몸무게']))
            self.ui.ckBox_preg_6.setChecked(True) if patient['임신여부'] == "T" else self.ui.ckBox_preg_6.setChecked(False)
            self.ui.ckBox_bFeeding_6.setChecked(True) if patient['수유여부'] == "T" else self.ui.ckBox_bFeeding_6.setChecked(False)
            self.ui.dateEdit_lastOfficeVisit_6.setDate(convert_date_string_to_QDate_obj(patient['진료일']))

    def save_and_go_2_nutrients_edit_page(self, id):
        self.update_existing_patient_data_second_page()
        self.go_2_nutrients_edit_page(id)

    def go_2_nutrients_edit_page(self, id):
        self.ui.stackedWidget.setCurrentIndex(8)

        patient = get_patient_by_id(id)
        self.ui.lineEdit_name_8.setText(patient["이름"])
        self.ui.lineEdit_ID_8.setText(patient["ID"])
        self.ui.lineEdit_birthdate_8.setText(patient["생년월일"])
        self.ui.lineEdit_age_8.setText(str(calculate_age_from_birthdate_string(patient["생년월일"])))
        self.ui.lineEdit_lastOfficeVisit_8.setText(patient["진료일"])
        self.ui.lineEdit_height_8.setText(str(patient["키"]))
        self.ui.lineEdit_weight_8.setText(str(patient["몸무게"]))



    def go_2_existing_patient_detail_second_page(self, id):
        self.update_existing_patient_data_first_page()
        self.ui.stackedWidget.setCurrentIndex(7)
        self.populate_existing_patient_detail(id)

    def populate_existing_patient_detail(self, id):
        print("id chosen: "+id)
        print("there are " + str(get_all_patients().count()) + " patients")
        patient = patients_collection.find_one({"ID": id})
        print(type(patient))

        print(patient["이름"])
        self.ui.lineEdit_name_7.setText(patient["이름"])
        self.ui.lineEdit_ID_7.setText(patient["ID"])
        self.ui.lineEdit_birthdate_7.setText(patient["생년월일"])
        self.ui.lineEdit_age_7.setText(str(calculate_age_from_birthdate_string(patient["생년월일"])))
        self.ui.lineEdit_lastOfficeVisit_7.setText(patient["진료일"])
        self.ui.lineEdit_height_7.setText(str(patient["키"]))
        self.ui.lineEdit_weight_7.setText(str(patient["몸무게"]))

        set_dis = convert_string_2_set(patient["진단명"])
        myCursor_dis = get_all_diseases()
        create_checkbox_lw(myCursor_dis, self.ui.listWidget_diseases_7, "질병명", False, set_dis)

        myCursor_gs = get_ingredients_guepsung()
        create_checkbox_level_tw(myCursor_gs, self.ui.tableWidget_allergies_gs_7, "식품명", False, patient["급성알레르기음식"])
        myCursor_ms = get_ingredients_mansung()
        create_checkbox_level_tw(myCursor_ms, self.ui.tableWidget_allergies_ms_7, "식품명", False, patient["만성알레르기음식"])
        myCursor_lgg4 = get_ingredients_mansung_lgg4()
        create_checkbox_level_tw(myCursor_lgg4, self.ui.tableWidget_allergies_lgg4_7, "식품명", False, patient["만성lgG4과민반응음식"])

    def update_existing_patient_data_first_page(self):
        id = self.ui.lineEdit_ID_6.text()
        name = self.ui.lineEdit_name_6.text()
        sex = "남" if self.ui.radioBtn_male_6.isChecked else "여"
        birthdate = self.ui.dateEdit_birthdate_6.date().toString(format=QtCore.Qt.ISODate)
        address = self.ui.lineEdit_address_6.text()
        if self.ui.lineEdit_height_6.text():
            # height = Decimal(float(self.ui.lineEdit_height_6.text()))
            height = float(self.ui.lineEdit_height_6.text())
        else:
            height = None
        if self.ui.lineEdit_weight_6.text():
            # weight = Decimal(float(self.ui.lineEdit_weight_6.text()))
            weight = float(self.ui.lineEdit_weight_6.text())
        else:
            weight = None
        isPreg = "T" if self.ui.ckBox_preg_6.isChecked() else "F"
        isBFeeding = "T" if self.ui.ckBox_bFeeding_6.isChecked() else "F"
        officeVisitDateList = self.ui.dateEdit_lastOfficeVisit_6.date().toString(format=QtCore.Qt.ISODate)

        update_patient_detail_first_page(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding, officeVisitDateList)

    def update_existing_patient_data_second_page(self):
        diseaseStr = convert_lw_2_string(self.ui.listWidget_diseases_7)
        gsTupleList = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_gs_7)
        msTupleList = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_ms_7)
        lgg4TupleList = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_lgg4_7)
        update_patient_detail_second_page(self.ui.lineEdit_ID_7.text(), diseaseStr, gsTupleList, msTupleList, lgg4TupleList)

    def register_client(self):
        if len(self.ui.lineEdit_ID_3.text()) == 0 or len(self.ui.lineEdit_name_3.text()) == 0:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("ID, 이름, 생년월일은 필수입니다.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()
        else:
            id = self.ui.lineEdit_ID_3.text()
            name = self.ui.lineEdit_name_3.text()
            sex = "남" if self.ui.radioBtn_male_3.isChecked else "여"
            birthdate = self.ui.dateEdit_birthdate_3.date().toString(format=QtCore.Qt.ISODate)
            address = self.ui.lineEdit_address_3.text()
            if self.ui.lineEdit_height_3.text():
                height = float(self.ui.lineEdit_height_3.text())
                # height = Decimal(float(self.ui.lineEdit_height_3.text()))
            else:
                height = 0
            if self.ui.lineEdit_weight_3.text():
                weight = float(self.ui.lineEdit_weight_3.text())
                # weight = Decimal(float(self.ui.lineEdit_weight_3.text()))
            else:
                weight = 0
            isPreg = "T" if self.ui.ckBox_preg_3.isChecked() else "F"
            isBFeeding = "T" if self.ui.ckBox_bFeeding_3.isChecked() else "F"
            officeVisitDateList = self.ui.dateEdit_lastOfficeVisit_3.date().toString(format=QtCore.Qt.ISODate)

            diagDiseasesStr = convert_lw_2_string(self.ui.listWidget_diseases_4)
            # diagDiseasesStr = ""
            # isFirstCheckedFound = False
            # for i in range(self.ui.listWidget_diseases_4.count()):
            #     ckbtn = self.ui.listWidget_diseases_4.item(i)
            #     if ckbtn.checkState() == QtCore.Qt.Checked:
            #         if not isFirstCheckedFound:
            #             diagDiseasesStr = ckbtn.text()
            #             isFirstCheckedFound = True
            #         else:
            #             diagDiseasesStr = diagDiseasesStr + "," + ckbtn.text()

            patientObj = get_empty_patient_obj()
            patientObj['ID'] = id
            patientObj['이름'] = name
            patientObj['성별'] = sex
            patientObj['생년월일'] = birthdate
            patientObj['주소'] = address
            patientObj['진단명'] = diagDiseasesStr
            patientObj['진료일'] = officeVisitDateList
            patientObj['방문횟수'] = 1
            patientObj['키'] = height
            patientObj['몸무게'] = weight
            patientObj['임신여부'] = isPreg
            patientObj['수유여부'] = isBFeeding
            patientObj['급성알레르기음식'] = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_gs_4)
            patientObj['만성알레르기음식'] = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_ms_4)
            patientObj['만성lgG4과민반응음식'] = convert_tw_2_tuple_list(self.ui.tableWidget_allergies_lgg4_4)
            add_one_patient(patientObj)

            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Information")
            msgbox.setText("회원 "+name+" 등록되었습니다. 진단을 계속하시겠습니까?")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            ret = msgbox.exec_()
            if ret == QtWidgets.QMessageBox.Yes:
                self.go_2_nutrients_edit_page(id)
            else:
                self.ui.stackedWidget.setCurrentIndex(1)

    def check_unique_ID(self):
        uniqIDChecked = False
        while (uniqIDChecked == False):
            idCand = self.ui.lineEdit_ID_3.text()
            idFound = get_patient_by_id(idCand)
            if idFound.count() != 0:
                self.ui.lineEdit_ID_3.setText("")
                msgbox = QtWidgets.QMessageBox()
                msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                msgbox.setText("동일한 ID가 존재합니다. 다른 ID를 시도해주세요")
                msgbox.setWindowTitle("Error")
                msgbox.exec_()
            else:
                msgbox = QtWidgets.QMessageBox()
                msgbox.setText("사용가능한 아이디입니다")
                msgbox.exec_()
                uniqIDChecked = True

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyFoodRecommender()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
