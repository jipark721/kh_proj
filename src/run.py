# -*- coding: utf-8 -*-

import sys
import operator
from mongoengine import *
from mongoengine.queryset.visitor import Q
from ui import Ui_MainWindow as UI
from mongodb.utils import *
from functions import *
from mongodb.models import *
from decimal import *
import math


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

        # local classes
        self.current_date = datetime.date.today()
        self.current_patient = None

        self.local_gs_allergic_ingredients = {}
        self.local_ms_allergic_ingredients = {}
        self.local_lgG4_allergic_ingredients = {}
        self.local_diseases = {}

        # local filters
        self.local_remove_duplicates = True
        self.local_rec_threshold = 0
        self.local_nonrec_threshold = 0
        self.local_gs_threshold = 0
        self.local_lgG4_threshold = 0
        self.local_ms_threshold = 0
        self.local_gasung_threshold = 0

        # edit
        self.local_disease_to_edit = None

        self.list_of_nut_cat = Nutrient.objects.distinct("영양소분류")
        self.list_of_nut_tw = [self.ui.tableWidget_nutrients1_4, self.ui.tableWidget_nutrients2_4,
                               self.ui.tableWidget_nutrients3_4, self.ui.tableWidget_nutrients4_4,
                               self.ui.tableWidget_nutrients5_4, self.ui.tableWidget_nutrients6_4,
                               self.ui.tableWidget_nutrients7_4, self.ui.tableWidget_nutrients8_4,
                               self.ui.tableWidget_nutrients9_4,
                               self.ui.tableWidget_nutrients1_29, self.ui.tableWidget_nutrients2_29,
                               self.ui.tableWidget_nutrients3_29, self.ui.tableWidget_nutrients4_29,
                               self.ui.tableWidget_nutrients5_29, self.ui.tableWidget_nutrients6_29,
                               self.ui.tableWidget_nutrients7_29]
        self.list_of_nut_lw = [self.ui.listWidget_nutrients1_23, self.ui.listWidget_nutrients2_23,
                               self.ui.listWidget_nutrients3_23, self.ui.listWidget_nutrients4_23,
                               self.ui.listWidget_nutrients5_23, self.ui.listWidget_nutrients6_23,
                               self.ui.listWidget_nutrients7_23, self.ui.listWidget_nutrients8_23,
                               self.ui.listWidget_nutrients1_24, self.ui.listWidget_nutrients2_24,
                               self.ui.listWidget_nutrients3_24, self.ui.listWidget_nutrients4_24,
                               self.ui.listWidget_nutrients5_24, self.ui.listWidget_nutrients6_24,
                               self.ui.listWidget_nutrients7_24, self.ui.listWidget_nutrients8_24]
        self.nut_level_src_dict = {} #nut - (level, src) dict
        self.rec_level_nut_dict = {}  # level - set of diseases dict
        self.unrec_level_nut_dict = {}
        self.current_ingredient = None
        self.current_nutrient = None
        self.current_disease = None
        self.lang_to_print = ['영어', '중국어', '일본어', '러시아어', '몽골어', '아랍어', '스페인어', '외국어8', '외국어9', '외국어10', '외국어11']
        self.nut_info_to_print = []

        self.setupLogic()

    def setupLogic(self):
        # page_0
        self.ui.btn_enter_0.clicked.connect(self.check_password)
        self.ui.btn_quit_app_0.clicked.connect(lambda x: self.close())
        # page_1 - home
        self.ui.btn_goToPatient_1.clicked.connect(self.go_to_patient)
        self.ui.btn_goToData_1.clicked.connect(self.go_to_data)
        self.ui.btn_logout_1.clicked.connect(self.logout)

        # page_2 - select patient type
        self.ui.btn_findExistingPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.btn_registerNewPatient_2.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.btn_home_2.clicked.connect(self.go_to_home_no_warning)

        # page_3 - register new patient
        self.ui.btn_home_3.clicked.connect(lambda x: self.go_home(3))
        self.ui.btn_cancel_3.clicked.connect(self.cancel_register_new_patient)
        self.ui.btn_next_3.clicked.connect(self.register_patient_and_go_to_select_diseases_and_allergies)
        self.ui.btn_checkUniqID_3.clicked.connect(self.check_unique_ID)

        # page_5 - find existing patient
        self.ui.btn_cancel_5.clicked.connect(self.cancel_find_existing_client)
        self.ui.btn_home_5.clicked.connect(lambda x: self.go_home(5))
        self.ui.btn_findbyID_5.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_5.text(), self.ui.tableWidget_clientCandidates_5))
        self.ui.btn_findbyName_5.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_5.text(), self.ui.tableWidget_clientCandidates_5))
        self.ui.btn_confirmClient_5.clicked.connect(
            lambda x: self.go_to_select_disease_and_allergies(
                get_first_checked_btn_text_in_tw(self.ui.tableWidget_clientCandidates_5)))

        # page_6 - patient information view/edit
        # self.ui.btn_home_6.clicked.connect(lambda x: self.go_home(6))
        # self.ui.btn_cancel_6.clicked.connect(self.cancel_edit_existing_patient)
        # self.ui.btn_save_6.clicked.connect(lambda x: self.update_edit_existing_patient_data_page1())
        # self.ui.btn_save_next_6.clicked.connect(lambda x: self.go_to_edit_existing_patient_page2(self.ui.lineEdit_ID_6.text()))

        # page_7 - patient information (diseases / allergies)
        self.ui.btn_back_7.clicked.connect(self.go_back_to_patient_selection)
        self.ui.btn_next_7.clicked.connect(lambda x: self.go_to_page_8(7))
        self.ui.btn_home_7.clicked.connect(lambda x: self.go_to_pageN_with_warning_before_exiting(1))

        # page 8 - filtering page
        self.ui.btn_back_8.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(7))
        self.ui.btn_next_8.clicked.connect(self.go_to_page_4)

        # page_4
        self.ui.btn_home_4.clicked.connect(lambda x: self.go_home(4))
        self.ui.btn_next_4.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(29))
        self.ui.btn_back_4.clicked.connect(lambda x: self.go_to_page_8(4))
        # page_29
        self.ui.btn_home_29.clicked.connect(lambda x: self.go_home(29))
        self.ui.btn_back_29.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.btn_next_29.clicked.connect(lambda x: self.go_to_page_9())
        self.ui.btn_go_to_rec_29.clicked.connect(lambda x: self.put_selected_nutrients_to_tw(self.ui.tableWidget_nutrients_rec_29, True))
        self.ui.btn_undo_go_to_rec_29.clicked.connect(lambda x: self.take_out_selected_nutrients_from_tw(self.ui.tableWidget_nutrients_rec_29, True))
        self.ui.btn_go_to_unrec_29.clicked.connect(lambda x: self.put_selected_nutrients_to_tw(self.ui.tableWidget_nutrients_unrec_29, False))
        self.ui.btn_undo_go_to_unrec_29.clicked.connect(lambda x: self.take_out_selected_nutrients_from_tw(self.ui.tableWidget_nutrients_unrec_29, False))
        # page_9 - get rec/unrec ingredients page
        self.ui.btn_back_9.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.btn_next_9.clicked.connect(lambda x: self.go_to_page_10(9))
        self.ui.btn_check_duplicate_ing_9.clicked.connect(self.highlight_duplicate_ingredients)
        self.ui.btn_render_rec_unrec_ing_from_nut_9.clicked.connect(self.render_rec_unrec_ing_from_nut)
        self.ui.btn_delete_selected_9.clicked.connect(self.remove_selected_items_tws)
        # page 10 - see current collapsed rec/unrec ingredients page
        self.ui.btn_home_10.clicked.connect(lambda x: self.go_home(10))
        self.ui.btn_back_10.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(9))
        self.ui.btn_next_10.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(11))
        # page 11 - print-filtering page2
        # self.ui.btn_PRINT_11.clicked.connect()

        # page_12 - data home
        self.ui.btn_home_12.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_edit_patients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(28))
        self.ui.btn_edit_ingredients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(13))
        self.ui.btn_edit_nutrients_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(20))
        self.ui.btn_edit_diseases_data_12.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(25))
        # page_13 - data ingredient home
        self.ui.btn_home_13.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_data_home_13.clicked.connect(self.go_to_data_home_with_no_warning)
        self.ui.btn_register_new_ing_13.clicked.connect(lambda x: self.go_to_register_or_edit_ingredient_info(None))
        self.ui.btn_edit_existing_ing_13.clicked.connect(lambda x: self.go_to_find_existing_ingredient_for_editing())
        self.ui.btn_edit_gasung_allergy_ing_list_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(18))
        self.ui.btn_edit_common_unrec_ing_list_13.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(19))
        # page_14 - find existing ingredient to look up/edit
        self.ui.btn_home_14.clicked.connect(lambda x: self.go_home(14))
        self.ui.btn_data_home_14.clicked.connect(lambda x: self.go_to_data_home(14))
        self.ui.btn_findby_ing_name_14.clicked.connect(
            lambda x: self.find_ingredients_by_name(self.ui.lineEdit_ing_name_14.text()))
        self.ui.btn_findby_ing_category_14.clicked.connect(lambda x: self.find_ingredients_by_category())
        self.ui.btn_cancel_14.clicked.connect(lambda x: self.cancel_find_existing_ingredient())
        self.ui.btn_confirm_ing_14.clicked.connect(lambda x: self.go_to_register_or_edit_ingredient_info(
            get_first_checked_btn_text_in_tw(self.ui.tableWidget_ing_candidates_14)))
        # page_15 - register/edit ingredient
        self.ui.btn_home_15.clicked.connect(lambda x: self.go_home(15))
        self.ui.btn_data_home_15.clicked.connect(lambda x: self.go_to_data_home(15))
        self.ui.btn_check_uniq_ing_name_15.clicked.connect(lambda x: self.check_unique_ing_name(self.ui.lineEdit_ing_name_15))
        self.ui.btn_cancel_15.clicked.connect(lambda x: self.cancel_edit_existing_ingredient())
        self.ui.btn_next_15.clicked.connect(lambda x: self.go_to_register_or_edit_ingredient_info_page2())
        #page_16 - register/edit ingredient page 2, adding ing-nut relationship
        self.ui.btn_home_16.clicked.connect(lambda x: self.go_home(16))
        self.ui.btn_data_home_16.clicked.connect(lambda x: self.go_to_data_home(16))
        self.ui.btn_show_popup_nut_16.clicked.connect(lambda x: self.show_popup_nut_for_ing_nut_rel())
        self.ui.btn_findby_nut_name_16.clicked.connect(lambda x: self.find_nutrients_by_name(self.ui.lineEdit_nut_name_16.text(), self.ui.tableWidget_nutCandidates_16))
        self.ui.btn_findby_nut_category_16.clicked.connect(lambda x: self.find_nutrients_by_category(self.ui.comboBox_nut_category1_16, self.ui.tableWidget_nutCandidates_16))
        self.ui.btn_add_nut_16.clicked.connect(lambda x: self.add_selected_nutrients_to_tw_and_clear_and_hide_popup())
        self.ui.btn_delete_selected_nut_16.clicked.connect(lambda x: self.remove_selected_nutrients_from_tw(self.ui.tableWidget_nut_quant_16))
        self.ui.btn_back_16.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(15))
        self.ui.btn_cancel_16.clicked.connect(lambda x: self.cancel_edit_existing_ingredient())
        self.ui.btn_save_16.clicked.connect(lambda x: self.save_or_update_ingredient())
        # page_20 - data nutrient home
        self.ui.btn_home_20.clicked.connect(self.go_to_home_no_warning)
        self.ui.btn_data_home_20.clicked.connect(self.go_to_data_home_with_no_warning)
        self.ui.btn_register_new_nut_20.clicked.connect(lambda x: self.go_to_register_or_edit_nutrient_info(None))
        self.ui.btn_edit_existing_nut_20.clicked.connect(lambda x: self.go_to_find_existing_nutrient_for_editing())
        self.ui.btn_edit_nut_category_20.clicked.connect(lambda x: self.go_to_edit_nut_category())
        # page_21 find existing nutrient for editing
        self.ui.btn_findby_nut_name_21.clicked.connect(
            lambda x: self.find_nutrients_by_name(self.ui.lineEdit_nut_name_21.text(), self.ui.tableWidget_nutCandidates_21))
        self.ui.btn_findby_nut_category_21.clicked.connect(lambda x: self.find_nutrients_by_category(self.ui.comboBox_nut_category1_21, self.ui.tableWidget_nutCandidates_21))
        self.ui.btn_cancel_21.clicked.connect(lambda x: self.cancel_find_existing_nutrient())
        self.ui.btn_confirm_nut_21.clicked.connect(lambda x: self.go_to_register_or_edit_nutrient_info(
            get_first_checked_btn_text_in_tw(self.ui.tableWidget_nutCandidates_21)))
        #page_22
        self.ui.btn_check_uniq_nut_name_22.clicked.connect(lambda x: self.check_unique_nut_name(self.ui.lineEdit_nut_name_22))
        # page_23
        self.ui.btn_next_23.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(24))
        self.ui.btn_update_cat1_23.clicked.connect(lambda x: self.update_nutrient_column_i(1, self.ui.lineEdit_cat1_23))
        self.ui.btn_update_cat2_23.clicked.connect(lambda x: self.update_nutrient_column_i(2, self.ui.lineEdit_cat2_23))
        self.ui.btn_update_cat3_23.clicked.connect(lambda x: self.update_nutrient_column_i(3, self.ui.lineEdit_cat3_23))
        self.ui.btn_update_cat4_23.clicked.connect(lambda x: self.update_nutrient_column_i(4, self.ui.lineEdit_cat4_23))
        self.ui.btn_update_cat5_23.clicked.connect(lambda x: self.update_nutrient_column_i(5, self.ui.lineEdit_cat5_23))
        self.ui.btn_update_cat6_23.clicked.connect(lambda x: self.update_nutrient_column_i(6, self.ui.lineEdit_cat6_23))
        self.ui.btn_update_cat7_23.clicked.connect(lambda x: self.update_nutrient_column_i(7, self.ui.lineEdit_cat7_23))
        self.ui.btn_update_cat8_23.clicked.connect(lambda x: self.update_nutrient_column_i(8, self.ui.lineEdit_cat8_23))
        # page_24
        self.ui.btn_back_24.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(23))
        self.ui.btn_update_cat1_24.clicked.connect(lambda x: self.update_nutrient_column_i(1, self.ui.lineEdit_cat1_24))
        self.ui.btn_update_cat2_24.clicked.connect(lambda x: self.update_nutrient_column_i(2, self.ui.lineEdit_cat2_24))
        self.ui.btn_update_cat3_24.clicked.connect(lambda x: self.update_nutrient_column_i(3, self.ui.lineEdit_cat3_24))
        self.ui.btn_update_cat4_24.clicked.connect(lambda x: self.update_nutrient_column_i(4, self.ui.lineEdit_cat4_24))
        self.ui.btn_update_cat5_24.clicked.connect(lambda x: self.update_nutrient_column_i(5, self.ui.lineEdit_cat5_24))
        self.ui.btn_update_cat6_24.clicked.connect(lambda x: self.update_nutrient_column_i(6, self.ui.lineEdit_cat6_24))
        self.ui.btn_update_cat7_24.clicked.connect(lambda x: self.update_nutrient_column_i(7, self.ui.lineEdit_cat7_24))
        self.ui.btn_update_cat8_24.clicked.connect(lambda x: self.update_nutrient_column_i(8, self.ui.lineEdit_cat8_24))
        #page_28 find existing patient for edit
        self.ui.btn_cancel_28.clicked.connect(self.cancel_find_existing_client)
        self.ui.btn_findby_patient_id_28.clicked.connect(lambda x: self.find_patients_by_id(self.ui.lineEdit_ID_28.text(), self.ui.tableWidget_patientCandidates_28))
        self.ui.btn_findby_patient_name_28.clicked.connect(lambda x: self.find_patients_by_name(self.ui.lineEdit_name_28.text(), self.ui.tableWidget_patientCandidates_28))
        self.ui.btn_confirmPatient_28.clicked.connect(
            lambda x: self.go_to_edit_patient_basic_info(
                get_first_checked_btn_text_in_tw(self.ui.tableWidget_patientCandidates_28)))

        #page_6 edit_patient_basic_info
        self.ui.btn_cancel_6.clicked.connect(lambda x: self.go_to_pageN_with_warning_before_exiting(28))
        self.ui.btn_save_6.clicked.connect(self.update_patient_basic_info)

        #page_25 add or edit disease
        self.ui.btn_edit_existing_dis_25.clicked.connect(lambda x: self.go_to_pageN(26))
        self.ui.btn_register_new_dis_25.clicked.connect(lambda x: self.go_to_pageN(27))

        #page_26 add new disease
        # self.ui.btn_lookup_ing_27.clicked.connect(self.popup_ing_table_for_disease_edit)
        # self.ui.btn_lookup_nut_27.clicked.connect(self.popup_nut_table_for_disease_edit)

        #page_27 edit existing disease
        self.ui.btn_findby_dis_name_26.clicked.connect(self.find_existing_disease_for_edit)
        self.ui.btn_confirm_dis_26.clicked.connect(self.go_to_edit_disease)

    def cancel_find_existing_nutrient(self):
        self.clear_find_existing_nutrient()
        self.ui.stackedWidget.setCurrentIndex(20)

    ####################
    # GO TO
    ####################
    def go_to_edit_nut_category(self):
        self.ui.stackedWidget.setCurrentIndex(23)
        self.render_edit_nut_category()

    def update_nutrient_column_i(self, i, lineedit):
        i = i -1
        curr_lw = self.list_of_nut_lw[i]
        if curr_lw.count() > 0:
            old_nut_cat = Nutrient.objects.get(영양소명 = curr_lw.item(0).text()).영양소분류
            new_nut_cat = lineedit.text()
            if old_nut_cat != new_nut_cat:
                for i in range(curr_lw.count()):
                    nut_str = curr_lw.item(i).text()
                    Nutrient.objects.get(영양소명=nut_str).update(영양소분류 = new_nut_cat)
                create_normal_message("영양소분류가 정상적으로 업데이트되었습니다.")
                self.list_of_nut_cat = Nutrient.objects.distinct("영양소분류")

    def render_edit_nut_category(self):
        list_of_nut_cat_lineedit = [self.ui.lineEdit_cat1_23, self.ui.lineEdit_cat2_23, self.ui.lineEdit_cat3_23,
                                    self.ui.lineEdit_cat4_23, self.ui.lineEdit_cat5_23, self.ui.lineEdit_cat6_23,
                                    self.ui.lineEdit_cat7_23, self.ui.lineEdit_cat8_23,
                                    self.ui.lineEdit_cat1_24, self.ui.lineEdit_cat2_24, self.ui.lineEdit_cat3_24,
                                    self.ui.lineEdit_cat4_24, self.ui.lineEdit_cat5_24, self.ui.lineEdit_cat6_24,
                                    self.ui.lineEdit_cat7_24, self.ui.lineEdit_cat8_23]
        for i in range(len(self.list_of_nut_cat)):
            nut_cat = self.list_of_nut_cat[i]
            list_of_nut_cat_lineedit[i].setText(nut_cat)
            for nutrient in Nutrient.objects(영양소분류=nut_cat):
                nut_item = make_lw_str_item(nutrient.영양소명)
                self.list_of_nut_lw[i].addItem(nut_item)


    def put_selected_nutrients_to_tw(self, rec_or_unrec_tw, isRec):
        lv = self.get_level_page29()
        if not isRec:
            lv = lv * (-1)
        for i in range(len(self.list_of_nut_cat)):
            nut_tw = self.list_of_nut_tw[i]
            for rowIndex in range(nut_tw.rowCount()):
                if nut_tw.item(rowIndex, 0).checkState() == QtCore.Qt.Checked:
                    nut_str = nut_tw.item(rowIndex, 1).text()
                    if nut_str in self.nut_level_src_dict: #if nut_str already in either rec_tw or unrec_tw
                        old_level, old_source = self.nut_level_src_dict[nut_str]
                        found_index = find_item_index_for_str_in_tw(rec_or_unrec_tw, nut_str, 0)

                        if (isRec and lv > old_level) or (not isRec and lv < old_level):
                            new_source = "User Input"
                            self.nut_level_src_dict[nut_str] = (lv, new_source)
                            rec_or_unrec_tw.item(found_index, 1).setText(str(lv))
                            rec_or_unrec_tw.item(found_index, 2).setText(new_source)
                    else: #nut_str not in rec_tw nor unrec_tw
                        source = "User Input"
                        self.nut_level_src_dict[nut_str] = (lv, source)
                        rec_or_unrec_tw_rowIndex = rec_or_unrec_tw.rowCount()
                        rec_or_unrec_tw.insertRow(rec_or_unrec_tw_rowIndex)
                        nut_item = make_tw_checkbox_item(nut_str, False)
                        level_item = make_tw_str_item(str(lv))
                        src_item = make_tw_str_item(source)
                        rec_or_unrec_tw.setItem(rec_or_unrec_tw_rowIndex, 0, nut_item)
                        rec_or_unrec_tw.setItem(rec_or_unrec_tw_rowIndex, 1, level_item)
                        rec_or_unrec_tw.setItem(rec_or_unrec_tw_rowIndex, 2, src_item)

                        nut_tw.item(rowIndex, 1).setBackground(QtGui.QColor(135,206,250))
                    nut_tw.item(rowIndex, 0).setCheckState(QtCore.Qt.Unchecked)

    def take_out_selected_nutrients_from_tw(self, rec_or_unrec_tw, isRec):
        for rowIndex in range(rec_or_unrec_tw.rowCount(), -1, -1):
            if rec_or_unrec_tw.item(rowIndex, 0) and rec_or_unrec_tw.item(rowIndex, 0).checkState() == QtCore.Qt.Checked:
                nut_str = rec_or_unrec_tw.item(rowIndex, 0).text()
                del self.nut_level_src_dict[nut_str]
                rec_or_unrec_tw.removeRow(rowIndex)

                for i in range(len(self.list_of_nut_tw)):
                    nut_tw = self.list_of_nut_tw[i]
                    found_index = find_item_index_for_str_in_tw(nut_tw, nut_str, 1)
                    if found_index != -1:
                        nut_tw.item(found_index, 1).setBackground(QtGui.QColor(255,255,255))
                        break

    def go_to_page_4(self):
        self.local_remove_duplicates = True if self.ui.radioButton_dis_rel_ing_delete_both_8.isChecked() else False
        self.local_rec_threshold = int(self.ui.spinBox_dis_rel_ing_level_rec_8.text())
        self.local_nonrec_threshold = int(self.ui.spinBox_dis_rel_ing_level_unrec_8.text())
        self.local_gs_threshold = int(self.ui.spinBox_allergy_gs_level_8.text())
        self.local_lgG4_threshold = int(self.ui.spinBox_allergy_lgg4_level_8.text())
        self.local_ms_threshold = int(self.ui.spinBox_allergy_ms_level_8.text())
        self.local_gasung_threshold = int(self.ui.spinBox_allergy_gasung_level_8.text())
        self.ui.stackedWidget.setCurrentIndex(4)
        self.render_page_4_and_29()


    def go_to_page_9(self):
        self.ui.stackedWidget.setCurrentIndex(9)
        self.render_page_9()

    def go_to_page_10(self, currPage):
        self.build_ultimate_rec_ing_level_dict()

        self.ui.stackedWidget.setCurrentIndex(10)
        self.render_basic_patient_info_on_top(10)

    def build_ultimate_rec_ing_level_dict(self):
        rec_dict = convert_tw_to_dict(self.ui.tableWidget_rec_ing_from_nut_9, 1)
        rec_dict.update(convert_tw_to_dict(self.ui.tableWidget_rec_ing_from_dis_9, 1))

        unrec_dict = convert_tw_to_dict(self.ui.tableWidget_unrec_ing_from_nut_9, 1)
        unrec_dict.update(convert_tw_to_dict(self.ui.tableWidget_unrec_ing_from_dis_9, 1))
        unrec_dict.update(convert_tw_to_dict(self.ui.tableWidget_unrec_ing_from_allergies_9, 1))

        self.ui.tableWidget_current_rec_ing_10.setRowCount(len(rec_dict))
        self.ui.tableWidget_current_unrec_ing_10.setRowCount(len(unrec_dict))

        i = 0
        for rec_ingredient, lvl in rec_dict.items():
            ingredient = Ingredient.objects.get(식품명=rec_ingredient)
            self.make_rec_ingredient_tw_item(self.ui.tableWidget_current_rec_ing_10, i, ingredient, lvl)
            i+=1

        i = 0
        for unrec_ingredient, lvl in unrec_dict.items():
            ingredient = Ingredient.objects.get(식품명=unrec_ingredient)
            self.make_rec_ingredient_tw_item(self.ui.tableWidget_current_unrec_ing_10, i, ingredient, lvl)
            i+=1

    def make_rec_ingredient_tw_item(self, tw, rowIndex, ingredient, lvl):
        ingredient_item = QtWidgets.QTableWidgetItem(ingredient.식품명)
        level_item = QtWidgets.QTableWidgetItem(str(lvl))
        class_one = QtWidgets.QTableWidgetItem(ingredient.식품분류1)
        class_two = QtWidgets.QTableWidgetItem(ingredient.식품분류2)
        class_three = QtWidgets.QTableWidgetItem(ingredient.식품분류3)
        class_four = QtWidgets.QTableWidgetItem(ingredient.식품분류4)
        class_five = QtWidgets.QTableWidgetItem(ingredient.식품분류5)
        tw.setItem(rowIndex, 0, ingredient_item)
        tw.setItem(rowIndex, 1, level_item)
        tw.setItem(rowIndex, 2, class_one)
        tw.setItem(rowIndex, 3, class_two)
        tw.setItem(rowIndex, 4, class_three)
        tw.setItem(rowIndex, 5, class_four)
        tw.setItem(rowIndex, 6, class_five)


    def go_back_to_patient_selection(self):
        if self.warn_before_leaving() == False:
            return
        else:
            self.clear_current_patient_info_and_all_related_pages()
            self.ui.stackedWidget.setCurrentIndex(5)

    def go_to_register_or_edit_nutrient_info(self, nut_name):
        if nut_name is not None:
            self.clear_find_existing_nutrient()
        self.ui.stackedWidget.setCurrentIndex(22)
        self.ui.comboBox_nut_category1_22.addItem("")
        self.ui.comboBox_nut_category1_22.addItems(self.list_of_nut_cat)
        if nut_name is not None:  # if editing existing ingredient
            self.populate_existing_nutrient_info(nut_name)

    ####################
    # RENDER
    ####################
    def render_page_4_and_29(self):
        self.render_basic_patient_info_on_top(4)
        self.render_basic_patient_info_on_top(29)

        list_of_nut_cat_lineedit = [self.ui.lineEdit_cat1_4, self.ui.lineEdit_cat2_4, self.ui.lineEdit_cat3_4,
                                    self.ui.lineEdit_cat4_4, self.ui.lineEdit_cat5_4, self.ui.lineEdit_cat6_4,
                                    self.ui.lineEdit_cat7_4, self.ui.lineEdit_cat8_4, self.ui.lineEdit_cat9_4,
                                    self.ui.lineEdit_cat1_29, self.ui.lineEdit_cat2_29, self.ui.lineEdit_cat3_29,
                                    self.ui.lineEdit_cat4_29, self.ui.lineEdit_cat5_29, self.ui.lineEdit_cat6_29,
                                    self.ui.lineEdit_cat7_29]
        self.ui.tableWidget_nutrients_rec_29.setRowCount(0)
        self.ui.tableWidget_nutrients_unrec_29.setRowCount(0)
        for i in range(len(self.list_of_nut_cat)):
            nut_cat = self.list_of_nut_cat[i]
            list_of_nut_cat_lineedit[i].setText(nut_cat)
            render_rec_nutrient_tw(nut_cat, self.list_of_nut_tw[i], self.ui.tableWidget_nutrients_rec_29,
                                   self.ui.tableWidget_nutrients_unrec_29, self.local_diseases, False, self.nut_level_src_dict)
            self.ui.tableWidget_nutrients_rec_29.resizeColumnsToContents()
            self.ui.tableWidget_nutrients_unrec_29.resizeColumnsToContents()




    def render_page_9(self):
        self.render_basic_patient_info_on_top(9)

        # render relevant nutrient by disease
        # TODO : remove duplicates?
        self.render_all_selected_nutrients()

        # render rec/nonrec ingredients by disease
        render_checkbox_pos_and_neg_level_tw(self.ui.tableWidget_rec_ing_from_dis_9,
                                             self.ui.tableWidget_unrec_ing_from_dis_9,
                                             get_relevant_ingredients_from_diseases_str(self.local_diseases, self.local_remove_duplicates),
                                             self.local_rec_threshold, self.local_nonrec_threshold)

        # render nonrec ingredients by allergies
        render_checkbox_level_tw(self.ui.tableWidget_unrec_ing_from_allergies_9,
                                 self.get_relevant_ingred_from_all_allergies(self.local_gs_threshold, self.local_lgG4_threshold,
                                                                             self.local_ms_threshold, self.local_gasung_threshold),
                                 -1)

    def remove_selected_items_tws(self):
        self.remove_selected_items_tw(self.ui.tableWidget_rec_ing_from_nut_9)
        self.remove_selected_items_tw(self.ui.tableWidget_unrec_ing_from_nut_9)
        self.remove_selected_items_tw(self.ui.tableWidget_rec_ing_from_dis_9)
        self.remove_selected_items_tw(self.ui.tableWidget_unrec_ing_from_dis_9)
        self.remove_selected_items_tw(self.ui.tableWidget_unrec_ing_from_allergies_9)

    def remove_selected_items_tw(self, tw):
        for rowIndex in range(tw.rowCount(), -1, -1):
            if tw.item(rowIndex, 0) and tw.item(rowIndex, 0).checkState() == QtCore.Qt.Checked:
                tw.removeRow(rowIndex)

    def render_all_selected_nutrients(self):
        # rec_level_nut_dict = {}  # level - set of diseases dict
        # unrec_level_nut_dict = {}
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients1_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients2_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients3_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients4_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients5_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients6_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients7_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients8_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)
        self.build_rec_unrec_index_nut_dict(self.ui.tableWidget_nutrients9_4, self.rec_level_nut_dict, self.unrec_level_nut_dict)


        self.ui.tableWidget_nutrients_rec_9.setRowCount(1000)
        rowIndex = 0
        for level in reversed(range(1,6)):
            if level in self.rec_level_nut_dict:
                for nut_str in self.rec_level_nut_dict.get(level):
                    nut_item = make_tw_str_item(nut_str)
                    level_item = make_tw_str_item(str(level))
                    self.ui.tableWidget_nutrients_rec_9.setItem(rowIndex, 0, nut_item)
                    self.ui.tableWidget_nutrients_rec_9.setItem(rowIndex, 1, level_item)
                    rowIndex += 1
        self.ui.tableWidget_nutrients_rec_9.setRowCount(rowIndex)

        self.ui.tableWidget_nutrients_unrec_9.setRowCount(1000)
        unrec_rowIndex = 0
        for level in reversed(range(1,6)):
            level = level * (-1)
            if level in self.unrec_level_nut_dict:
                for nut_str in self.unrec_level_nut_dict.get(level):
                    nut_item = make_tw_str_item(nut_str)
                    level_item = make_tw_str_item(str(level))
                    self.ui.tableWidget_nutrients_unrec_9.setItem(unrec_rowIndex, 0, nut_item)
                    self.ui.tableWidget_nutrients_unrec_9.setItem(unrec_rowIndex, 1, level_item)
                    unrec_rowIndex += 1
        self.ui.tableWidget_nutrients_unrec_9.setRowCount(unrec_rowIndex)


    def render_rec_unrec_ing_from_nut(self):

        # TODO - gotta do something about this row count issue
        self.ui.tableWidget_rec_ing_from_nut_9.setRowCount(1000)
        self.ui.tableWidget_unrec_ing_from_nut_9.setRowCount(1000)

        self.render_tw_for_ing_from_nut(self.ui.tableWidget_rec_ing_from_nut_9, self.rec_level_nut_dict, True)
        self.render_tw_for_ing_from_nut(self.ui.tableWidget_unrec_ing_from_nut_9, self.unrec_level_nut_dict, False)

    def isOriginAndSpecialtyBothSatisfied(self, ing_str):
        origin, origin_level = self.get_most_specified_origin_and_level(8)
        specialty, specialty_level = self.get_most_specified_specialty_and_level(8)
        ing = Ingredient.objects.get(식품명 = ing_str)
        if origin_level != -1:
            if origin_level == 1 and ing.원산지분류1 != origin:
                return False
            elif origin_level == 2 and ing.원산지분류2 != origin:
                return False
            elif origin_level == 3 and ing.원산지분류3 != origin:
                return False
            elif origin_level == 4 and ing.원산지분류4 != origin:
                return False
            elif origin_level == 5 and ing.원산지분류5 != origin:
                return False
        if specialty_level != -1:
            if specialty_level == 1 and ing.특산지분류1 != specialty:
                return False
            elif specialty_level == 2 and ing.특산지분류2 != specialty:
                return False
            elif specialty_level == 3 and ing.특산지분류3 != specialty:
                return False
            elif specialty_level == 4 and ing.특산지분류4 != specialty:
                return False
            elif specialty_level == 5 and ing.특산지분류5 != specialty:
                return False
        return True

    def render_tw_for_ing_from_nut(self, tw, dict, isRec):
        # ints
        printing_rep_level = self.ui.spinBox_printingRep_level_8.value()
        extinction_level = self.ui.spinBox_extinction_level_8.value()

        # bools
        is_one_portion_first = self.ui.ckBox_onePortionFirst_8.isChecked()
        is_100g_first = self.ui.ckBox_100gFirst_8.isChecked()
        is_mortality_first = self.ui.ckBox_mortalityFirst_8.isChecked()
        is_protein_first = self.ui.ckBox_proteinFirst_8.isChecked()
        # 1 - one_portion_first clicked, 2 - 100g_first clicked, 4 - mortality_first clicked, 8 - protein_first clicked
        portion_code = get_portion_code(is_one_portion_first, is_100g_first, is_mortality_first, is_protein_first)

        rowIndex = 0
        ing_quant_list_for_nut_secondary = [] #list of (식품명, quant, level)
        for level in reversed(range(1, 6)):
            if not isRec:
                level = level * (-1) #reverse to negative
            if level in dict:
                for nut_str in dict.get(level):
                    ing_quant_dict_for_nut = {}
                    ing_quant_dict_for_nut_secondary = {}  # for 100g when both one-portion and 100g checked

                    ingredients_containing_nut = Nutrient.objects.get(영양소명 = nut_str).포함식품리스트.keys()
                    for ing_str in ingredients_containing_nut:
                        if self.isOriginAndSpecialtyBothSatisfied(ing_str) and \
                                        Ingredient.objects.get(식품명 = ing_str).출력대표성등급 <= printing_rep_level and \
                                        Ingredient.objects.get(식품명 = ing_str).멸종등급 > extinction_level:
                            ing_quant_dict_for_nut[ing_str] = self.calculate_nut_quant_for_ing(ing_str, nut_str,
                                                                                               portion_code, False)
                            if is_one_portion_first and is_100g_first: #1회식사와 100그램 중복 설정시 1회식사분량 먼저 표시후 100그램 표시
                                ing_quant_dict_for_nut_secondary[ing_str] = self.calculate_nut_quant_for_ing(ing_str, nut_str,
                                                                                                             portion_code, True)
                    min_count = self.get_level_count(level, ing_quant_dict_for_nut)
                    sorted_ing_quant_list = sorted(ing_quant_dict_for_nut.items(), key=operator.itemgetter(1),
                                                   reverse=True)[:min_count]

                    if is_one_portion_first and is_100g_first:
                        min_count2 = self.get_level_count(level, ing_quant_dict_for_nut_secondary)
                        sorted_ing_quant_list2 = sorted(ing_quant_dict_for_nut_secondary.items(), key=operator.itemgetter(1),
                                                       reverse=True)[:min_count2]
                        for item in sorted_ing_quant_list2:
                            ing_quant_list_for_nut_secondary.append((item[0], item[1], level, nut_str)) #(ing_str, quant, level, nut_str)
                    for index in range(min_count):
                        ing_name = sorted_ing_quant_list[index][0]
                        quant = sorted_ing_quant_list[index][1]
                        ing_name_item = make_tw_checkbox_item(ing_name, False)
                        level_item = make_tw_str_item(str(level))
                        nut_item = make_tw_str_item(nut_str)
                        quant_item = make_tw_str_item(str(quant))
                        tw.setItem(rowIndex, 0, ing_name_item)
                        tw.setItem(rowIndex, 1, level_item)
                        tw.setItem(rowIndex, 2, nut_item)
                        tw.setItem(rowIndex, 3, quant_item)
                        if is_one_portion_first and is_100g_first:
                            description_item = make_tw_str_item("1회식사분량 고려출력")
                            tw.setItem(rowIndex, 4, description_item)
                        rowIndex += 1

        if is_one_portion_first and is_100g_first:
            for (ing_str, quant, level, nut_str) in ing_quant_list_for_nut_secondary:
                ing_name_item = make_tw_checkbox_item(ing_str, False)
                level_item = make_tw_str_item(str(level))
                nut_item = make_tw_str_item(nut_str)
                quant_item = make_tw_str_item(str(quant))
                description_item = make_tw_str_item("100g분량 고려출력")
                tw.setItem(rowIndex, 0, ing_name_item)
                tw.setItem(rowIndex, 1, level_item)
                tw.setItem(rowIndex, 2, nut_item)
                tw.setItem(rowIndex, 3, quant_item)
                tw.setItem(rowIndex, 4, description_item)
                rowIndex += 1
        tw.setRowCount(rowIndex)
        tw.resizeColumnsToContents()
        #             for ing in Ingredient.objects(
        #                             Q(출력대표성등급__lte=printing_rep_level) & Q(멸종등급__lt=extinction_level)):
        #             # for ing in Ingredient.objects.all():
        #             #    self.build_ing_quant_dict(nut_str, ing, ing_quant_dict_for_nut, ing_quant_dict_for_nut_secondary, portion_code, is_one_portion_first, is_100g_first)
        #                 if self.isOriginAndSpecialtyBothSatisfied(ing) and nut_str in ing.식품영양소관계:
        #                     ing_quant_dict_for_nut[ing.식품명] = self.calculate_nut_quant_for_ing(ing, nut_str,
        #                                                                                        portion_code, False)
        #                     if is_one_portion_first and is_100g_first: #1회식사와 100그램 중복 설정시 1회식사분량 먼저 표시후 100그램 표시
        #                         ing_quant_dict_for_nut_secondary[ing.식품명] = self.calculate_nut_quant_for_ing(ing, nut_str,
        #                                                                                                      portion_code, True)
        #                     # ing_quant_dict_for_nut[ing.식품명] = ing.식품영양소관계[nut_str]
        #             min_count = self.get_level_count(level, ing_quant_dict_for_nut)
        #             sorted_ing_quant_list = sorted(ing_quant_dict_for_nut.items(), key=operator.itemgetter(1),
        #                                            reverse=True)[:min_count]
        #             if is_one_portion_first and is_100g_first:
        #                 min_count2 = self.get_level_count(level, ing_quant_dict_for_nut_secondary)
        #                 sorted_ing_quant_list2 = sorted(ing_quant_dict_for_nut_secondary.items(), key=operator.itemgetter(1),
        #                                                reverse=True)[:min_count2]
        #                 for item in sorted_ing_quant_list2:
        #                     ing_quant_list_for_nut_secondary.append((item[0], item[1], level, nut_str)) #(ing_str, quant, level, nut_str)
        #
        #             for index in range(min_count):
        #                 ing_name = sorted_ing_quant_list[index][0]
        #                 quant = sorted_ing_quant_list[index][1]
        #                 ing_name_item = make_tw_checkbox_item(ing_name, False)
        #                 level_item = make_tw_str_item(str(level))
        #                 nut_item = make_tw_str_item(nut_str)
        #                 quant_item = make_tw_str_item(str(quant))
        #                 tw.setItem(rowIndex, 0, ing_name_item)
        #                 tw.setItem(rowIndex, 1, level_item)
        #                 tw.setItem(rowIndex, 2, nut_item)
        #                 tw.setItem(rowIndex, 3, quant_item)
        #                 if is_one_portion_first and is_100g_first:
        #                     description_item = make_tw_str_item("1회식사분량 고려출력")
        #                     tw.setItem(rowIndex, 4, description_item)
        #                 rowIndex += 1
        #
        # if is_one_portion_first and is_100g_first:
        #     for (ing_str, quant, level, nut_str) in ing_quant_list_for_nut_secondary:
        #         ing_name_item = make_tw_checkbox_item(ing_str, False)
        #         level_item = make_tw_str_item(str(level))
        #         nut_item = make_tw_str_item(nut_str)
        #         quant_item = make_tw_str_item(str(quant))
        #         description_item = make_tw_str_item("100g분량 고려출력")
        #         tw.setItem(rowIndex, 0, ing_name_item)
        #         tw.setItem(rowIndex, 1, level_item)
        #         tw.setItem(rowIndex, 2, nut_item)
        #         tw.setItem(rowIndex, 3, quant_item)
        #         tw.setItem(rowIndex, 4, description_item)
        #         rowIndex += 1
        #
        #
        # tw.setRowCount(rowIndex)
        # tw.resizeColumnsToContents()

    def calculate_nut_quant_for_ing(self, ing_str, nut_str, portion_code, for_secondary):
        # 데이터안에는 각 식품 100그램 안에 영양소가 얼마 들어있는지 기입되어있음
        # 1 - one_portion_first clicked, 2 - 100g_first clicked, 4 - mortality_first clicked, 8 - protein_first clicked
        ing = Ingredient.objects.get(식품명 = ing_str)
        default_100g_value = Decimal(ing.식품영양소관계[nut_str])
        if for_secondary or portion_code == 2 or portion_code == 6 or portion_code == 10 or portion_code == 14: #여기서는 무조건 100그램으로 써줘야함
            if portion_code == 3 or portion_code == 2:
                return default_100g_value
            elif portion_code == 7 or portion_code == 6:
                return default_100g_value * (1-ing.폐기율)
            elif portion_code == 11 or portion_code == 10:
                return default_100g_value * (ing.단백질가식부)
            elif portion_code == 15 or portion_code == 14:
                return default_100g_value * (1-ing.폐기율) * ing.단백질가식부
        else:
            if (portion_code == 1 or portion_code == 3):
                return default_100g_value * ing.단일식사분량 / 100
            elif portion_code == 4 or portion_code == 5 or portion_code == 7:
                return default_100g_value * ing.단일식사분량 / 100 * (1-ing.폐기율)
            elif portion_code == 8 or portion_code == 9 or portion_code == 11:
                return default_100g_value * ing.단일식사분량 / 100 * ing.단백질가식부
            elif portion_code == 12 or portion_code == 13 or portion_code == 15:
                return default_100g_value * ing.단일식사분량 / 100 * (1-ing.폐기율) * ing.단백질가식부


    def get_level_count(self, level, dict):
        if level == 5:
            return min(int(self.ui.lineEdit_lv5_9.text()), len(dict))
        elif level == 4:
            return min(int(self.ui.lineEdit_lv4_9.text()), len(dict))
        elif level == 3:
            return min(int(self.ui.lineEdit_lv3_9.text()), len(dict))
        elif level == 2:
            return min(int(self.ui.lineEdit_lv2_9.text()), len(dict))
        elif level == 1:
            return min(int(self.ui.lineEdit_lv1_9.text()), len(dict))
        elif level == -5:
            return min(int(self.ui.lineEdit_lvn5_9.text()), len(dict))
        elif level == -4:
            return min(int(self.ui.lineEdit_lvn4_9.text()), len(dict))
        elif level == -3:
            return min(int(self.ui.lineEdit_lvn3_9.text()), len(dict))
        elif level == -2:
            return min(int(self.ui.lineEdit_lvn2_9.text()), len(dict))
        elif level == -1:
            return min(int(self.ui.lineEdit_lvn1_9.text()), len(dict))


    def build_rec_unrec_index_nut_dict(self, tw, rec_index_nut_dict, unrec_index_nut_dict):
        for index in range(tw.rowCount()):
            # recommended nut
            if tw.item(index, 0).checkState() == QtCore.Qt.Checked and tw.item(index, 1).checkState() == QtCore.Qt.Unchecked and int(tw.item(index, 3).text()) > 0:
                level = int(tw.item(index, 3).text())
                nut_name = tw.item(index, 2).text()
                insert_item_in_a_value_set_in_dict(rec_index_nut_dict, level, nut_name)
            # unrecommended nut
            elif tw.item(index, 0).checkState() == QtCore.Qt.Unchecked and tw.item(index, 1).checkState() == QtCore.Qt.Checked and int(tw.item(index, 3).text()) < 0:
                level = int(tw.item(index, 3).text())
                nut_name = tw.item(index, 2).text()
                insert_item_in_a_value_set_in_dict(unrec_index_nut_dict, level, nut_name)

    def render_basic_patient_info_on_top(self, currPage):
        if currPage == 4:
            self.ui.lineEdit_name_4.setText(self.current_patient.이름)
            self.ui.lineEdit_ID_4.setText(self.current_patient.ID)
            self.ui.lineEdit_birthdate_4.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
            self.ui.lineEdit_age_4.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
            self.ui.lineEdit_lastOfficeVisit_4.setText(str(datetime.date.today()))
            self.ui.lineEdit_height_4.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_4.setText(str(self.current_patient.몸무게))
            self.ui.lineEdit_nthVisit_4.setText(str(self.current_patient.방문횟수 + 1))
        elif currPage == 7:
            self.ui.lineEdit_name_7.setText(self.current_patient.이름)
            self.ui.lineEdit_ID_7.setText(self.current_patient.ID)
            self.ui.lineEdit_birthdate_7.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
            self.ui.lineEdit_age_7.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
            self.ui.lineEdit_lastOfficeVisit_7.setText(str(datetime.date.today()))
            self.ui.lineEdit_height_7.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_7.setText(str(self.current_patient.몸무게))
            self.ui.lineEdit_nthVisit_7.setText(str(self.current_patient.방문횟수 + 1))
        elif currPage == 9:
            self.ui.lineEdit_name_9.setText(self.current_patient.이름)
            self.ui.lineEdit_ID_9.setText(self.current_patient.ID)
            self.ui.lineEdit_birthdate_9.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
            self.ui.lineEdit_age_9.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
            self.ui.lineEdit_lastOfficeVisit_9.setText(str(datetime.date.today()))
            self.ui.lineEdit_height_9.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_9.setText(str(self.current_patient.몸무게))
            self.ui.lineEdit_nthVisit_9.setText(str(self.current_patient.방문횟수 + 1))
        elif currPage == 10:
            self.ui.lineEdit_name_10.setText(self.current_patient.이름)
            self.ui.lineEdit_ID_10.setText(self.current_patient.ID)
            self.ui.lineEdit_birthdate_10.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
            self.ui.lineEdit_age_10.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
            self.ui.lineEdit_lastOfficeVisit_10.setText(str(datetime.date.today()))
            self.ui.lineEdit_height_10.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_10.setText(str(self.current_patient.몸무게))
            self.ui.lineEdit_nthVisit_10.setText(str(self.current_patient.방문횟수 + 1))
        elif currPage == 29:
            self.ui.lineEdit_name_29.setText(self.current_patient.이름)
            self.ui.lineEdit_ID_29.setText(self.current_patient.ID)
            self.ui.lineEdit_birthdate_29.setText(self.current_patient.생년월일.strftime('%Y/%m/%d'))
            self.ui.lineEdit_age_29.setText(calculate_age_from_birthdate_string(self.current_patient.생년월일))
            self.ui.lineEdit_lastOfficeVisit_29.setText(str(datetime.date.today()))
            self.ui.lineEdit_height_29.setText(str(self.current_patient.키))
            self.ui.lineEdit_weight_29.setText(str(self.current_patient.몸무게))
            self.ui.lineEdit_nthVisit_29.setText(str(self.current_patient.방문횟수 + 1))
        else:
            pass

    def get_relevant_ingred_from_all_allergies(self, gs_threshold, lgG4_threshold, ms_threshold, gasung_threshold):
        relevant_ingredients = {}
        for ingred, lvl in self.local_gs_allergic_ingredients.items():
            if lvl >= gs_threshold:
                if ingred not in relevant_ingredients or lvl >= relevant_ingredients[ingred]:
                    relevant_ingredients[ingred] = lvl
        for ingred, lvl in self.local_lgG4_allergic_ingredients.items():
            if lvl >= lgG4_threshold:
                if ingred not in relevant_ingredients or relevant_ingredients[ingred] > lvl:
                    relevant_ingredients[ingred] = lvl
        for ingred, lvl in self.local_ms_allergic_ingredients.items():
            if lvl >= ms_threshold:
                if ingred not in relevant_ingredients or relevant_ingredients[ingred] > lvl:
                    relevant_ingredients[ingred] = lvl
        for ingredient in Ingredient.objects(가성알레르기등급__lte=gasung_threshold):
            ingred = ingredient.식품명
            lvl = ingredient.가성알레르기등급
            if ingred not in relevant_ingredients or relevant_ingredients[ingred] > lvl:
                relevant_ingredients[ingred] = lvl
        return relevant_ingredients

    def highlight_duplicate_ingredients(self):
        highlight_duplicate_ingredients_page_9(self.ui.tableWidget_rec_ing_from_nut_9, self.ui.tableWidget_unrec_ing_from_nut_9, self.ui.tableWidget_rec_ing_from_dis_9, self.ui.tableWidget_unrec_ing_from_dis_9, self.ui.tableWidget_unrec_ing_from_allergies_9)

    def populate_rec_or_unrec_ing_tw(self, tw, level, dis_set, currRowIndex):
        rowIndex = currRowIndex
        for dis_name in dis_set:
            ckbtnitem = QtWidgets.QTableWidgetItem(dis_name)
            ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            ckbtnitem.setCheckState(QtCore.Qt.Checked)
            tw.setItem(rowIndex, 0, ckbtnitem)
            item = QtWidgets.QTableWidgetItem(str(level))
            tw.setItem(rowIndex, 1, item)
            rowIndex += 1

    def get_most_specified_origin_and_level(self, currPage):
        if currPage == 8:
            if self.ui.comboBox_origin_5_8.currentText() != "":
                return self.ui.comboBox_origin_5_8.currentText(), 5
            elif self.ui.comboBox_origin_4_8.currentText() != "":
                return self.ui.comboBox_origin_4_8.currentText(), 4
            elif self.ui.comboBox_origin_3_8.currentText() != "":
                return self.ui.comboBox_origin_3_8.currentText(), 3
            elif self.ui.comboBox_origin_2_8.currentText() != "":
                return self.ui.comboBox_origin_2_8.currentText(), 2
            elif self.ui.comboBox_origin_1_8.currentText() != "":
                return self.ui.comboBox_origin_1_8.currentText(), 1
            else:
                return "", -1


    def get_most_specified_specialty_and_level(self, currPage):
        if currPage == 8:
            if self.ui.comboBox_specialty_5_8.currentText() != "":
                return self.ui.comboBox_specialty_5_8.currentText(), 5
            elif self.ui.comboBox_specialty_4_8.currentText() != "":
                return self.ui.comboBox_specialty_4_8.currentText(), 4
            elif self.ui.comboBox_specialty_3_8.currentText() != "":
                return self.ui.comboBox_specialty_3_8.currentText(), 3
            elif self.ui.comboBox_specialty_2_8.currentText() != "":
                return self.ui.comboBox_specialty_2_8.currentText(), 2
            elif self.ui.comboBox_specialty_1_8.currentText() != "":
                return self.ui.comboBox_specialty_1_8.currentText(), 1
            else:
                return "", -1


    def activate_origin_and_specialty_combobox(self):
        listOfOrigin1 = Ingredient.objects.distinct("원산지분류1")
        self.ui.comboBox_origin_1_8.addItem("")
        self.ui.comboBox_origin_1_8.addItems(listOfOrigin1)
        self.ui.comboBox_origin_1_8.activated[str].connect(self.on_origin1_changed)
        listOfSpecialty1 = Ingredient.objects.distinct("특산지분류1")
        self.ui.comboBox_specialty_1_8.addItem("")
        self.ui.comboBox_specialty_1_8.addItems(listOfSpecialty1)
        self.ui.comboBox_specialty_1_8.activated[str].connect(self.on_specialty1_changed)

    def on_origin1_changed(self, inputText):
        listOfOrigin2 = Ingredient.objects(원산지분류1=inputText).distinct("원산지분류2")
        self.ui.comboBox_origin_2_8.clear()
        self.ui.comboBox_origin_3_8.clear()
        self.ui.comboBox_origin_4_8.clear()
        self.ui.comboBox_origin_5_8.clear()

        self.ui.comboBox_origin_2_8.addItem("")
        self.ui.comboBox_origin_2_8.addItems(listOfOrigin2)
        self.ui.comboBox_origin_2_8.activated[str].connect(self.on_origin2_changed)

    def on_origin2_changed(self, inputText):
        listOfOrigin3 = Ingredient.objects(원산지분류2=inputText).distinct("원산지분류3")
        self.ui.comboBox_origin_3_8.clear()
        self.ui.comboBox_origin_4_8.clear()
        self.ui.comboBox_origin_5_8.clear()

        self.ui.comboBox_origin_3_8.addItem("")
        self.ui.comboBox_origin_3_8.addItems(listOfOrigin3)
        self.ui.comboBox_origin_3_8.activated[str].connect(self.on_origin3_changed)

    def on_origin3_changed(self, inputText):
        listOfOrigin4 = Ingredient.objects(원산지분류3=inputText).distinct("원산지분류4")
        self.ui.comboBox_origin_4_8.clear()
        self.ui.comboBox_origin_5_8.clear()

        self.ui.comboBox_origin_4_8.addItem("")
        self.ui.comboBox_origin_4_8.addItems(listOfOrigin4)
        self.ui.comboBox_origin_4_8.activated[str].connect(self.on_origin4_changed)

    def on_origin4_changed(self, inputText):
        listOfOrigin5 = Ingredient.objects(원산지분류4=inputText).distinct("원산지분류5")
        self.ui.comboBox_origin_5_8.clear()
        self.ui.comboBox_origin_5_8.addItem("")
        self.ui.comboBox_origin_5_8.addItems(listOfOrigin5)

    def on_specialty1_changed(self, inputText):
        listOfSpecialty2 = Ingredient.objects(특산지분류1=inputText).distinct("특산지분류2")
        self.ui.comboBox_specialty_2_8.clear()
        self.ui.comboBox_specialty_3_8.clear()
        self.ui.comboBox_specialty_4_8.clear()
        self.ui.comboBox_specialty_5_8.clear()

        self.ui.comboBox_specialty_2_8.addItem("")
        self.ui.comboBox_specialty_2_8.addItems(listOfSpecialty2)
        self.ui.comboBox_specialty_2_8.activated[str].connect(self.on_specialty2_changed)

    def on_specialty2_changed(self, inputText):
        listOfSpecialty3 = Ingredient.objects(특산지분류2=inputText).distinct("특산지분류3")
        self.ui.comboBox_specialty_3_8.clear()
        self.ui.comboBox_specialty_4_8.clear()
        self.ui.comboBox_specialty_5_8.clear()

        self.ui.comboBox_specialty_3_8.addItem("")
        self.ui.comboBox_specialty_3_8.addItems(listOfSpecialty3)
        self.ui.comboBox_specialty_3_8.activated[str].connect(self.on_specialty3_changed)

    def on_specialty3_changed(self, inputText):
        listOfSpecialty4 = Ingredient.objects(특산지분류3=inputText).distinct("특산지분류4")
        self.ui.comboBox_specialty_4_8.clear()
        self.ui.comboBox_specialty_5_8.clear()

        self.ui.comboBox_specialty_4_8.addItem("")
        self.ui.comboBox_specialty_4_8.addItems(listOfSpecialty4)
        self.ui.comboBox_specialty_4_8.activated[str].connect(self.on_specialty4_changed)

    def on_specialty4_changed(self, inputText):
        listOfSpecialty5 = Ingredient.objects(특산지분류4=inputText).distinct("특산지분류5")
        self.ui.comboBox_specialty_5_8.clear()
        self.ui.comboBox_specialty_5_8.addItem("")
        self.ui.comboBox_specialty_5_8.addItems(listOfSpecialty5)

    def go_to_register_or_edit_ingredient_info_page2(self):
        self.ui.stackedWidget.setCurrentIndex(16)
        self.ui.widget_popup_nut_16.hide()
        if self.current_ingredient is not None: #already existing ingredient
            self.populate_existing_ingredient_nut_relationship()

    def populate_existing_ingredient_nut_relationship(self):
        relevant_nutrients = get_relevant_nutrients_from_ingredient_str(self.current_ingredient.식품명)
        self.ui.tableWidget_nut_quant_16.setRowCount(len(relevant_nutrients))
        rowIndex = 0
        for nut in relevant_nutrients.keys():
            quant = relevant_nutrients[nut]
            ckbtnitem = make_tw_checkbox_item(nut, False)
            self.ui.tableWidget_nut_quant_16.setItem(rowIndex, 0, ckbtnitem)
            item = make_tw_str_item(str(quant))
            self.ui.tableWidget_nut_quant_16.setItem(rowIndex, 1, item)
            rowIndex+=1
        self.ui.tableWidget_nut_quant_16.resizeColumnToContents(0)
        self.ui.tableWidget_nut_quant_16.resizeColumnToContents(1)

    def go_to_pageN_with_warning_before_exiting(self, pageToGo):
        if self.warn_before_leaving():
            self.ui.stackedWidget.setCurrentIndex(pageToGo)

    def go_to_pageN(self, pageToGo):
        self.ui.stackedWidget.setCurrentIndex(pageToGo)

    def check_unique_ing_name(self, lineedit):
        try:
            nameFound = Ingredient.objects.get(식품명=lineedit.text())
        except Ingredient.DoesNotExist:
            nameFound = None
        if nameFound:
            lineedit.setText("")
            create_warning_message("동일한 식품명이 존재합니다. 다른 식품명을 시도해주세요")

        else:
            create_normal_message("사용가능한 식품명입니다")

    def check_unique_nut_name(self, lineedit):
        try:
            nameFound = Nutrient.objects.get(영양소명=lineedit.text())
        except Nutrient.DoesNotExist:
            nameFound = None
        if nameFound:
            lineedit.setText("")
            create_warning_message("동일한 영양소명이 존재합니다. 다른 영양소명을 시도해주세요")

        else:
            create_normal_message("사용가능한 명양소명입니다")

    def check_unique_dis_name(self, lineedit):
        try:
            nameFound = Disease.objects.get(질병명=lineedit.text())
        except Disease.DoesNotExist:
            nameFound = None
        if nameFound:
            lineedit.setText("")
            create_warning_message("동일한 질병명이 존재합니다. 다른 질병명을 시도해주세요")

        else:
            create_normal_message("사용가능한 질병명입니다")


    def go_to_register_or_edit_ingredient_info(self, ing_name):
        if ing_name is not None:
            self.clear_find_existing_ingredient()
        self.ui.stackedWidget.setCurrentIndex(15)
        listOfCat1 = Ingredient.objects.distinct("식품분류1")
        self.ui.comboBox_ing_category1_15.addItem("")
        self.ui.comboBox_ing_category1_15.addItems(listOfCat1)
        listOfOrigin1 = Ingredient.objects.distinct("원산지분류1")
        self.ui.comboBox_ing_origin1_15.addItem("")
        self.ui.comboBox_ing_origin1_15.addItems(listOfOrigin1)
        listOfSpecialty1 = Ingredient.objects.distinct("특산지분류1")
        self.ui.comboBox_ing_specialty1_15.addItem("")
        self.ui.comboBox_ing_specialty1_15.addItems(listOfSpecialty1)

        if ing_name is not None:  # if editing existing ingredient
            self.populate_existing_ingredient_info1(ing_name)

    def populate_existing_ingredient_info1(self, ing_name):
        self.current_ingredient = Ingredient.objects.get(식품명=ing_name)
        self.ui.lineEdit_ing_name_15.setText(self.current_ingredient.식품명)

        listOfCat2 = Ingredient.objects(식품분류1=self.current_ingredient.식품분류1).distinct("식품분류2")
        self.ui.comboBox_ing_category2_15.addItem("")
        self.ui.comboBox_ing_category2_15.addItems(listOfCat2)
        listOfCat3 = Ingredient.objects(식품분류2=self.current_ingredient.식품분류2).distinct("식품분류3")
        self.ui.comboBox_ing_category3_15.addItem("")
        self.ui.comboBox_ing_category3_15.addItems(listOfCat3)
        listOfCat4 = Ingredient.objects(식품분류3=self.current_ingredient.식품분류3).distinct("식품분류4")
        self.ui.comboBox_ing_category4_15.addItem("")
        self.ui.comboBox_ing_category4_15.addItems(listOfCat4)
        listOfCat5 = Ingredient.objects(식품분류4=self.current_ingredient.식품분류4).distinct("식품분류5")
        self.ui.comboBox_ing_category5_15.addItem("")
        self.ui.comboBox_ing_category5_15.addItems(listOfCat5)

        listOfOrigin2 = Ingredient.objects(원산지분류1=self.current_ingredient.원산지분류1).distinct("원산지분류2")
        self.ui.comboBox_ing_origin2_15.addItem("")
        self.ui.comboBox_ing_origin2_15.addItems(listOfOrigin2)
        listOfOrigin3 = Ingredient.objects(원산지분류2=self.current_ingredient.원산지분류2).distinct("원산지분류3")
        self.ui.comboBox_ing_origin3_15.addItem("")
        self.ui.comboBox_ing_origin3_15.addItems(listOfOrigin3)
        listOfOrigin4 = Ingredient.objects(원산지분류3=self.current_ingredient.원산지분류3).distinct("원산지분류4")
        self.ui.comboBox_ing_origin4_15.addItem("")
        self.ui.comboBox_ing_origin4_15.addItems(listOfOrigin4)
        listOfOrigin5 = Ingredient.objects(원산지분류4=self.current_ingredient.원산지분류4).distinct("원산지분류5")
        self.ui.comboBox_ing_origin5_15.addItem("")
        self.ui.comboBox_ing_origin5_15.addItems(listOfOrigin5)
        listOfSpecialty2 = Ingredient.objects(특산지분류1=self.current_ingredient.특산지분류1).distinct("특산지분류2")
        self.ui.comboBox_ing_specialty2_15.addItem("")
        self.ui.comboBox_ing_specialty2_15.addItems(listOfSpecialty2)
        listOfSpecialty3 = Ingredient.objects(특산지분류2=self.current_ingredient.특산지분류2).distinct("특산지분류3")
        self.ui.comboBox_ing_specialty3_15.addItem("")
        self.ui.comboBox_ing_specialty3_15.addItems(listOfSpecialty3)
        listOfSpecialty4 = Ingredient.objects(특산지분류3=self.current_ingredient.특산지분류3).distinct("특산지분류4")
        self.ui.comboBox_ing_specialty4_15.addItem("")
        self.ui.comboBox_ing_specialty4_15.addItems(listOfSpecialty4)
        listOfSpecialty5 = Ingredient.objects(특산지분류4=self.current_ingredient.특산지분류4).distinct("특산지분류5")
        self.ui.comboBox_ing_specialty5_15.addItem("")
        self.ui.comboBox_ing_specialty5_15.addItems(listOfSpecialty5)

        self.ui.comboBox_ing_category1_15.setCurrentText(self.current_ingredient.식품분류1)
        self.ui.comboBox_ing_category2_15.setCurrentText(self.current_ingredient.식품분류2)
        self.ui.comboBox_ing_category3_15.setCurrentText(self.current_ingredient.식품분류3)
        self.ui.comboBox_ing_category4_15.setCurrentText(self.current_ingredient.식품분류4)
        self.ui.comboBox_ing_category5_15.setCurrentText(self.current_ingredient.식품분류5)

        self.ui.comboBox_ing_origin1_15.setCurrentText(self.current_ingredient.원산지분류1)
        self.ui.comboBox_ing_origin2_15.setCurrentText(self.current_ingredient.원산지분류2)
        self.ui.comboBox_ing_origin3_15.setCurrentText(self.current_ingredient.원산지분류3)
        self.ui.comboBox_ing_origin4_15.setCurrentText(self.current_ingredient.원산지분류4)
        self.ui.comboBox_ing_origin5_15.setCurrentText(self.current_ingredient.원산지분류5)

        self.ui.comboBox_ing_specialty1_15.setCurrentText(self.current_ingredient.특산지분류1)
        self.ui.comboBox_ing_specialty2_15.setCurrentText(self.current_ingredient.특산지분류2)
        self.ui.comboBox_ing_specialty3_15.setCurrentText(self.current_ingredient.특산지분류3)
        self.ui.comboBox_ing_specialty4_15.setCurrentText(self.current_ingredient.특산지분류4)
        self.ui.comboBox_ing_specialty5_15.setCurrentText(self.current_ingredient.특산지분류5)

        self.ui.plainTextEdit_ing_description_15.setPlainText(self.current_ingredient.식품설명)
        self.ui.lineEdit_ing_academic_name_15.setText(self.current_ingredient.학명)
        self.ui.lineEdit_ing_lang_english_15.setText(self.current_ingredient.식품명영어)
        self.ui.lineEdit_ing_lang_chinese_15.setText(self.current_ingredient.식품명중국어)
        self.ui.lineEdit_ing_lang_japanese_15.setText(self.current_ingredient.식품명일본어)
        self.ui.lineEdit_ing_lang_russian_15.setText(self.current_ingredient.식품명러시아어)
        self.ui.lineEdit_ing_lang_mongolian_15.setText(self.current_ingredient.식품명몽골어)
        self.ui.lineEdit_ing_lang_arabic_15.setText(self.current_ingredient.식품명아랍어)
        self.ui.lineEdit_ing_lang_spanish_15.setText(self.current_ingredient.식품명스페인어)
        self.ui.lineEdit_ing_lang8_15.setText(self.current_ingredient.식품명외국어8)
        self.ui.lineEdit_ing_lang9_15.setText(self.current_ingredient.식품명외국어9)
        self.ui.lineEdit_ing_lang10_15.setText(self.current_ingredient.식품명외국어10)
        self.ui.lineEdit_ing_lang11_15.setText(self.current_ingredient.식품명외국어11)
        self.ui.lineEdit_ing_one_portion_15.setText(str(self.current_ingredient.단일식사분량))
        self.ui.plainTextEdit_one_portion_description_15.setPlainText(self.current_ingredient.단일식사분량설명)
        self.ui.lineEdit_ing_mortality_rate_15.setText(str(self.current_ingredient.폐기율))
        self.ui.lineEdit_ing_protein_portion_15.setText(str(self.current_ingredient.단백질가식부))
        self.ui.spinBox_printingRep_level_15.setValue(self.current_ingredient.출력대표성등급)
        self.ui.spinBox_extinction_level_15.setValue(self.current_ingredient.멸종등급)
        set_checkstate_for_ckbtn(self.ui.ckBox_immediate_intake_15, self.current_ingredient.즉시섭취)
        set_checkstate_for_ckbtn(self.ui.ckBox_always_unrec_15, self.current_ingredient.항상비권고식품여부)
        set_checkstate_for_ckbtn(self.ui.ckBox_gs_allergy_15, self.current_ingredient.급성알레르기가능여부)
        set_checkstate_for_ckbtn(self.ui.ckBox_ms_allergy_15, self.current_ingredient.만성알레르기가능여부)
        set_checkstate_for_ckbtn(self.ui.ckBox_lgg4_allergy_15, self.current_ingredient.만성lgG4과민반응가능여부)
        self.ui.spinBox_gasung_allergy_level_15.setValue(self.current_ingredient.가성알레르기등급)
        self.ui.plainTextEdit_tale_15.setPlainText(self.current_ingredient.이야기거리)
        self.ui.plainTextEdit_feature_15.setPlainText(self.current_ingredient.특징)
        self.ui.plainTextEdit_cooking_feature_15.setPlainText(self.current_ingredient.조리시특성)
        self.ui.plainTextEdit_storage_15.setPlainText(self.current_ingredient.보관법)
        self.ui.plainTextEdit_polishing_state_15.setPlainText(self.current_ingredient.도정상태)
        self.ui.plainTextEdit_processing_state_15.setPlainText(self.current_ingredient.가공상태)

    def go_to_find_existing_ingredient_for_editing(self):
        self.ui.stackedWidget.setCurrentIndex(14)
        self.render_ing_category1_dropdown_menu()
        self.render_ing_origin1_dropdown_menu()
        self.render_ing_specialty1_dropdown_menu()

    def go_to_find_existing_nutrient_for_editing(self):
        self.ui.stackedWidget.setCurrentIndex(21)
        self.render_nut_category1_dropdown_menu()

    def clear_find_existing_nutrient(self):
        self.ui.lineEdit_nut_name_21.clear()
        self.ui.comboBox_nut_category1_21.clear()
        self.ui.tableWidget_nutCandidates_21.setRowCount(0)

    def populate_existing_nutrient_info(self, nut_name):
        self.current_nutrient = Nutrient.objects.get(영양소명=nut_name)
        self.ui.lineEdit_nut_name_22.setText(self.current_nutrient.영양소명)

        self.ui.comboBox_nut_category1_22.setCurrentText(self.current_nutrient.영양소분류)
        self.ui.lineEdit_nut_lang_english_22.setText(self.current_nutrient.영양소명영어)
        self.ui.lineEdit_nut_lang_chinese_22.setText(self.current_nutrient.영양소명중국어)
        self.ui.lineEdit_nut_lang_japanese_22.setText(self.current_nutrient.영양소명일본어)
        self.ui.lineEdit_nut_lang_russian_22.setText(self.current_nutrient.영양소명러시아어)
        self.ui.lineEdit_nut_lang_mongolian_22.setText(self.current_nutrient.영양소명몽골어)
        self.ui.lineEdit_nut_lang_arabic_22.setText(self.current_nutrient.영양소명아랍어)
        self.ui.lineEdit_nut_lang_spanish_22.setText(self.current_nutrient.영양소명스페인어)
        self.ui.lineEdit_nut_lang8_22.setText(self.current_nutrient.영양소명외국어8)
        self.ui.lineEdit_nut_lang9_22.setText(self.current_nutrient.영양소명외국어9)
        self.ui.lineEdit_nut_lang10_22.setText(self.current_nutrient.영양소명외국어10)
        self.ui.lineEdit_nut_lang11_22.setText(self.current_nutrient.영양소명외국어11)
        self.ui.lineEdit_nut_lang12_22.setText(self.current_nutrient.영양소명외국어12)

        self.ui.lineEdit_quant_RDA_22.setText(str(self.current_nutrient.하루권장량RDA))
        self.ui.lineEdit_quant_WHO_22.setText(str(self.current_nutrient.최대권장량WHO))
        self.ui.lineEdit_quant_FDA_22.setText(str(self.current_nutrient.최대권장량식약처))

        self.ui.plainTextEdit_description_22.setPlainText(self.current_nutrient.설명)
        self.ui.plainTextEdit_cooking_caution_22.setPlainText(self.current_nutrient.조리시주의할점)
        self.ui.plainTextEdit_tale_22.setPlainText(self.current_nutrient.이야기거리)
        self.ui.plainTextEdit_story1_22.setPlainText(self.current_nutrient.이야기1)
        self.ui.plainTextEdit_story2_22.setPlainText(self.current_nutrient.이야기2)
        self.ui.plainTextEdit_story3_22.setPlainText(self.current_nutrient.이야기3)
        self.ui.plainTextEdit_story4_22.setPlainText(self.current_nutrient.이야기4)

    def render_nut_category1_dropdown_menu(self):
        self.ui.comboBox_nut_category1_21.addItem("")
        self.ui.comboBox_nut_category1_21.addItems(self.list_of_nut_cat)

    def render_ing_specialty1_dropdown_menu(self):
        listOfSpecialty1 = Ingredient.objects.distinct("특산지분류1")
        self.ui.comboBox_ing_specialty1_15.addItem("")
        self.ui.comboBox_ing_specialty1_15.addItems(listOfSpecialty1)
        self.ui.comboBox_ing_specialty1_15.activated[str].connect(self.on_ing_specialty1_changed)

    def on_ing_specialty1_changed(self, inputText):
        listOfSpecialty2 = Ingredient.objects(특산지분류1=inputText).distinct("특산지분류2")
        self.ui.comboBox_ing_specialty2_15.clear()
        self.ui.comboBox_ing_specialty3_15.clear()
        self.ui.comboBox_ing_specialty4_15.clear()
        self.ui.comboBox_ing_specialty5_15.clear()

        self.ui.comboBox_ing_specialty2_15.addItem("")
        self.ui.comboBox_ing_specialty2_15.addItems(listOfSpecialty2)
        self.ui.comboBox_ing_specialty2_15.activated[str].connect(self.on_ing_specialty2_changed)

    def on_ing_specialty2_changed(self, inputText):
        listOfSpecialty3 = Ingredient.objects(특산지분류2=inputText).distinct("특산지분류3")
        self.ui.comboBox_ing_specialty3_15.clear()
        self.ui.comboBox_ing_specialty4_15.clear()
        self.ui.comboBox_ing_specialty5_15.clear()

        self.ui.comboBox_ing_specialty3_15.addItem("")
        self.ui.comboBox_ing_specialty3_15.addItems(listOfSpecialty3)
        self.ui.comboBox_ing_specialty3_15.activated[str].connect(self.on_ing_specialty3_changed)

    def on_ing_specialty3_changed(self, inputText):
        listOfSpecialty4 = Ingredient.objects(특산지분류3=inputText).distinct("특산지분류4")
        self.ui.comboBox_ing_specialty4_15.clear()
        self.ui.comboBox_ing_specialty5_15.clear()

        self.ui.comboBox_ing_specialty4_15.addItem("")
        self.ui.comboBox_ing_specialty4_15.addItems(listOfSpecialty4)
        self.ui.comboBox_ing_specialty4_15.activated[str].connect(self.on_ing_specialty4_changed)

    def on_ing_specialty4_changed(self, inputText):
        listOfSpecialty5 = Ingredient.objects(특산지분류4=inputText).distinct("특산지분류5")
        self.ui.comboBox_ing_specialty5_15.clear()
        self.ui.comboBox_ing_specialty5_15.addItem("")
        self.ui.comboBox_ing_specialty5_15.addItems(listOfSpecialty5)

    def render_ing_origin1_dropdown_menu(self):
        listOfOrigin1 = Ingredient.objects.distinct("원산지분류1")
        self.ui.comboBox_ing_origin1_15.addItem("")
        self.ui.comboBox_ing_origin1_15.addItems(listOfOrigin1)
        self.ui.comboBox_ing_origin1_15.activated[str].connect(self.on_ing_origin1_changed)

    def on_ing_origin1_changed(self, inputText):
        listOfOrigin2 = Ingredient.objects(원산지분류1=inputText).distinct("원산지분류2")
        self.ui.comboBox_ing_origin2_15.clear()
        self.ui.comboBox_ing_origin3_15.clear()
        self.ui.comboBox_ing_origin4_15.clear()
        self.ui.comboBox_ing_origin5_15.clear()

        self.ui.comboBox_ing_origin2_15.addItem("")
        self.ui.comboBox_ing_origin2_15.addItems(listOfOrigin2)
        self.ui.comboBox_ing_origin2_15.activated[str].connect(self.on_ing_origin2_changed)

    def on_ing_origin2_changed(self, inputText):
        listOfOrigin3 = Ingredient.objects(원산지분류2=inputText).distinct("원산지분류3")
        self.ui.comboBox_ing_origin3_15.clear()
        self.ui.comboBox_ing_origin4_15.clear()
        self.ui.comboBox_ing_origin5_15.clear()

        self.ui.comboBox_ing_origin3_15.addItem("")
        self.ui.comboBox_ing_origin3_15.addItems(listOfOrigin3)
        self.ui.comboBox_ing_origin3_15.activated[str].connect(self.on_ing_origin3_changed)

    def on_ing_origin3_changed(self, inputText):
        listOfOrigin4 = Ingredient.objects(원산지분류3=inputText).distinct("원산지분류4")
        self.ui.comboBox_ing_origin4_15.clear()
        self.ui.comboBox_ing_origin5_15.clear()

        self.ui.comboBox_ing_origin4_15.addItem("")
        self.ui.comboBox_ing_origin4_15.addItems(listOfOrigin4)
        self.ui.comboBox_ing_origin4_15.activated[str].connect(self.on_ing_origin4_changed)

    def on_ing_origin4_changed(self, inputText):
        listOfOrigin5 = Ingredient.objects(원산지분류4=inputText).distinct("원산지분류5")
        self.ui.comboBox_ing_origin5_15.clear()
        self.ui.comboBox_ing_origin5_15.addItem("")
        self.ui.comboBox_ing_origin5_15.addItems(listOfOrigin5)

    def render_ing_category1_dropdown_menu(self):
        listOfCat1 = Ingredient.objects.distinct("식품분류1")
        self.ui.comboBox_ing_category1_14.addItem("")
        self.ui.comboBox_ing_category1_14.addItems(listOfCat1)
        self.ui.comboBox_ing_category1_14.activated[str].connect(self.on_ing_cat1_changed)

    def on_ing_cat1_changed(self, inputText):
        listOfCat2 = Ingredient.objects(식품분류1=inputText).distinct("식품분류2")
        self.ui.comboBox_ing_category2_14.clear()
        self.ui.comboBox_ing_category3_14.clear()
        self.ui.comboBox_ing_category4_14.clear()
        self.ui.comboBox_ing_category5_14.clear()

        self.ui.comboBox_ing_category2_14.addItem("")
        self.ui.comboBox_ing_category2_14.addItems(listOfCat2)
        self.ui.comboBox_ing_category2_14.activated[str].connect(self.on_ing_cat2_changed)

    def on_ing_cat2_changed(self, inputText):
        listOfCat3 = Ingredient.objects(식품분류2=inputText).distinct("식품분류3")
        self.ui.comboBox_ing_category3_14.clear()
        self.ui.comboBox_ing_category4_14.clear()
        self.ui.comboBox_ing_category5_14.clear()

        self.ui.comboBox_ing_category3_14.addItem("")
        self.ui.comboBox_ing_category3_14.addItems(listOfCat3)
        self.ui.comboBox_ing_category3_14.activated[str].connect(self.on_ing_cat3_changed)

    def on_ing_cat3_changed(self, inputText):
        listOfCat4 = Ingredient.objects(식품분류3=inputText).distinct("식품분류4")
        self.ui.comboBox_ing_category4_14.clear()
        self.ui.comboBox_ing_category5_14.clear()

        self.ui.comboBox_ing_category4_14.addItem("")
        self.ui.comboBox_ing_category4_14.addItems(listOfCat4)
        self.ui.comboBox_ing_category4_14.activated[str].connect(self.on_ing_cat4_changed)

    def on_ing_cat4_changed(self, inputText):
        listOfCat5 = Ingredient.objects(식품분류4=inputText).distinct("식품분류5")
        self.ui.comboBox_ing_category5_14.clear()
        self.ui.comboBox_ing_category5_14.addItem("")
        self.ui.comboBox_ing_category5_14.addItems(listOfCat5)

    def find_ingredients_by_name(self, name):
        if not name:
            found_ingredients = Ingredient.objects.all()
        else:
            found_ingredients = Ingredient.objects(식품명__icontains=name)
        self.render_found_ingredients(found_ingredients)

    def find_ingredients_by_category(self):
        if self.ui.comboBox_ing_category5_14.currentText() != "":
            found_ingredients = Ingredient.objects(식품분류5=self.ui.comboBox_ing_category5_14.currentText())
        elif self.ui.comboBox_ing_category4_14.currentText() != "":
            found_ingredients = Ingredient.objects(식품분류4=self.ui.comboBox_ing_category4_14.currentText())
        elif self.ui.comboBox_ing_category3_14.currentText() != "":
            found_ingredients = Ingredient.objects(식품분류3=self.ui.comboBox_ing_category3_14.currentText())
        elif self.ui.comboBox_ing_category2_14.currentText() != "":
            found_ingredients = Ingredient.objects(식품분류2=self.ui.comboBox_ing_category2_14.currentText())
        elif self.ui.comboBox_ing_category1_14.currentText() != "":
            found_ingredients = Ingredient.objects(식품분류1=self.ui.comboBox_ing_category1_14.currentText())
        else:
            found_ingredients = Ingredient.objects.all()
        self.render_found_ingredients(found_ingredients)

    def render_found_ingredients(self, found_ingredients):
        self.ui.tableWidget_ing_candidates_14.setRowCount(found_ingredients.count())
        i = 0
        for ingredient in found_ingredients:
            self.ui.tableWidget_ing_candidates_14.setItem(i, 0, make_tw_checkbox_item(ingredient.식품명, False))
            self.ui.tableWidget_ing_candidates_14.setItem(i, 1, make_tw_str_item(ingredient.식품분류1))
            self.ui.tableWidget_ing_candidates_14.setItem(i, 2, make_tw_str_item(ingredient.식품분류2))
            self.ui.tableWidget_ing_candidates_14.setItem(i, 3, make_tw_str_item(ingredient.식품분류3))
            self.ui.tableWidget_ing_candidates_14.setItem(i, 4, make_tw_str_item(ingredient.식품분류4))
            self.ui.tableWidget_ing_candidates_14.setItem(i, 5, make_tw_str_item(ingredient.식품분류5))
            i += 1

    #############################
    # NAVIGATION - Go
    #############################
    def go_home(self, currPage):
        if self.warn_before_leaving() == False:
            return
        else:
            if currPage == 3:
                self.clear_register_new_patient()
            elif currPage == 4 or currPage == 29 or currPage == 7 or currPage == 8 or currPage == 9 or currPage == 10:
                self.clear_current_patient_info_and_all_related_pages()
            elif currPage == 5:
                self.clear_find_existing_client()
            elif currPage == 6:
                self.clear_edit_existing_client()
            elif currPage == 14:
                self.clear_find_existing_ingredient()
            elif currPage == 15:
                self.clear_edit_existing_ingredient()
            elif currPage == 21:
                self.clear_find_existing_nutrient()
            else:
                pass
            self.ui.stackedWidget.setCurrentIndex(1)

    def clear_current_patient_info_and_all_related_pages(self):
        self.reset_page_7()
        self.reset_page_8()
        self.reset_page_4_and_29()
        self.reset_page_9()
        self.reset_page_10()

        self.current_patient = None
        self.local_gs_allergic_ingredients.clear()
        self.local_ms_allergic_ingredients.clear()
        self.local_lgG4_allergic_ingredients.clear()
        self.local_diseases.clear()

        self.local_rec_threshold = 0
        self.local_nonrec_threshold = 0
        self.local_gs_threshold = 0
        self.local_lgG4_threshold = 0
        self.local_ms_threshold = 0
        self.local_gasung_threshold = 0

        self.rec_level_nut_dict.clear()
        self.unrec_level_nut_dict.clear()

    def reset_page_10(self):
        self.ui.lineEdit_ID_10.clear()
        self.ui.lineEdit_name_10.clear()
        self.ui.lineEdit_birthdate_10.clear()
        self.ui.lineEdit_age_10.clear()
        self.ui.lineEdit_height_10.clear()
        self.ui.lineEdit_weight_10.clear()
        self.ui.lineEdit_nthVisit_10.clear()
        self.ui.lineEdit_lastOfficeVisit_10.clear()
        self.ui.tableWidget_current_rec_ing_10.setRowCount(0)
        self.ui.tableWidget_current_unrec_ing_10.setRowCount(0)
        self.ui.tableWidget_past_rec_ing_10.setRowCount(0)
        self.ui.tableWidget_past_unrec_ing_10.setRowCount(0)

    def reset_page_9(self):
        self.ui.lineEdit_ID_9.clear()
        self.ui.lineEdit_name_9.clear()
        self.ui.lineEdit_birthdate_9.clear()
        self.ui.lineEdit_age_9.clear()
        self.ui.lineEdit_height_9.clear()
        self.ui.lineEdit_weight_9.clear()
        self.ui.lineEdit_nthVisit_9.clear()
        self.ui.lineEdit_lastOfficeVisit_9.clear()
        self.ui.tableWidget_nutrients_rec_9.setRowCount(0)
        self.ui.tableWidget_nutrients_unrec_9.setRowCount(0)
        self.ui.tableWidget_rec_ing_from_nut_9.setRowCount(0)
        self.ui.tableWidget_unrec_ing_from_nut_9.setRowCount(0)
        self.ui.tableWidget_rec_ing_from_dis_9.setRowCount(0)
        self.ui.tableWidget_unrec_ing_from_dis_9.setRowCount(0)
        self.ui.tableWidget_unrec_ing_from_allergies_9.setRowCount(0)

    def reset_page_8(self):
        self.ui.ckBox_onePortionFirst_8.setCheckState(QtCore.Qt.Checked)
        self.ui.ckBox_100gFirst_8.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_proteinFirst_8.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_mortalityFirst_8.setCheckState(QtCore.Qt.Unchecked)
        self.ui.spinBox_printingRep_level_8.setValue(1)
        self.ui.spinBox_extinction_level_8.setValue(1)
        self.ui.comboBox_origin_1_8.clear()
        self.ui.comboBox_origin_2_8.clear()
        self.ui.comboBox_origin_3_8.clear()
        self.ui.comboBox_origin_4_8.clear()
        self.ui.comboBox_origin_5_8.clear()
        self.ui.comboBox_specialty_1_8.clear()
        self.ui.comboBox_specialty_2_8.clear()
        self.ui.comboBox_specialty_3_8.clear()
        self.ui.comboBox_specialty_4_8.clear()
        self.ui.comboBox_specialty_5_8.clear()
        self.ui.spinBox_dis_rel_ing_level_rec_8.setValue(1)
        self.ui.spinBox_dis_rel_ing_level_unrec_8.setValue(-1)
        self.ui.radioButton_dis_rel_ing_delete_both_8.setChecked(True)
        self.ui.radioButton_dis_rel_ing_to_unrec_8.setChecked(False)
        self.ui.radioButton_upperLevel_auto_8.setChecked(True)
        self.ui.radioButton_upperLevel_manual_8.setChecked(False)
        self.ui.spinBox_allergy_gasung_level_8.setValue(1)
        self.ui.spinBox_allergy_gs_level_8.setValue(1)
        self.ui.spinBox_allergy_ms_level_8.setValue(1)
        self.ui.spinBox_allergy_lgg4_level_8.setValue(1)

    def reset_page_7(self):
        self.ui.lineEdit_ID_7.clear()
        self.ui.lineEdit_name_7.clear()
        self.ui.lineEdit_birthdate_7.clear()
        self.ui.lineEdit_age_7.clear()
        self.ui.lineEdit_height_7.clear()
        self.ui.lineEdit_weight_7.clear()
        self.ui.lineEdit_nthVisit_7.clear()
        self.ui.lineEdit_lastOfficeVisit_7.clear()
        self.ui.listWidget_diseases_7.clear()
        self.ui.tableWidget_allergies_gs_7.setRowCount(0)
        self.ui.tableWidget_allergies_ms_7.setRowCount(0)
        self.ui.tableWidget_allergies_lgg4_7.setRowCount(0)

    def reset_page_4_and_29(self):
        self.ui.lineEdit_ID_4.clear()
        self.ui.lineEdit_name_4.clear()
        self.ui.lineEdit_birthdate_4.clear()
        self.ui.lineEdit_age_4.clear()
        self.ui.lineEdit_height_4.clear()
        self.ui.lineEdit_weight_4.clear()
        self.ui.lineEdit_nthVisit_4.clear()
        self.ui.lineEdit_lastOfficeVisit_4.clear()

        self.ui.lineEdit_ID_29.clear()
        self.ui.lineEdit_name_29.clear()
        self.ui.lineEdit_birthdate_29.clear()
        self.ui.lineEdit_age_29.clear()
        self.ui.lineEdit_height_29.clear()
        self.ui.lineEdit_weight_29.clear()
        self.ui.lineEdit_nthVisit_29.clear()
        self.ui.lineEdit_lastOfficeVisit_29.clear()

        for i in range(len(self.list_of_nut_tw)):
            self.list_of_nut_tw[i].setRowCount(0)

        self.ui.tableWidget_nutrients_rec_29.setRowCount(0)
        self.ui.tableWidget_nutrients_unrec_29.setRowCount(0)

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
        self.currPatientLGG4IngTupleSet = build_allergy_index_level_tuple_set_from_tw(
            self.ui.tableWidget_allergies_lgg4_4)
        self.ui.stackedWidget.setCurrentIndex(3)

    def go_back_to_edit_existing_patient_page1(self):
        self.go_to_edit_patient_basic_info(self.ui.lineEdit_ID_7.text())

    def go_back_to_edit_existing_patient_page2(self):
        self.ui.stackedWidget.setCurrentIndex(7)

    def register_patient_and_go_to_select_diseases_and_allergies(self):
        tempID = self.ui.lineEdit_ID_3.text()
        tempName = self.ui.lineEdit_name_3.text()
        tempGender = "남" if self.ui.radioBtn_male_3.isChecked() else "여"
        # TODO : fill in patient info
        # tempBirthDate = self.ui.dateEdit_birthdate_3.text()
        # tempHeight = float(self.ui.lineEdit_height_3.text()) if self.ui.lineEdit_height_3.text() != "" else 0.0

        if not tempID or not tempName:
            create_warning_message("ID, 이름, 생년월일은 필수입니다.")
        else:
            try:
                Patient(ID=tempID, 이름=tempName, 성별=tempGender).save()  # , 성별=tempGender, 키=tempHeight).save()
                self.ui.stackedWidget.setCurrentIndex(7)
                self.render_existing_patient_info_disease_and_allergies(tempID)
            except:
                create_warning_message("잘못된 환자정보입니다. 다시 입력해주시길 바랍니다")

                # self.ui.stackedWidget.setCurrentIndex(4)
                # if self.currPatientDiseaseIndexSet and \
                #         self.currPatientGSIngTupleSet and \
                #         self.currPatientMSIngTupleSet and \
                #         self.currPatientLGG4IngTupleSet:
                # #     populate_checkbox_lw(self.ui.listWidget_diseases_4, Disease.objects, "식품명")
                #     update_checkbox_state_lw(self.ui.listWidget_diseases_4, Disease.objects, "식품명", set())
                #     myCursor_gs = get_ingredients_guepsung()
                #     create_checkbox_level_tw(myCursor_gs, self.ui.tableWidget_allergies_gs_4, "식품명", True, None)
                #     myCursor_ms = get_ingredients_mansung()
                #     create_checkbox_level_tw(myCursor_ms, self.ui.tableWidget_allergies_ms_4, "식품명", True, None)
                #     myCursor_lgg4 = get_ingredients_mansung_lgg4()
                #     create_checkbox_level_tw(myCursor_lgg4, self.ui.tableWidget_allergies_lgg4_4, "식품명", True, None)
                # else: #if coming from register_new_client_page2
                #     if len(self.currPatientDiseaseIndexSet) != 0:
                #         for index in self.currPatientDiseaseIndexSet:
                #             ckbtn = self.ui.listWidget_diseases_4.item(index)
                #             ckbtn.setCheckState(QtCore.Qt.Checked)
                #     if len(self.currPatientGSIngTupleSet) != 0:
                #         self.build_current_patient_tw(self.currPatientGSIngTupleSet, self.ui.tableWidget_allergies_gs_4)
                #     if len(self.currPatientMSIngTupleSet) != 0:
                #         self.build_current_patient_tw(self.currPatientMSIngTupleSet, self.ui.tableWidget_allergies_ms_4)
                #     if len(self.currPatientLGG4IngTupleSet) != 0:
                #         self.build_current_patient_tw(self.currPatientLGG4IngTupleSet, self.ui.tableWidget_allergies_lgg4_4)

    def go_to_data_home_with_no_warning(self):
        self.ui.stackedWidget.setCurrentIndex(12)

    def go_to_data_home(self, currPage):
        if self.warn_before_leaving() == False:
            return
        else:
            if currPage == 14:
                self.clear_find_existing_ingredient()
            elif currPage == 15 or currPage == 16:
                self.clear_edit_existing_ingredient()
            elif currPage == 21:
                self.clear_find_existing_nutrient()
            else:
                pass
            self.ui.stackedWidget.setCurrentIndex(12)

    #############################
    # Page 1 - find patient
    #############################
    def find_patients_by_name(self, name, tw):
        if not name:
            found_patients = Patient.objects.all()
        else:
            found_patients = Patient.objects(이름=name)
        self.render_found_patients(found_patients, tw)

    def find_patients_by_id(self, id, tw):
        if not id:
            found_patients = Patient.objects.all()
        else:
            found_patients = Patient.objects.get(ID=id)
        self.render_found_patients(found_patients, tw)

    def render_found_patients(self, found_patients, tw):
        tw.setRowCount(found_patients.count())
        i = 0
        for patient in found_patients:
            tw.setItem(i, 0, make_tw_checkbox_item(patient.ID, False))
            tw.setItem(i, 1, make_tw_str_item(patient.이름))
            tw.setItem(i, 2, make_tw_str_item(patient.생년월일.strftime('%Y/%m/%d')))
            tw.setItem(i, 3, make_tw_str_item(patient.주소))
            i += 1
        tw.resizeColumnToContents(0)
        tw.resizeColumnToContents(1)
        tw.resizeColumnToContents(2)
        tw.resizeColumnToContents(3)


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
        # def print_current_patient(self):
        # print(self.current_patient)

    def updatePatients(self):
        pass

    def go_to_data(self):
        self.ui.stackedWidget.setCurrentIndex(12)

    def check_password(self):
        pwd = self.ui.lineEdit_pw_0.text()
        if pwd == "kiho":
            self.ui.lineEdit_pw_0.setText("")
            self.ui.stackedWidget.setCurrentIndex(1)
        elif len(pwd) != 0:
            create_warning_message("비밀번호가 틀립니다.")
        else:
            create_warning_message("비밀번호를 입력해주세요.")

    # def get_selected_patient_id(self):
    #     for patient_idx in range(self.ui.tableWidget_clientCandidates_5.rowCount()):
    #         if self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).checkState() == QtCore.Qt.Checked:
    #             return self.ui.tableWidget_clientCandidates_5.item(patient_idx, 0).text()
    #     return None

    def go_to_edit_patient_basic_info(self, id):
        self.clear_find_existing_client()
        self.ui.stackedWidget.setCurrentIndex(6)
        if id:
            # First time a current patient info is stored locally.
            self.current_patient = Patient.objects.get(ID=id)
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
            self.ui.ckBox_preg_6.setChecked(
                True) if self.current_patient.임신여부 == True else self.ui.ckBox_preg_6.setChecked(False)
            self.ui.ckBox_bFeeding_6.setChecked(
                True) if self.current_patient.수유여부 == True else self.ui.ckBox_bFeeding_6.setChecked(False)

    def go_to_page_8(self, currPage):
        if currPage == 7:
            self.update_selected_disease_and_allergies_locally()
        self.ui.stackedWidget.setCurrentIndex(8)
        self.activate_origin_and_specialty_combobox()

    def go_to_select_disease_and_allergies(self, id):
        if id == None:
            create_warning_message("진료할 회원을 선택해주세요.")
        else:
            self.ui.stackedWidget.setCurrentIndex(7)
            self.render_existing_patient_info_disease_and_allergies(
                get_first_checked_btn_text_in_tw(self.ui.tableWidget_clientCandidates_5))

    def render_existing_patient_info_disease_and_allergies(self, id):
        self.current_patient = Patient.objects.get(ID=id)
        self.render_basic_patient_info_on_top(7)

        # Render all elements to lw and tw
        self.render_disease_and_allergies_by_date("")
        self.render_past_diagnosis_combo_box()

    def render_past_diagnosis_combo_box(self):
        past_dates = [str(date).split()[0] for date in self.current_patient.진료일]
        self.ui.combobox_past_diagnosis_7.clear()
        self.ui.combobox_past_diagnosis_7.addItem("")
        self.ui.combobox_past_diagnosis_7.addItems(past_dates)
        self.ui.combobox_past_diagnosis_7.activated[str].connect(self.render_disease_and_allergies_by_date)

    def render_disease_and_allergies_by_date(self, date):
        if date:
            render_checkbox_lw(self.ui.listWidget_diseases_7, Disease.objects, "질병명", self.current_patient.진단[date])
            render_all_checkbox_level_tw(get_ingredients_guepsung(), self.ui.tableWidget_allergies_gs_7, "식품명",
                                         self.current_patient.급성알레르기음식[date])
            render_all_checkbox_level_tw(get_ingredients_mansung(), self.ui.tableWidget_allergies_ms_7, "식품명",
                                         self.current_patient.만성알레르기음식[date])
            render_all_checkbox_level_tw(get_ingredients_mansung_lgg4(), self.ui.tableWidget_allergies_lgg4_7, "식품명",
                                         self.current_patient.만성lgG4과민반응음식[date])
        else:
            render_checkbox_lw(self.ui.listWidget_diseases_7, Disease.objects, "질병명", set())
            render_all_checkbox_level_tw(get_ingredients_guepsung(), self.ui.tableWidget_allergies_gs_7, "식품명", {})
            render_all_checkbox_level_tw(get_ingredients_mansung(), self.ui.tableWidget_allergies_ms_7, "식품명", {})
            render_all_checkbox_level_tw(get_ingredients_mansung_lgg4(), self.ui.tableWidget_allergies_lgg4_7, "식품명", {})

    def update_patient_basic_info(self, patient_id):
        id = self.ui.lineEdit_ID_6.text()
        name = self.ui.lineEdit_name_6.text()
        sex = "남" if self.ui.radioBtn_male_6.isChecked else "여"
        birthdate = self.ui.dateEdit_birthdate_6.date().toString(format=QtCore.Qt.ISODate)
        address = self.ui.lineEdit_address_6.text()
        if self.ui.lineEdit_height_6.text():
            height = Decimal(self.ui.lineEdit_height_6.text())
        else:
            height = None
        if self.ui.lineEdit_weight_6.text():
            weight = Decimal(self.ui.lineEdit_weight_6.text())
        else:
            weight = None
        isPreg = True if self.ui.ckBox_preg_6.isChecked() else False
        isBFeeding = True if self.ui.ckBox_bFeeding_6.isChecked() else False
        update_patient_basic_info(id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding)
        self.go_to_home_no_warning()

    def update_selected_disease_and_allergies_locally(self):
        self.local_diseases = convert_lw_to_str_set(self.ui.listWidget_diseases_7)
        self.local_gs_allergic_ingredients = convert_tw_to_dict(self.ui.tableWidget_allergies_gs_7, 1)
        self.local_ms_allergic_ingredients = convert_tw_to_dict(self.ui.tableWidget_allergies_ms_7, 1)
        self.local_lgG4_allergic_ingredients = convert_tw_to_dict(self.ui.tableWidget_allergies_lgg4_7, 1)
        #self.save_local_data_to_patient(self.current_patient)
        # 진단 = Patient.objects.get(ID=id).진단
        # print(진단)

    def remove_selected_nutrients_from_tw(self, nutrient_tw):
        unchecked_nutrient_dict = convert_tw_to_dict(nutrient_tw, 0)
        populate_checkbox_tw_from_dict(nutrient_tw, unchecked_nutrient_dict)

    def get_level_page29(self):
        if self.ui.radioButton_lv1_29.isChecked():
            return 1
        elif self.ui.radioButton_lv2_29.isChecked():
            return 2
        elif self.ui.radioButton_lv3_29.isChecked():
            return 3
        elif self.ui.radioButton_lv4_29.isChecked():
            return 4
        elif self.ui.radioButton_lv5_29.isChecked():
            return 5
        else:
            return 0

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
            진단 = {convert_DateEditWidget_to_string(self.ui.dateEdit_lastOfficeVisit_3): convert_lw_to_str_set(
                self.ui.listWidget_diseases_4)}
            new_patient.진료 = 진단
            new_patient.방문횟수 = 1
            new_patient.키 = Decimal(self.ui.lineEdit_height_3.text()) if self.ui.lineEdit_height_3.text() else 0
            new_patient.몸무게 = Decimal(self.ui.lineEdit_weight_3.text()) if self.ui.lineEdit_weight_3.text() else 0
            new_patient.임신여부 = True if self.ui.ckBox_preg_3.isChecked() else False
            new_patient.수유여부 = True if self.ui.ckBox_bFeeding_3.isChecked() else False
            new_patient.급성알레르기음식 = convert_tw_to_dict(self.ui.tableWidget_allergies_gs_4, 1)
            new_patient.만성알레르기음식 = convert_tw_to_dict(self.ui.tableWidget_allergies_ms_4, 1)
            new_patient.만성lgG4과민반응음식 = convert_tw_to_dict(self.ui.tableWidget_allergies_lgg4_4, 1)
            new_patient.save()
            self.current_patient = new_patient

            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Information")
            msgbox.setText("회원 " + name + " 등록되었습니다. 진단을 계속하시겠습니까?")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            ret = msgbox.exec_()
            # if ret == QtWidgets.QMessageBox.Yes:
            #     self.go_to_filtering_page(id)
            # else:
            #     self.ui.stackedWidget.setCurrentIndex(1)


    def check_unique_ID(self):
        uniqIDChecked = False
        while (uniqIDChecked == False):
            idCand = self.ui.lineEdit_ID_3.text()
            try:
                idFound = Patient.objects.get(ID=idCand)
            except Patient.DoesNotExist:
                idFound = None
            if idFound:
                self.ui.lineEdit_ID_3.setText("")
                create_warning_message("동일한 ID가 존재합니다. 다른 ID를 시도해주세요")
            else:
                create_normal_message("사용가능한 아이디입니다")
                uniqIDChecked = True

    def save_local_data_to_patient(self, patient):
        patient.급성알레르기음식[str(self.current_date)] = self.local_gs_allergic_ingredients
        patient.만성알레르기음식[str(self.current_date)] = self.local_ms_allergic_ingredients
        patient.만성lgG4과민반응음식[str(self.current_date)] = self.local_lgG4_allergic_ingredients
        patient.진단[str(self.current_date)] = self.local_diseases
        local_진료일 = patient.진료일
        local_진료일.append(self.current_date)
        patient.진료일 = local_진료일
        patient.save()

    def reset_local_data(self):
        self.current_patient = None
        self.local_gs_allergic_ingredients = None
        self.local_ms_allergic_ingredients = None
        self.local_lgG4_allergic_ingredients = None
        self.local_diseases = None

    def print_local_data(self):
        print("local_급성알레르기음식: " + str(self.local_gs_allergic_ingredients))
        print("local_만성알레르기음식: " + str(self.local_ms_allergic_ingredients))
        print("local_만성lgG4과민반응음식: " + str(self.local_lgG4_allergic_ingredients))
        print("local_진단: " + str(self.local_diseases))
        print("local_권고영양소레벨_dict: " + str(self.local_권고영양소레벨_dict))
        print("local_비권고영양소레벨_dict: " + str(self.local_비권고영양소레벨_dict))

    def find_nutrients_by_category(self, combobox, tw_to_show):
        if combobox.currentText() != "":
            found_nutrients = Nutrient.objects(영양소분류=combobox.currentText())
        else:
            found_nutrients = Nutrient.objects.all()
        self.render_found_nutrients(found_nutrients, tw_to_show)


    def find_nutrients_by_name(self, nut_name, tw_to_show):
        if not nut_name:
            found_nutrients = Nutrient.objects.all()
        else:
            found_nutrients = Nutrient.objects(영양소명__icontains=nut_name)
        self.render_found_nutrients(found_nutrients, tw_to_show)

    #given collection of found nutrients, render ckbox of 영양소명, 영양소분류
    def render_found_nutrients(self, found_nutrients, tw_to_show):
        tw_to_show.setRowCount(found_nutrients.count())
        i = 0
        for nutrient in found_nutrients:
            tw_to_show.setItem(i, 0, make_tw_checkbox_item(nutrient.영양소명, False))
            tw_to_show.setItem(i, 1, make_tw_str_item(nutrient.영양소분류))
            i += 1

    def show_popup_nut_for_ing_nut_rel(self):
        self.ui.widget_popup_nut_16.show()

        self.ui.comboBox_nut_category1_16.addItem("")
        self.ui.comboBox_nut_category1_16.addItems(self.list_of_nut_cat)


    def add_selected_nutrients_to_tw_and_clear_and_hide_popup(self):
        selected_nutrients = convert_checked_item_in_tw_to_str_set(self.ui.tableWidget_nutCandidates_16)
        index = self.ui.tableWidget_nut_quant_16.rowCount()
        self.ui.tableWidget_nut_quant_16.setRowCount(index+ len(selected_nutrients))
        for nut in selected_nutrients:
            ckboxitem = make_tw_checkbox_item(nut, False)
            item = make_tw_str_item("0.0")
            self.ui.tableWidget_nut_quant_16.setItem(index, 0, ckboxitem)
            self.ui.tableWidget_nut_quant_16.setItem(index, 1, item)
            index += 1
        self.clear_popup_nut_for_ing_nut_rel()
        self.ui.widget_popup_nut_16.hide()

    def clear_popup_nut_for_ing_nut_rel(self):
        self.ui.lineEdit_nut_name_16.clear()
        self.ui.comboBox_nut_category1_16.clear()
        self.ui.tableWidget_nutCandidates_16.setRowCount(0)

    def clear_find_existing_ingredient(self):
        self.ui.lineEdit_ing_name_14.clear()
        self.ui.comboBox_ing_category1_14.clear()
        self.ui.comboBox_ing_category2_14.clear()
        self.ui.comboBox_ing_category3_14.clear()
        self.ui.comboBox_ing_category4_14.clear()
        self.ui.comboBox_ing_category5_14.clear()
        self.ui.tableWidget_ing_candidates_14.setRowCount(0)

    def cancel_edit_existing_ingredient(self):
        if self.warn_before_leaving():
            self.clear_edit_existing_ingredient()
            self.ui.stackedWidget.setCurrentIndex(13)

    def clear_edit_existing_ingredient(self): #clearing out page 15 and 16
        self.current_ingredient = None
        #page_15 stuff
        self.ui.lineEdit_ing_name_15.clear()
        self.ui.comboBox_ing_category1_15.clear()
        self.ui.comboBox_ing_category2_15.clear()
        self.ui.comboBox_ing_category3_15.clear()
        self.ui.comboBox_ing_category4_15.clear()
        self.ui.comboBox_ing_category5_15.clear()
        self.ui.plainTextEdit_ing_description_15.clear()
        self.ui.lineEdit_ing_academic_name_15.clear()
        self.ui.lineEdit_ing_lang_english_15.clear()
        self.ui.lineEdit_ing_lang_chinese_15.clear()
        self.ui.lineEdit_ing_lang_japanese_15.clear()
        self.ui.lineEdit_ing_lang_russian_15.clear()
        self.ui.lineEdit_ing_lang_mongolian_15.clear()
        self.ui.lineEdit_ing_lang_arabic_15.clear()
        self.ui.lineEdit_ing_lang_spanish_15.clear()
        self.ui.lineEdit_ing_lang8_15.clear()
        self.ui.lineEdit_ing_lang9_15.clear()
        self.ui.lineEdit_ing_lang10_15.clear()
        self.ui.lineEdit_ing_lang11_15.clear()
        self.ui.lineEdit_ing_one_portion_15.clear()
        self.ui.plainTextEdit_one_portion_description_15.clear()
        self.ui.lineEdit_ing_mortality_rate_15.clear()
        self.ui.lineEdit_ing_protein_portion_15.clear()
        self.ui.spinBox_printingRep_level_15.setValue(1)
        self.ui.spinBox_extinction_level_15.setValue(0)
        self.ui.ckBox_immediate_intake_15.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_always_unrec_15.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_gs_allergy_15.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_ms_allergy_15.setCheckState(QtCore.Qt.Unchecked)
        self.ui.ckBox_lgg4_allergy_15.setCheckState(QtCore.Qt.Unchecked)
        self.ui.spinBox_gasung_allergy_level_15.setValue(0)
        self.ui.plainTextEdit_tale_15.clear()
        self.ui.plainTextEdit_feature_15.clear()
        self.ui.plainTextEdit_cooking_feature_15.clear()
        self.ui.plainTextEdit_storage_15.clear()
        self.ui.plainTextEdit_processing_state_15.clear()
        self.ui.plainTextEdit_polishing_state_15.clear()

        #page_16 stuff
        self.ui.tableWidget_nut_quant_16.setRowCount(0)
        self.ui.lineEdit_nut_name_16.clear()
        self.ui.comboBox_nut_category1_16.clear()
        self.ui.tableWidget_nutCandidates_16.setRowCount(0)

    def cancel_find_existing_ingredient(self):
        self.clear_find_existing_ingredient()
        self.ui.stackedWidget.setCurrentIndex(13)

    def get_ing_categories(self):
        if self.ui.lineEdit_ing_category1_15.text() != "":
            new_ing_cat1 = self.ui.lineEdit_ing_category1_15.text()
        else:
            new_ing_cat1 = self.ui.comboBox_ing_category1_15.currentText()
        if self.ui.lineEdit_ing_category2_15.text() != "":
            new_ing_cat2 = self.ui.lineEdit_ing_category2_15.text()
        else:
            new_ing_cat2 = self.ui.comboBox_ing_category2_15.currentText()
        if self.ui.lineEdit_ing_category3_15.text() != "":
            new_ing_cat3 = self.ui.lineEdit_ing_category3_15.text()
        else:
            new_ing_cat3 = self.ui.comboBox_ing_category3_15.currentText()
        if self.ui.lineEdit_ing_category4_15.text() != "":
            new_ing_cat4 = self.ui.lineEdit_ing_category4_15.text()
        else:
            new_ing_cat4 = self.ui.comboBox_ing_category4_15.currentText()
        if self.ui.lineEdit_ing_category5_15.text() != "":
            new_ing_cat5 = self.ui.lineEdit_ing_category5_15.text()
        else:
            new_ing_cat5 = self.ui.comboBox_ing_category5_15.currentText()
        return new_ing_cat1, new_ing_cat2, new_ing_cat3, new_ing_cat4, new_ing_cat5



    def save_or_update_ingredient(self):
        # new_ing_cat1, new_ing_cat2, new_ing_cat3, new_ing_cat4, new_ing_cat5 = self.get_ing_categories()
        new_ing_cat1, new_ing_cat2, new_ing_cat3, new_ing_cat4, new_ing_cat5 = get_five_combobox_texts(
            self.ui.comboBox_ing_category1_15, self.ui.comboBox_ing_category2_15, self.ui.comboBox_ing_category3_15, self.ui.comboBox_ing_category4_15, self.ui.comboBox_ing_category5_15,
            self.ui.lineEdit_ing_category1_15, self.ui.lineEdit_ing_category2_15, self.ui.lineEdit_ing_category3_15, self.ui.lineEdit_ing_category4_15, self.ui.lineEdit_ing_category5_15)

        if not self.ui.lineEdit_ing_name_15.text() or not new_ing_cat1 or not new_ing_cat2 or not new_ing_cat3 or not new_ing_cat4 or not new_ing_cat5:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setText("식품명, 식품분류 1-5는 필수입니다.")
            msgbox.setWindowTitle("Error")
            msgbox.exec_()
        else:
            origin1, origin2, origin3, origin4, origin5 = get_five_combobox_texts(
                self.ui.comboBox_ing_origin1_15, self.ui.comboBox_ing_origin2_15, self.ui.comboBox_ing_origin3_15,
                self.ui.comboBox_ing_origin4_15, self.ui.comboBox_ing_origin5_15,
                self.ui.lineEdit_ing_origin1_15, self.ui.lineEdit_ing_origin2_15, self.ui.lineEdit_ing_origin3_15,
                self.ui.lineEdit_ing_origin4_15, self.ui.lineEdit_ing_origin5_15
            )
            specialty1, specialty2, specialty3, specialty4, specialty5 = get_five_combobox_texts(
                self.ui.comboBox_ing_specialty1_15, self.ui.comboBox_ing_specialty2_15, self.ui.comboBox_ing_specialty3_15,
                self.ui.comboBox_ing_specialty4_15, self.ui.comboBox_ing_specialty5_15,
                self.ui.lineEdit_ing_specialty1_15, self.ui.lineEdit_ing_specialty2_15, self.ui.lineEdit_ing_specialty3_15,
                self.ui.lineEdit_ing_specialty4_15, self.ui.lineEdit_ing_specialty5_15
            )
            if self.current_ingredient is None: #new ingredient
                Ingredient(
                    식품명= self.ui.lineEdit_ing_name_15.text(),
                    식품분류1 = new_ing_cat1,
                    식품분류2 = new_ing_cat2,
                    식품분류3 = new_ing_cat3,
                    식품분류4 = new_ing_cat4,
                    식품분류5 = new_ing_cat5,
                    학명 = self.ui.lineEdit_ing_academic_name_15.text(),
                    식품설명 = self.ui.plainTextEdit_ing_description_15.toPlainText(),
                    식품명영어 = self.ui.lineEdit_ing_lang_english_15.text(),
                    식품명중국어=self.ui.lineEdit_ing_lang_chinese_15.text(),
                    식품명일본어=self.ui.lineEdit_ing_lang_japanese_15.text(),
                    식품명러시아어=self.ui.lineEdit_ing_lang_russian_15.text(),
                    식품명몽골어=self.ui.lineEdit_ing_lang_mongolian_15.text(),
                    식품명아랍어=self.ui.lineEdit_ing_lang_arabic_15.text(),
                    식품명스페인어=self.ui.lineEdit_ing_lang_spanish_15.text(),
                    식품명외국어8=self.ui.lineEdit_ing_lang8_15.text(),
                    식품명외국어9=self.ui.lineEdit_ing_lang9_15.text(),
                    식품명외국어10=self.ui.lineEdit_ing_lang10_15.text(),
                    식품명외국어11=self.ui.lineEdit_ing_lang11_15.text(),
                    단일식사분량=Decimal(self.ui.lineEdit_ing_one_portion_15.text()),
                    단일식사분량설명 = self.ui.plainTextEdit_one_portion_description_15.toPlainText(),
                    폐기율 = Decimal(self.ui.lineEdit_ing_mortality_rate_15.text()),
                    단백질가식부 = Decimal(self.ui.lineEdit_ing_protein_portion_15.text()),
                    출력대표성등급 = self.ui.spinBox_printingRep_level_15.value(),
                    멸종등급 = self.ui.spinBox_extinction_level_15.value(),
                    즉시섭취 = self.ui.ckBox_immediate_intake_15.isChecked(),
                    항상비권고식품여부 = self.ui.ckBox_always_unrec_15.isChecked(),
                    가성알레르기등급 = self.ui.spinBox_gasung_allergy_level_15.value(),
                    급성알레르기가능여부 = self.ui.ckBox_gs_allergy_15.isChecked(),
                    만성알레르기가능여부 = self.ui.ckBox_ms_allergy_15.isChecked(),
                    만성lgG4과민반응가능여부 = self.ui.ckBox_lgg4_allergy_15.isChecked(),
                    이야기거리 = self.ui.plainTextEdit_tale_15.toPlainText(),
                    특징 = self.ui.plainTextEdit_feature_15.toPlainText(),
                    조리시특성 = self.ui.plainTextEdit_cooking_feature_15.toPlainText(),
                    보관법 = self.ui.plainTextEdit_storage_15.toPlainText(),
                    도정상태 = self.ui.plainTextEdit_polishing_state_15.toPlainText(),
                    가공상태 = self.ui.plainTextEdit_processing_state_15.toPlainText(),
                    원산지분류1 = origin1,
                    원산지분류2 = origin2,
                    원산지분류3 = origin3,
                    원산지분류4 = origin4,
                    원산지분류5 = origin5,
                    특산지분류1 = specialty1,
                    특산지분류2 = specialty2,
                    특산지분류3 = specialty3,
                    특산지분류4 = specialty4,
                    특산지분류5 = specialty5,
                    식품영양소관계 = convert_tw_to_dict(self.ui.tableWidget_nut_quant_16, 2)
                ).save()
            else: #updating already existing ingredient
                Ingredient.objects.get(식품명 = self.current_ingredient.식품명).update(
                    식품명=self.ui.lineEdit_ing_name_15.text(),
                    식품분류1=new_ing_cat1,
                    식품분류2=new_ing_cat2,
                    식품분류3=new_ing_cat3,
                    식품분류4=new_ing_cat4,
                    식품분류5=new_ing_cat5,
                    학명=self.ui.lineEdit_ing_academic_name_15.text(),
                    식품설명=self.ui.plainTextEdit_ing_description_15.toPlainText(),
                    식품명영어=self.ui.lineEdit_ing_lang_english_15.text(),
                    식품명중국어=self.ui.lineEdit_ing_lang_chinese_15.text(),
                    식품명일본어=self.ui.lineEdit_ing_lang_japanese_15.text(),
                    식품명러시아어=self.ui.lineEdit_ing_lang_russian_15.text(),
                    식품명몽골어=self.ui.lineEdit_ing_lang_mongolian_15.text(),
                    식품명아랍어=self.ui.lineEdit_ing_lang_arabic_15.text(),
                    식품명스페인어=self.ui.lineEdit_ing_lang_spanish_15.text(),
                    식품명외국어8=self.ui.lineEdit_ing_lang8_15.text(),
                    식품명외국어9=self.ui.lineEdit_ing_lang9_15.text(),
                    식품명외국어10=self.ui.lineEdit_ing_lang10_15.text(),
                    식품명외국어11=self.ui.lineEdit_ing_lang11_15.text(),
                    단일식사분량=Decimal(self.ui.lineEdit_ing_one_portion_15.text()),
                    단일식사분량설명=self.ui.plainTextEdit_one_portion_description_15.toPlainText(),
                    폐기율=Decimal(self.ui.lineEdit_ing_mortality_rate_15.text()),
                    단백질가식부=Decimal(self.ui.lineEdit_ing_protein_portion_15.text()),
                    출력대표성등급=self.ui.spinBox_printingRep_level_15.value(),
                    멸종등급=self.ui.spinBox_extinction_level_15.value(),
                    즉시섭취=self.ui.ckBox_immediate_intake_15.isChecked(),
                    항상비권고식품여부=self.ui.ckBox_always_unrec_15.isChecked(),
                    가성알레르기등급=self.ui.spinBox_gasung_allergy_level_15.value(),
                    급성알레르기가능여부=self.ui.ckBox_gs_allergy_15.isChecked(),
                    만성알레르기가능여부=self.ui.ckBox_ms_allergy_15.isChecked(),
                    만성lgG4과민반응가능여부=self.ui.ckBox_lgg4_allergy_15.isChecked(),
                    이야기거리=self.ui.plainTextEdit_tale_15.toPlainText(),
                    특징=self.ui.plainTextEdit_feature_15.toPlainText(),
                    조리시특성=self.ui.plainTextEdit_cooking_feature_15.toPlainText(),
                    보관법=self.ui.plainTextEdit_storage_15.toPlainText(),
                    도정상태=self.ui.plainTextEdit_polishing_state_15.toPlainText(),
                    가공상태=self.ui.plainTextEdit_processing_state_15.toPlainText(),
                    원산지분류1=origin1,
                    원산지분류2=origin2,
                    원산지분류3=origin3,
                    원산지분류4=origin4,
                    원산지분류5=origin5,
                    특산지분류1=specialty1,
                    특산지분류2=specialty2,
                    특산지분류3=specialty3,
                    특산지분류4=specialty4,
                    특산지분류5=specialty5,
                    식품영양소관계=convert_tw_to_dict(self.ui.tableWidget_nut_quant_16, 2)
                )

        self.clear_edit_existing_ingredient()
        self.ui.stackedWidget.setCurrentIndex(13)

    def find_existing_disease_for_edit(self):
        tag = self.ui.lineEdit_dis_name_26.text()
        found_diseases = Disease.objects(질병명__icontains=tag)
        render_checkbox_lw(self.ui.listWidget_dis_candidates_26, found_diseases, "질병명", None)

    def go_to_edit_disease(self):
        disease_name = get_first_checked_btn_text_in_lw(self.ui.listWidget_dis_candidates_26)
        self.local_disease_to_edit = Disease.objects.get(질병명=disease_name)
        self.render_edit_disease_page()
        self.go_to_pageN(27)

    def render_edit_disease_page(self):
        self.ui.lineEdit_dis_name_27.setText(self.local_disease_to_edit.질병명)
        self.ui.lineEdit_dis__name_english_27.setText(self.local_disease_to_edit.질병명영어)
        populate_checkbox_tw_from_dict(self.ui.tableWidget_dis_ing_27, self.local_disease_to_edit.질병식품관계)
        populate_checkbox_tw_from_dict(self.ui.tableWidget_dis_nut_27, self.local_disease_to_edit.질병영양소관계)
        self.ui.widget_popup_add_ing_27.hide()
        self.ui.widget_popup_add_nut_27.hide()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyFoodRecommender()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
