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

        # contains the 진단명s
        self.currPatientDiseaseIndexSet = set()
        self.currPatientGSIngTupleSet = set()
        self.currPatientMSIngTupleSet = set()
        self.currPatientLGG4IngTupleSet = set()

        self.setupLogic()

    def setupLogic(self):
        # page_0
        self.ui.btn_enter_0.clicked.connect(self.check_password)
        # page_1 - home
        self.ui.btn_goToPatient_1.clicked.connect(self.go_to_patient)
        self.ui.btn_goToData_1.clicked.connect(self.go_to_data)
        self.ui.btn_logout_1.clicked.connect(self.logout)
        # page_2
        self.ui.btn_findExistingPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.btn_registerNewPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.btn_home_2.clicked.connect(self.go_to_home)
        # page_3 - register new patient page 1
        self.ui.btn_home_3.clicked.connect(lambda x: self.go_home(3))
        self.ui.btn_cancel_3.clicked.connect(self.cancel_register_new_patient)
        self.ui.btn_next_3.clicked.connect(self.go_to_register_new_patient_page2)
        self.ui.btn_checkUniqID_3.clicked.connect(self.check_unique_ID)
        # page_4 register new patient page 2
        self.ui.btn_cancel_4.clicked.connect(self.cancel_register_new_patient)
        self.ui.btn_back_4.clicked.connect(self.go_back_to_register_new_patient_page1)
        self.ui.btn_registerClient_4.clicked.connect(self.register_client)
        # page_5 find existing client
        self.ui.btn_cancel_5.clicked.connect(self.cancel_find_existing_client)
        self.ui.btn_home_5.clicked.connect(lambda x: self.go_home(5))
        self.ui.btn_findbyID_5.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_5.text()))
        self.ui.btn_findbyName_5.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_5.text()))
        self.ui.btn_confirmClient_5.clicked.connect(lambda x: self.go_to_edit_existing_patient_page1(self.get_selected_patient_id()))
        # page_6
        self.ui.btn_home_6.clicked.connect(lambda x: self.go_home(6))
        self.ui.btn_cancel_6.clicked.connect(self.cancel_edit_existing_patient)
        self.ui.btn_save_6.clicked.connect(lambda x: self.update_edit_existing_patient_data_page1())
        self.ui.btn_save_next_6.clicked.connect(lambda x: self.go_to_edit_existing_patient_page2(self.ui.lineEdit_ID_6.text()))
        # page_7
        self.ui.btn_back_7.clicked.connect(self.go_back_to_edit_existing_patient_page1)
        self.ui.btn_save_7.clicked.connect(lambda x: self.update_edit_existing_patient_data_page2())
        self.ui.btn_save_next_7.clicked.connect(lambda x: self.save_and_go_to_nutrients_edit_page(self.ui.lineEdit_ID_7.text()))

    def go_home(self, currPage):
        if self.warn_before_leaving() == False:
            return
        else:
            if currPage == 3:
                self.clear_register_new_patient()
            elif currPage == 5:
                self.clear_find_existing_client()
            elif currPage == 6:
                self.clear_edit_existing_client()
            else: 
                pass
            self.ui.stackedWidget.setCurrentIndex(1)

    # TODO - Figure out if it was saved before pressing back button; if so, don't show warning message
    def go_back_to_edit_existing_patient_page1(self):
        # if self.warn_before_leaving() == False:
        #     return
        # else:
        #     self.go_to_edit_existing_patient_page1(self.ui.lineEdit_ID_7.text())
        self.go_to_edit_existing_patient_page1(self.ui.lineEdit_ID_7.text())

    def clear_edit_existing_client(self):
        self.ui.lineEdit_ID_6.setText("")
        self.ui.lineEdit_name_6.setText("")
        self.ui.radioBtn_male_6.setChecked(True)
        self.ui.radioBtn_female_6.setChecked(False)
        self.ui.dateEdit_birthdate_6.setDate(QtCore.QDate(1900, 1, 1))
        self.ui.lineEdit_address_6.setText("")
        self.ui.lineEdit_height_6.setText("")
        self.ui.lineEdit_weight_6.setText("")
        self.ui.ckBox_preg_6.setChecked(False)
        self.ui.ckBox_bFeeding_6.setChecked(False)
        self.ui.dateEdit_lastOfficeVisit_6.setDate(QtCore.QDate.currentDate())

        self.currPatientDiseaseIndexSet.clear()
        self.currPatientGSIngTupleSet.clear()
        self.currPatientMSIngTupleSet.clear()
        self.currPatientLGG4IngTupleSet.clear()

    def cancel_edit_existing_patient(self):
        self.clear_edit_existing_client()
        self.ui.stackedWidget.setCurrentIndex(5)

    def go_to_register_new_patient_page2(self):
        tempID = self.ui.lineEdit_ID_3.text()
        tempName = self.ui.lineEdit_name_3.text()

        if len(tempID) == 0 or len(tempName) == 0:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("ID, 이름, 생년월일은 필수입니다.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()
        else:
            self.ui.stackedWidget.setCurrentIndex(4)
            if len(self.currPatientDiseaseIndexSet) == 0 and len(self.currPatientGSIngTupleSet) == 0 and len(self.currPatientMSIngTupleSet)==0 and len(self.currPatientLGG4IngTupleSet) == 0:
                myCursor_dis = get_all_diseases()
                create_checkbox_lw(myCursor_dis, self.ui.listWidget_diseases_4, '질병명', True, None)
                myCursor_gs = get_ingredients_guepsung()
                create_checkbox_level_tw(myCursor_gs, self.ui.tableWidget_allergies_gs_4, "식품명", True, None)
                myCursor_ms = get_ingredients_mansung()
                create_checkbox_level_tw(myCursor_ms, self.ui.tableWidget_allergies_ms_4, "식품명", True, None)
                myCursor_lgg4 = get_ingredients_mansung_lgg4()
                create_checkbox_level_tw(myCursor_lgg4, self.ui.tableWidget_allergies_lgg4_4, "식품명", True, None)
            else: #if coming from register_new_client_page2
                if len(self.currPatientDiseaseIndexSet) != 0:
                    for index in self.currPatientDiseaseIndexSet:
                        ckbtn = self.ui.listWidget_diseases_4.item(index)
                        ckbtn.setCheckState(QtCore.Qt.Checked)
                if len(self.currPatientGSIngTupleSet) != 0:
                    self.build_current_patient_tw(self.currPatientGSIngTupleSet, self.ui.tableWidget_allergies_gs_4)
                if len(self.currPatientMSIngTupleSet) != 0:
                    self.build_current_patient_tw(self.currPatientMSIngTupleSet, self.ui.tableWidget_allergies_ms_4)
                if len(self.currPatientLGG4IngTupleSet) != 0:
                    self.build_current_patient_tw(self.currPatientLGG4IngTupleSet, self.ui.tableWidget_allergies_lgg4_4)

    def build_current_patient_tw(self, s, tw):
        for index, levelStr in s:
            tw.item(index, 0).setCheckState(QtCore.Qt.Checked)
            tw.item(index, 1).setText(levelStr)

    def clear_find_existing_client(self):
        self.ui.lineEdit_ID_5.setText("")
        self.ui.lineEdit_name_5.setText("")
        self.ui.tableWidget_clientCandidates_5.setRowCount(0)

    def cancel_find_existing_client(self):
        self.clear_find_existing_client()
        self.ui.stackedWidget.setCurrentIndex(2)

    def warn_before_leaving(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Warning")
        msgbox.setText("현재 페이지 정보가 저장되지않습니다. 계속하시겠습니까?")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.No)
        ret = msgbox.exec_()
        if ret == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def clear_register_new_patient(self):
        self.ui.lineEdit_ID_3.setText("")
        self.ui.lineEdit_name_3.setText("")
        self.ui.radioBtn_male_3.setChecked(True)
        self.ui.radioBtn_female_3.setChecked(False)
        self.ui.dateEdit_birthdate_3.setDate(QtCore.QDate(1900, 1, 1))
        self.ui.lineEdit_address_3.setText("")
        self.ui.lineEdit_height_3.setText("")
        self.ui.lineEdit_weight_3.setText("")
        self.ui.ckBox_preg_3.setChecked(False)
        self.ui.ckBox_bFeeding_3.setChecked(False)
        self.ui.dateEdit_lastOfficeVisit_3.setDate(QtCore.QDate.currentDate())

        self.currPatientDiseaseIndexSet.clear()
        self.currPatientGSIngTupleSet.clear()
        self.currPatientMSIngTupleSet.clear()
        self.currPatientLGG4IngTupleSet.clear()

    def cancel_register_new_patient(self):
        if self.warn_before_leaving() == False:
            return
        else:
            self.clear_register_new_patient()
            self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_previous_page(self, currPage):
        self.ui.stackedWidget.setCurrentIndex(currPage - 1)

    def logout(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def go_to_home(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_find_existing_patient(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def go_back_to_register_new_patient_page1(self):
        self.currPatientDiseaseIndexSet = build_disease_index_set_from_lw(self.ui.listWidget_diseases_4)
        self.currPatientGSIngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_gs_4)
        self.currPatientMSIngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_ms_4)
        self.currPatientLGG4IngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_lgg4_4)

        self.ui.stackedWidget.setCurrentIndex(3)

    #############################
    # TODO - NEED TO WORK ON DATA PAGE
    #############################
    def updatePatients(self):
        # for patient in getAllPatients():
        #     self.tableWidget_clientCandidates_5.
        #     patient.
        pass

    def go_to_data(self):
        pass

    def go_to_patient(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def check_password(self):
        pwd = self.ui.lineEdit_pw_0.text()
        if pwd == "kiho":
            self.ui.lineEdit_pw_0.setText("")
            self.ui.stackedWidget.setCurrentIndex(1)
        elif len(pwd) != 0:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("비밀번호가 틀립니다.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()
        else:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("비밀번호를 입력해주세요.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()

    def find_patients_by_name(self, name):
        if not name:
            found_patients = get_all_patients()
        else:
            found_patients = get_patients_by_name(name)
        self.populate_found_patients(found_patients)

    def find_patients_by_id(self, id):
        if not id:
            found_patients = get_all_patients()
        else:
            found_patients = get_patient_by_id(id)
        self.populate_found_patients(found_patients)

    def populate_found_patients(self, found_patients):
        self.ui.tableWidget_clientCandidates_5.setRowCount(found_patients.count())
        i=0
        for patient in found_patients:
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

    def go_to_edit_existing_patient_page1(self, id):
        self.ui.stackedWidget.setCurrentIndex(6)
        selected_patient_id = self.get_selected_patient_id()
        self.clear_find_existing_client()
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

    def save_and_go_to_nutrients_edit_page(self, id):
        self.update_edit_existing_patient_data_page2()
        self.go_to_nutrients_edit_page(id)

    def go_to_nutrients_edit_page(self, id):
        self.ui.stackedWidget.setCurrentIndex(8)

        patient = get_patient_by_id(id)
        self.ui.lineEdit_name_8.setText(patient["이름"])
        self.ui.lineEdit_ID_8.setText(patient["ID"])
        self.ui.lineEdit_birthdate_8.setText(patient["생년월일"])
        self.ui.lineEdit_age_8.setText(str(calculate_age_from_birthdate_string(patient["생년월일"])))
        self.ui.lineEdit_lastOfficeVisit_8.setText(patient["진료일"])
        self.ui.lineEdit_height_8.setText(str(patient["키"]))
        self.ui.lineEdit_weight_8.setText(str(patient["몸무게"]))

    def go_to_edit_existing_patient_page2(self, id):
        self.update_edit_existing_patient_data_page1()
        self.ui.stackedWidget.setCurrentIndex(7)
        self.populate_existing_patient_detail(id)

    def populate_existing_patient_detail(self, id):
        patient = patients_collection.find_one({"ID": id})

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

    def update_edit_existing_patient_data_page1(self):
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

    def update_edit_existing_patient_data_page2(self):
        diseaseStr = convert_lw_to_string(self.ui.listWidget_diseases_7)
        gsTupleList = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_gs_7)
        msTupleList = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_ms_7)
        lgg4TupleList = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_lgg4_7)
        update_patient_detail_second_page(self.ui.lineEdit_ID_7.text(), diseaseStr, gsTupleList, msTupleList, lgg4TupleList)

    def register_client(self):
        if len(self.ui.lineEdit_ID_3.text()) == 0 or len(self.ui.lineEdit_name_3.text()) == 0:
            create_warning_message("ID, 이름, 생년월일은 필수입니다.")
        else:
            id = self.ui.lineEdit_ID_3.text()
            name = self.ui.lineEdit_name_3.text()
            patientObj = get_empty_patient_obj()
            patientObj['ID'] = id
            patientObj['이름'] = name
            patientObj['성별'] = "남" if self.ui.radioBtn_male_3.isChecked else "여"
            patientObj['생년월일'] = convert_DateEditWidget_to_string(self.ui.dateEdit_birthdate_3)
            patientObj['주소'] = self.ui.lineEdit_address_3.text()
            patientObj['진단명'] = convert_lw_to_string(self.ui.listWidget_diseases_4)
            patientObj['진료일'] = convert_DateEditWidget_to_string(self.ui.dateEdit_lastOfficeVisit_3)
            patientObj['방문횟수'] = 1
            patientObj['키'] = float(self.ui.lineEdit_height_3.text()) if self.ui.lineEdit_height_3.text() else 0
            patientObj['몸무게'] = float(self.ui.lineEdit_weight_3.text()) if self.ui.lineEdit_weight_3.text() else 0
            patientObj['임신여부'] = "T" if self.ui.ckBox_preg_3.isChecked() else "F"
            patientObj['수유여부'] = "T" if self.ui.ckBox_bFeeding_3.isChecked() else "F"
            patientObj['급성알레르기음식'] = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_gs_4)
            patientObj['만성알레르기음식'] = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_ms_4)
            patientObj['만성lgG4과민반응음식'] = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_lgg4_4)
            add_one_patient(patientObj)

            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Information")
            msgbox.setText("회원 "+name+" 등록되었습니다. 진단을 계속하시겠습니까?")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            ret = msgbox.exec_()
            if ret == QtWidgets.QMessageBox.Yes:
                self.go_to_nutrients_edit_page(id)
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
