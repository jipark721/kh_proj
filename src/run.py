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
        # page_4_1
        self.ui.btn_checkUniqID_3.clicked.connect(self.checkUniqID)
        # page 4_1_1
        self.ui.btn_registerClient_4.clicked.connect(self.registerClient)
        # page_5
        self.ui.btn_findbyID_5.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_5.text()))
        self.ui.btn_findbyName_5.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_5.text()))
        # self.ui.btn_
        self.ui.btn_confirmClient_5.clicked.connect(lambda x: self.populate_selected_patient())

        #save btn not update and next
        #self.ui.btn_save_6.clicked.connect(lambda x: self.update_exiting_patient_detail_data())
        self.ui.btn_save_6.clicked.connect(lambda x: self.populate_existing_patient_detail(self.ui.lineEdit_ID_6.text()))

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
            found_patients = get_patients_by_id(id)
        self.populate_found_patients(found_patients)

    def populate_found_patients(self, found_patients):
        self.ui.tableWidget_clientCandidates_5.setRowCount(found_patients.count())
        i=0
        for patient in found_patients:
            self.ui.tableWidget_clientCandidates_5.setItem(i, 0, make_tw_checkbox_item(patient['ID']))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 1, make_tw_str_item(patient['이름']))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 2, make_tw_str_item(patient['생년월일']))
            self.ui.tableWidget_clientCandidates_5.setItem(i, 3, make_tw_str_item(patient['주소']))
            i += 1

    def get_selected_patient(self):
        for patient_idx in range(self.ui.tableWidget_clientCandidates_5.rowCount()):
            if self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).checkState() == QtCore.Qt.Checked:
                return self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).text()
        return None

    def populate_selected_patient(self):
        self.ui.stackedWidget.setCurrentIndex(6)
        selected_patient_id = self.get_selected_patient()
        print(selected_patient_id)
        if selected_patient_id:
            patient = patients_collection.find_one({'ID': selected_patient_id})
            print(patient['ID'])
            self.ui.lineEdit_ID_6.setText(patient['ID'])
            self.ui.lineEdit_name_6.setText(patient['이름'])
            if patient['성별'] == "남":
                self.ui.radioBtn_male_6.setChecked(True)
                self.ui.radioBtn_female_6.setChecked(False)
            else:
                self.ui.radioBtn_male_6.setChecked(False)
                self.ui.radioBtn_female_6.setChecked(True)
            self.ui.lineEdit_address_6.setText(patient['주소'])
            self.ui.lineEdit_height_6.setText(str(patient['키']))
            self.ui.lineEdit_weight_6.setText(str(patient['몸무게']))
            self.ui.ckBox_preg_6.setChecked(True) if patient['임신여부'] == "T" else self.ui.ckBox_preg_6.setChecked(False)
            self.ui.ckBox_bFeeding_6.setChecked(True) if patient['수유여부'] == "T" else self.ui.ckBox_bFeeding_6.setChecked(False)

    def populate_existing_patient_detail(self, id):
        self.ui.stackedWidget.setCurrentIndex(7)
        patient = get_patients_by_id(id)
        self.ui.lineEdit_ID_7.setText(patient["ID"])
        self.ui.lineEdit_age_7.setText(patient["생년월일"]) # 나이!
        self.ui.lineEdit_height_7.setText(str(patient["키"]))
        self.ui.lineEdit_weight_7.setText(str(patient["몸무게"]))
        self.ui.lineEdit_name_7.setText(patient["이름"])

        # self.ui.listWidget_diseases_7
        # self.ui.tableWidget_allergies_gs_7
        # self.ui.tableWidget_allergies_lgg4_7
        # self.ui.tableWidget_allergies_ms_7

    def update_exiting_patient_detail_data(self):
        pass

    def registerClient(self):
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
                height = Decimal(float(self.ui.lineEdit_height_3.text()))
            else:
                height = 0
            if self.ui.lineEdit_weight_3.text():
                weight = Decimal(float(self.ui.lineEdit_weight_3.text()))
            else:
                weight = 0
            isPreg = "T" if self.ui.ckBox_preg_3.isChecked() else "F"
            isBFeeding = "T" if self.ui.ckBox_bFeeding_3.isChecked() else "F"
            officeVisitDateList = self.ui.dateEdit_lastOfficeVisit_3.date().toString(format=QtCore.Qt.ISODate)

            diagDiseasesStr = ""
            isFirstCheckedFound = False
            for i in range(self.ui.listWidget_diseases_4.count()):
                ckbtn = self.ui.listWidget_diseases_4.item(i)
                if ckbtn.checkState() == QtCore.Qt.Checked:
                    if not isFirstCheckedFound:
                        diagDiseasesStr = ckbtn.text()
                        isFirstCheckedFound = True
                    else:
                        diagDiseasesStr = diagDiseasesStr + ", " + ckbtn.text()

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
            patientObj['급성알레르기음식'] = self.convertAllergyTableWidget2Tuples(self.ui.tableWidget_allergies_gs_4)
            patientObj['만성알레르기음식'] = self.convertAllergyTableWidget2Tuples(self.ui.tableWidget_allergies_ms_4)
            patientObj['만성lgG4과민반응음식'] = self.convertAllergyTableWidget2Tuples(self.ui.tableWidget_allergies_lgg4_4)
            add_one_patient(patientObj)

    def convertAllergyTableWidget2Tuples(self, tw):
        list = []
        for index in range(tw.rowCount()):
            if int(tw.item(index, 1).text()) != 0:
                mytup = tuple([tw.item(index, 0).text(), int(tw.item(index, 1).text())])
                print(mytup[0], mytup[1])
                list.append(mytup)
        return list

    def checkUniqID(self):
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "비밀번호:"))
        self.btn_enter.setText(_translate("MainWindow", "Enter"))
        self.btn_go2Data.setText(_translate("MainWindow", "데이터 수정"))
        self.btn_go2Client.setText(_translate("MainWindow", "환자 보기"))
        self.btn_logout.setText(_translate("MainWindow", "로그아웃"))
        self.btn_registerNewClient.setText(_translate("MainWindow", "신규 회원 등록"))
        self.btn_findExistingClient.setText(_translate("MainWindow", "기존 회원 찾기"))
        self.label.setText(_translate("MainWindow", "환자 정보"))
        self.btn_home_3.setText(_translate("MainWindow", "HOME"))
        self.label_3.setText(_translate("MainWindow", "신규 회원 등록"))
        self.label_4.setText(_translate("MainWindow", "ID"))
        self.label_5.setText(_translate("MainWindow", "이름"))
        self.label_6.setText(_translate("MainWindow", "성별"))
        self.label_7.setText(_translate("MainWindow", "생년월일"))
        self.label_8.setText(_translate("MainWindow", "주소"))
        self.label_10.setText(_translate("MainWindow", "진료일"))
        self.label_11.setText(_translate("MainWindow", "키"))
        self.label_12.setText(_translate("MainWindow", "몸무게"))
        self.ckBox_preg_4_1.setText(_translate("MainWindow", "임신"))
        self.ckBox_bFeeding_4_1.setText(_translate("MainWindow", "수유"))
        self.radioBtn_female_4_1.setText(_translate("MainWindow", "여"))
        self.radioBtn_male_4_1.setText(_translate("MainWindow", "남"))
        self.dateEdit_birthdate_4_1.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.btn_home_4_1.setText(_translate("MainWindow", "HOME"))
        self.btn_cancel_4_1.setText(_translate("MainWindow", "취소"))
        self.btn_next_4_1.setText(_translate("MainWindow", "다음"))
        self.btn_checkUniqID.setText(_translate("MainWindow", "ID 사용가능?"))
        self.label_13.setText(_translate("MainWindow", "kg"))
        self.label_24.setText(_translate("MainWindow", "cm"))
        self.label_34.setText(_translate("MainWindow", "질병"))
        item = self.tableWidget_allergies_gs_4_1_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_gs_4_1_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        self.label_53.setText(_translate("MainWindow", "급성 알레르기 음식"))
        item = self.tableWidget_allergies_ms_4_1_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_ms_4_1_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        item = self.tableWidget_allergies_lgg4_4_1_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_lgg4_4_1_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        self.label_80.setText(_translate("MainWindow", "만성 알레르기 음식"))
        self.label_81.setText(_translate("MainWindow", "만성 알레르기 lgG4 음식 "))
        self.btn_cancel_4_1_1.setText(_translate("MainWindow", "취소"))
        self.btn_registerClient_4_1_1.setText(_translate("MainWindow", "등록"))
        self.label_38.setText(_translate("MainWindow", "기존회원 찾기 "))
        self.label_27.setText(_translate("MainWindow", "ID로 찾기"))
        self.btn_findbyID.setText(_translate("MainWindow", "찾기"))
        self.label_28.setText(_translate("MainWindow", "회원정보로 찾기"))
        self.label_29.setText(_translate("MainWindow", "생년월일"))
        self.label_30.setText(_translate("MainWindow", "이름"))
        self.btn_findbyName.setText(_translate("MainWindow", "찾기"))
        item = self.tableWidget_clientCandidates.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_clientCandidates.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "이름"))
        item = self.tableWidget_clientCandidates.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "생년월일"))
        item = self.tableWidget_clientCandidates.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "주소"))
        self.btn_home_4_2.setText(_translate("MainWindow", "HOME"))
        self.btn_cancel_4_2.setText(_translate("MainWindow", "취소"))
        self.btn_findClient.setText(_translate("MainWindow", "확인"))
        self.label_31.setText(_translate("MainWindow", "기존 회원 정보 보기/수정"))
        self.label_32.setText(_translate("MainWindow", "주소"))
        self.label_41.setText(_translate("MainWindow", "진료일"))
        self.radioBtn_female_4_3.setText(_translate("MainWindow", "여"))
        self.label_37.setText(_translate("MainWindow", "키"))
        self.radioBtn_male_4_3.setText(_translate("MainWindow", "남"))
        self.label_39.setText(_translate("MainWindow", "이름"))
        self.ckBox_preg_4_3.setText(_translate("MainWindow", "임신"))
        self.ckBox_bFeeding_4_3.setText(_translate("MainWindow", "수유"))
        self.label_40.setText(_translate("MainWindow", "생년월일"))
        self.label_36.setText(_translate("MainWindow", "ID"))
        self.label_35.setText(_translate("MainWindow", "몸무게"))
        self.label_42.setText(_translate("MainWindow", "성별"))
        self.btn_home_4_3.setText(_translate("MainWindow", "HOME"))
        self.btn_cancel_4_3.setText(_translate("MainWindow", "취소"))
        self.btn_update_next_4_3.setText(_translate("MainWindow", "수정 후 다음"))
        self.btn_not_update_next_4_4.setText(_translate("MainWindow", "수정 없이 다음"))
        self.label_56.setText(_translate("MainWindow", "cm"))
        self.label_79.setText(_translate("MainWindow", "kg"))
        self.label_14.setText(_translate("MainWindow", "이름"))
        self.label_15.setText(_translate("MainWindow", "ID"))
        self.label_16.setText(_translate("MainWindow", "생년월일 "))
        self.label_17.setText(_translate("MainWindow", "진료일"))
        self.label_18.setText(_translate("MainWindow", "번째 방문"))
        self.label_19.setText(_translate("MainWindow", "세"))
        self.label_20.setText(_translate("MainWindow", "몸무게"))
        self.label_21.setText(_translate("MainWindow", "키"))
        self.btn_back_5.setText(_translate("MainWindow", "뒤로"))
        self.btn_saveNext_5.setText(_translate("MainWindow", "저장 후 다음"))
        self.btn_home_5.setText(_translate("MainWindow", "HOME"))
        self.label_82.setText(_translate("MainWindow", "질병"))
        item = self.tableWidget_allergies_gs_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_gs_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        self.label_83.setText(_translate("MainWindow", "급성 알레르기 음식"))
        item = self.tableWidget_allergies_ms_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_ms_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        item = self.tableWidget_allergies_lgg4_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "식재료"))
        item = self.tableWidget_allergies_lgg4_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "알레르기 레벨"))
        self.label_84.setText(_translate("MainWindow", "만성 알레르기 음식"))
        self.label_85.setText(_translate("MainWindow", "만성 알레르기 lgG4 음식 "))
        self.label_25.setText(_translate("MainWindow", "이름"))
        self.label_26.setText(_translate("MainWindow", "ID"))
        self.label_43.setText(_translate("MainWindow", "생년월일 "))
        self.label_44.setText(_translate("MainWindow", "진료일"))
        self.label_45.setText(_translate("MainWindow", "번째 방문"))
        self.label_46.setText(_translate("MainWindow", "세"))
        self.label_47.setText(_translate("MainWindow", "몸무게"))
        self.label_48.setText(_translate("MainWindow", "키"))
        self.label_49.setText(_translate("MainWindow", "영양소"))
        item = self.tableWidget_RecNut.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "영양소"))
        item = self.tableWidget_RecNut.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "레벨"))
        item = self.tableWidget_NotRecNut.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "영양소"))
        item = self.tableWidget_NotRecNut.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "레벨"))
        self.label_50.setText(_translate("MainWindow", "권고 영양소"))
        self.label_51.setText(_translate("MainWindow", "주의 영양소"))
        self.btn_go2Rec.setText(_translate("MainWindow", "->"))
        self.btn_undo2Rec.setText(_translate("MainWindow", "<-"))
        self.btn_undo2NotRec.setText(_translate("MainWindow", "<-"))
        self.btn_go2NotRec.setText(_translate("MainWindow", "->"))
        self.label_52.setText(_translate("MainWindow", "Level"))
        self.radioBtn_lv1_6.setText(_translate("MainWindow", "1"))
        self.radioBtn_lv2_6.setText(_translate("MainWindow", "2"))
        self.radioBtn_lv3_6.setText(_translate("MainWindow", "3"))
        self.radioBtn_lv4_6.setText(_translate("MainWindow", "4"))
        self.radioBtn_lv5_6.setText(_translate("MainWindow", "5"))
        self.btn_back_6.setText(_translate("MainWindow", "뒤로"))
        self.btn_tempSave_6.setText(_translate("MainWindow", "임시저장"))
        self.btn_saveNext_6.setText(_translate("MainWindow", "저장 후 다음"))
        self.btn_home_6.setText(_translate("MainWindow", "HOME"))
        self.btn_home_7.setText(_translate("MainWindow", "HOME"))
        self.label_54.setText(_translate("MainWindow", "중복 제거:"))
        self.radioBtn_upper_auto2_8.setText(_translate("MainWindow", "자동"))
        self.radioBtn_upper_manual2_8.setText(_translate("MainWindow", "수동"))
        self.label_55.setText(_translate("MainWindow", "상위레벨 유지: "))
        self.radioBtn_dup_auto_8.setText(_translate("MainWindow", "자동"))
        self.radioBtn_dup_manual_8.setText(_translate("MainWindow", "수동"))
        self.label_58.setText(_translate("MainWindow", "출력대표성 등급:"))
        self.label_59.setText(_translate("MainWindow", "1회 분량당 출력조건:"))
        self.ckBox_100gFirst.setText(_translate("MainWindow", "100g당 많은 순서"))
        self.ckBox_onePortionFirst.setText(_translate("MainWindow", "1회분량 고려출력"))
        self.ckBox_mortalityFirst.setText(_translate("MainWindow", "폐기율 고려출력"))
        self.ckBox_proteinFirst.setText(_translate("MainWindow", "단백질가식부 고려출력"))
        self.label_60.setText(_translate("MainWindow", "등급 이하 출력"))
        self.label_61.setText(_translate("MainWindow", "가성알레르기 해당식품:"))
        self.label_62.setText(_translate("MainWindow", "급성알레르기 유발등급:"))
        self.label_63.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_65.setText(_translate("MainWindow", "만성알레르기 유발등급:"))
        self.label_66.setText(_translate("MainWindow", "만성lgG4 과민반응 유발등급:"))
        self.label_69.setText(_translate("MainWindow", "원산지:"))
        self.label_64.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_67.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_68.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_73.setText(_translate("MainWindow", "환자 지정 알레르기:"))
        self.label_74.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_75.setText(_translate("MainWindow", "등급 이상 제외"))
        self.label_76.setText(_translate("MainWindow", "멸종등급:"))
        self.toolButton_origin.setText(_translate("MainWindow", "..."))
        self.label_70.setText(_translate("MainWindow", "특산지:"))
        self.toolButton_localSpecialty.setText(_translate("MainWindow", "..."))
        self.pushButton_19.setText(_translate("MainWindow", "뒤로"))
        self.pushButton_20.setText(_translate("MainWindow", "다음"))
        self.btn_home_8.setText(_translate("MainWindow", "HOME"))
        self.label_71.setText(_translate("MainWindow", "식재료/성분 출력 언어표시:"))
        self.label_72.setText(_translate("MainWindow", "출력할 내용:"))
        self.ckBox_KoreanLang.setText(_translate("MainWindow", "한국어"))
        self.label_77.setText(_translate("MainWindow", "영양소 관련"))
        self.label_78.setText(_translate("MainWindow", "식재료 관련"))
        self.btn_home_9.setText(_translate("MainWindow", "HOME"))
        self.btn_back_9.setText(_translate("MainWindow", "뒤로"))
        self.btn_next_9.setText(_translate("MainWindow", "다음"))
        self.label_57.setText(_translate("MainWindow", "성분계산단위:"))
        self.radioBtn_RDA.setText(_translate("MainWindow", "하루 권장량 (RDA)"))
        self.radioButton_WHO.setText(_translate("MainWindow", "최대 권장량 (WHO)"))
        self.radioButton_MFDS.setText(_translate("MainWindow", "최대 권장량 (식약처)"))

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyFoodRecommender()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
