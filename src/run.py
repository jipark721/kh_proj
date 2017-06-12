# -*- coding: utf-8 -*-

import sys
from mongoengine import *
from ui import UI
from mongodb.utils import *
from functions import *
from mongodb.models import *

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

        # local classes
        self.current_date = datetime.date.today()
        self.current_patient = None
        self.local_급성알레르기음식 = None
        self.local_만성알레르기음식 = None
        self.local_만성lgG4과민반응음식 = None
        self.local_진단 = None

    def setupLogic(self):
        # page_0
        self.ui.btn_enter_0.clicked.connect(self.check_password)

        # page_1 - home
        self.ui.btn_goToPatient_1.clicked.connect(self.go_to_patient)
        self.ui.btn_goToData_1.clicked.connect(self.go_to_data)
        self.ui.btn_logout_1.clicked.connect(self.logout)

        # page_2 - select patient type
        self.ui.btn_findExistingPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.btn_registerNewPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.btn_home_2.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_home_3.clicked.connect(lambda x: self.go_home(3))

        # page_3 - register new patient page 1
        self.ui.btn_cancel_3.clicked.connect(self.cancel_register_new_patient)
        self.ui.btn_next_3.clicked.connect(self.go_to_register_new_patient_page2)
        self.ui.btn_checkUniqID_3.clicked.connect(self.check_unique_ID)

        # # page_4 - register new patient page 2
        # self.ui.btn_cancel_4.clicked.connect(self.cancel_register_new_patient)
        # self.ui.btn_back_4.clicked.connect(self.go_back_to_register_new_patient_page1)
        # self.ui.btn_registerClient_4.clicked.connect(self.register_client)

        # page_5 - find existing patient
        self.ui.btn_cancel_5.clicked.connect(self.cancel_find_existing_client)
        self.ui.btn_home_5.clicked.connect(lambda x: self.go_home(5))
        self.ui.btn_findbyID_5.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_5.text()))
        self.ui.btn_findbyName_5.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_5.text()))
        self.ui.btn_confirmClient_5.clicked.connect(lambda x: self.go_to_select_disease_and_allergies(self.get_selected_patient_id()))

        # page_6 - patient information view/edit
        # self.ui.btn_home_6.clicked.connect(lambda x: self.go_home(6))
        # self.ui.btn_cancel_6.clicked.connect(self.cancel_edit_existing_patient)
        # self.ui.btn_save_6.clicked.connect(lambda x: self.update_edit_existing_patient_data_page1())
        # self.ui.btn_save_next_6.clicked.connect(lambda x: self.go_to_edit_existing_patient_page2(self.ui.lineEdit_ID_6.text()))

        # page_7 - patient information (diseases / allergies)
        self.ui.btn_back_7.clicked.connect(self.go_back_to_edit_existing_patient_page1)
        self.ui.btn_save_next_7.clicked.connect(lambda x: self.save_and_go_to_nutrients_edit_page(self.ui.lineEdit_ID_7.text()))
        # self.ui.btn_save_7.clicked.connect(lambda x: self.update_edit_existing_patient_data_page2())

        # page 8 - nutrients edit page
        self.ui.btn_back_8.clicked.connect(self.go_back_to_edit_existing_patient_page2)
        #self.ui.btn_go2Rec_8.clicked.connect(self.update_recommended_nutrient)
        #self.ui.btn_go2NotRec_8.clicked.connect(self.update_not_recommended_nutrient)
        #self.ui.btn_save_next_8.clicked.connect()

        # page_12 - data home
        self.ui.btn_home_12.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_edit_patients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(27))
        self.ui.btn_edit_ingredients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(13))
        self.ui.btn_edit_nutrients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(20))
        self.ui.btn_edit_diseases_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(24))
        #page_13 - data ingredient home
        self.ui.btn_data_home_13.clicked.connect(self.go_to_data_home)
        self.ui.btn_home_13.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_register_new_ing_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(15))
        self.ui.btn_edit_existing_ing_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(14))
        self.ui.btn_edit_gasung_allergy_ing_list_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(18))
        self.ui.btn_edit_common_unrec_ing_list_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(19))
        #page_14 - find existing ingredient to look up/edit


    #############################
    # NAVIGATION - Go
    #############################
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

    def go_to_previous_page(self, currPage):
        self.ui.stackedWidget.setCurrentIndex(currPage - 1)

    def go_to_next_page(self, currPage):
        self.ui.stackedWidget.setCurrentIndex(currPage + 1)

    def go_to_home_no_warning(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_patient(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_find_existing_patient(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def go_back_to_register_new_patient_page1(self):
        self.currPatientDiseaseIndexSet = build_disease_index_set_from_lw(self.ui.listWidget_diseases_4)
        self.currPatientGSIngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_gs_4)
        self.currPatientMSIngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_ms_4)
        self.currPatientLGG4IngTupleSet = build_allergy_index_level_tuple_set_from_tw(self.ui.tableWidget_allergies_lgg4_4)
        self.ui.stackedWidget.setCurrentIndex(3)

    def go_back_to_edit_existing_patient_page1(self):
        self.go_to_edit_patient_basic_info(self.ui.lineEdit_ID_7.text())

    def go_back_to_edit_existing_patient_page2(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def go_to_register_new_patient_page2(self):
        tempID = self.ui.lineEdit_ID_3.text()
        tempName = self.ui.lineEdit_name_3.text()

        if not tempID or not tempName:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("ID, 이름, 생년월일은 필수입니다.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()
        else:
            self.ui.stackedWidget.setCurrentIndex(4)
            if self.currPatientDiseaseIndexSet and \
                    self.currPatientGSIngTupleSet and \
                    self.currPatientMSIngTupleSet and \
                    self.currPatientLGG4IngTupleSet:
                populate_checkbox_lw(self.ui.listWidget_diseases_4, Disease.objects, "식품명")
                update_checkbox_state_lw(self.ui.listWidget_diseases_4, Disease.objects, "식품명", set())
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

    def go_to_data_home(self):
        self.ui.stackedWidget.setCurrentIndex(12)

    #############################
    # Page 1 - find patient
    #############################
    def find_patients_by_name(self, name):
        if not name:
            found_patients = Patient.objects.all()
        else:
            found_patients = Patient.objects(이름=name)
        self.render_found_patients(found_patients)

    def find_patients_by_id(self, id):
        if not id:
            found_patients = Patient.objects.all()
        else:
            found_patients = Patient.objects.get(ID=id)
        self.render_found_patients(found_patients)

    def render_found_patients(self, found_patients):
        self.ui.tableWidget_clientCandidates_5.setRowCount(found_patients.count())
        i=0
        for patient in found_patients:
            self.ui.tableWidget_clientCandidates_5.setItem(i, 0, make_tw_checkbox_item(patient.ID, False))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 1, make_tw_str_item(patient.이름))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 2, make_tw_str_item(patient.생년월일.strftime('%Y/%m/%d')))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 3, make_tw_str_item(patient.주소))
            i += 1

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
        msgbox.setText("현재 페이지 정보가 저장되지 않습니다. 계속하시겠습니까?")
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

    def logout(self):
        self.ui.stackedWidget.setCurrentIndex(0)


    #############################
    # TODO - NEED TO WORK ON DATA PAGE
    #############################
    def updatePatients(self):
        # for patient in getAllPatients():
        #     self.tableWidget_clientCandidates_5.
        #     patient.
        pass

    def go_to_data(self):
        self.ui.stackedWidget.setCurrentIndex(12)

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

    def get_selected_patient_id(self):
        for patient_idx in range(self.ui.tableWidget_clientCandidates_5.rowCount()):
            if self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).checkState() == QtCore.Qt.Checked:
                return self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).text()
        return None

    def go_to_edit_patient_basic_info(self, id):
        selected_patient_id = self.get_selected_patient_id()
        self.clear_find_existing_client()
        self.ui.stackedWidget.setCurrentIndex(6)
        if selected_patient_id:
            # First time a current patient info is stored locally.
            self.current_patient = Patient.objects.get(ID=selected_patient_id)
            self.ui.lineEdit_ID_6.setText(self.current_patient.ID)
            self.ui.lineEdit_name_6.setText(self.current_patient.이름)
            if self.current_patient.성별 == "남":
                self.ui.radioBtn_male_6.setChecked(True)
                self.ui.radioBtn_female_6.setChecked(False)
            else:
                self.ui.radioBtn_male_6.setChecked(False)
                self.ui.radioBtn_female_6.setChecked(True)
            self.ui.dateEdit_birthdate_6.setDate(QtCore.QDate(self.current_patient.생년월일))
            self.ui.lineEdit_address_6.setText(self.current_patient.주소)
            self.ui.lineEdit_height_6.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_6.setText(str(self.current_patient.몸무게))
            self.ui.ckBox_preg_6.setChecked(True) if self.current_patient.임신여부 == True else self.ui.ckBox_preg_6.setChecked(False)
            self.ui.ckBox_bFeeding_6.setChecked(True) if self.current_patient.수유여부 == True else self.ui.ckBox_bFeeding_6.setChecked(False)
            self.ui.dateEdit_lastOfficeVisit_6.setDate(QtCore.QDate(datetime.date.today()))

    def save_and_go_to_nutrients_edit_page(self, id):
        self.update_selected_disease_and_allergies()
        self.go_to_nutrients_edit_page(id)

    def go_to_nutrients_edit_page(self, id):
        self.ui.stackedWidget.setCurrentIndex(8)
        self.render_nutrient_edit_page_content(id)

    def render_nutrient_edit_page_content(self, id):
        # patient information
        patient = Patient.objects.get(ID=id)
        self.ui.lineEdit_name_8.setText(self.current_patient.이름)
        self.ui.lineEdit_ID_8.setText(self.current_patient.ID)
        self.ui.lineEdit_birthdate_8.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
        self.ui.lineEdit_age_8.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
        self.ui.lineEdit_lastOfficeVisit_8.setText(str(datetime.date.today()))
        self.ui.lineEdit_height_8.setText(str(self.current_patient.키))
        self.ui.lineEdit_weight_8.setText(str(self.current_patient.몸무게))
        self.ui.lineEdit_nthVisit_8.setText(str(self.current_patient.방문횟수 + 1))

        # nutrient information
        populate_checkbox_lw(self.ui.listWidget_nutrients_8, Nutrient.objects, "영양소명")
        update_checkbox_state_lw(self.ui.listWidget_nutrients_8, Nutrient.objects, "영양소명", set())

    def go_to_select_disease_and_allergies(self, id):
        if id == None:
            create_warning_message("진료할 회원을 선택해주세요.")
        else:
            self.ui.stackedWidget.setCurrentIndex(7)
            self.populate_existing_patient_detail(self.get_selected_patient_id())

    def populate_existing_patient_detail(self, id):
        self.current_patient = Patient.objects.get(ID=id)
        self.ui.lineEdit_name_7.setText(self.current_patient.이름)
        self.ui.lineEdit_ID_7.setText(self.current_patient.ID)
        self.ui.lineEdit_birthdate_7.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
        self.ui.lineEdit_age_7.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
        self.ui.lineEdit_lastOfficeVisit_7.setText(str(datetime.date.today()))
        self.ui.lineEdit_height_7.setText(str(self.current_patient.키))
        self.ui.lineEdit_weight_7.setText(str(self.current_patient.몸무게))
        self.ui.lineEdit_nthVisit_7.setText(str(self.current_patient.방문횟수 + 1))

        latest_date = str(self.current_patient.진료일[-1]).split()[0]

        populate_checkbox_lw(self.ui.listWidget_diseases_7, Disease.objects, "질병명")
        create_checkbox_level_tw(get_ingredients_guepsung(), self.ui.tableWidget_allergies_gs_7, "식품명", False, self.current_patient.급성알레르기음식[latest_date])
        create_checkbox_level_tw(get_ingredients_mansung(), self.ui.tableWidget_allergies_ms_7, "식품명", False, self.current_patient.만성알레르기음식[latest_date])
        create_checkbox_level_tw(get_ingredients_mansung_lgg4(), self.ui.tableWidget_allergies_lgg4_7, "식품명", False, self.current_patient.만성lgG4과민반응음식[latest_date])
        update_checkbox_state_lw(self.ui.listWidget_diseases_7, Disease.objects, "질병명", self.current_patient.진단[latest_date])

    def update_patient_basic_info(self, patient_id):
        id = self.ui.lineEdit_ID_6.text()
        name = self.ui.lineEdit_name_6.text()
        sex = "남" if self.ui.radioBtn_male_6.isChecked else "여"
        birthdate = self.ui.dateEdit_birthdate_6.date().toString(format=QtCore.Qt.ISODate)
        address = self.ui.lineEdit_address_6.text()
        if self.ui.lineEdit_height_6.text():
            height = float(self.ui.lineEdit_height_6.text())
        else:
            height = None
        if self.ui.lineEdit_weight_6.text():
            weight = float(self.ui.lineEdit_weight_6.text())
        else:
            weight = None
        isPreg = True if self.ui.ckBox_preg_6.isChecked() else False
        isBFeeding = True if self.ui.ckBox_bFeeding_6.isChecked() else False
        update_patient_basic_info(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding)

    def update_selected_disease_and_allergies(self):
        self.local_급성알레르기음식 = convert_lw_to_str_list(self.ui.listWidget_diseases_7)
        self.local_만성알레르기음식 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_gs_7)
        self.local_만성lgG4과민반응음식 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_ms_7)
        self.local_진단 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_lgg4_7)

    def register_client(self):
        if len(self.ui.lineEdit_ID_3.text()) == 0 or len(self.ui.lineEdit_name_3.text()) == 0:
            create_warning_message("ID, 이름, 생년월일은 필수입니다.")
        else:
            id = self.ui.lineEdit_ID_3.text()
            name = self.ui.lineEdit_name_3.text()
            new_patient = Patient()
            new_patient.ID = id
            new_patient.이름 = name
            new_patient.성별 = "남" if self.ui.radioBtn_male_3.isChecked else "여"
            new_patient.생년월일 = convert_DateEditWidget_to_string(self.ui.dateEdit_birthdate_3)
            new_patient.주소 = self.ui.lineEdit_address_3.text()
            진단 = {convert_DateEditWidget_to_string(self.ui.dateEdit_lastOfficeVisit_3) : convert_lw_to_str_list(self.ui.listWidget_diseases_4)}
            new_patient.진료 = 진단
            new_patient.방문횟수 = 1
            new_patient.키 = float(self.ui.lineEdit_height_3.text()) if self.ui.lineEdit_height_3.text() else 0
            new_patient.몸무게 = float(self.ui.lineEdit_weight_3.text()) if self.ui.lineEdit_weight_3.text() else 0
            new_patient.임신여부 = True if self.ui.ckBox_preg_3.isChecked() else False
            new_patient.수유여부 = True if self.ui.ckBox_bFeeding_3.isChecked() else False
            new_patient.급성알레르기음식 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_gs_4)
            new_patient.만성알레르기음식 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_ms_4)
            new_patient.만성lgG4과민반응음식 = convert_tw_to_tuple_list(self.ui.tableWidget_allergies_lgg4_4)
            new_patient.save()
            self.current_patient = new_patient

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
            idFound = Patient.objects.get(ID=idCand)
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

    def save_local_data_to_patient(self, patient):
        patient.급성알레르기음식[self.current_date] = self.local_급성알레르기음식
        patient.만성알레르기음식[self.current_date] = self.local_만성알레르기음식
        patient.만성lgG4과민반응음식[self.current_date] = self.local_만성lgG4과민반응음식
        patient.진단[self.current_date] = self.local_진단
        patient.save()

    def reset_local_data(self):
        self.current_patient = None
        self.local_급성알레르기음식 = None
        self.local_만성알레르기음식 = None
        self.local_만성lgG4과민반응음식 = None
        self.local_진단 = None

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyFoodRecommender()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
