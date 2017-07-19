from PyQt5 import QtGui, QtWidgets, QtCore
from models import *
import operator
import datetime
from decimal import *

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

def copy_and_paste_tw(twToCopy, twToPaste):
    twToPaste.setRowCount(twToCopy.rowCount())
    twToPaste.setColumnCount(twToCopy.columnCount())
    for rowIndex in range(twToCopy.rowCount()):
        keyitem = twToCopy.item(rowIndex, 0).text()
        ckbtnitem = QtWidgets.QTableWidgetItem(keyitem)
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Checked)
        twToPaste.setItem(rowIndex, 0, ckbtnitem)
        for colIndex in range(1, twToCopy.columnCount()):
            itemText = twToCopy.item(rowIndex, colIndex).text()
            item = QtWidgets.QTableWidgetItem(itemText)
            twToPaste.setItem(rowIndex, colIndex, item)

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

#for allergy table widgets and nut_quant tablewidgets, iterate through rows and return a list of tuple(알레르기음식, level)
#0 - fetch unchecked items, 1 - fetch checked items, 2 - fetch everything(decimal) 3 - fetch everything(integer)
#4 - fetch only first columned name
def convert_tw_to_dict(tw, fetchItemCode):
    dict = {}
    for index in range(tw.rowCount()):
        if fetchItemCode == 1:
            if tw.item(index, 0).checkState() == QtCore.Qt.Checked and int(tw.item(index, 1).text()) != 0:
                dict[tw.item(index, 0).text()] = int(tw.item(index, 1).text())
        elif fetchItemCode == 0:
            if tw.item(index, 0).checkState() == QtCore.Qt.Unchecked and Decimal(tw.item(index, 1).text()) != 0:
                dict[tw.item(index, 0).text()] = Decimal(float(tw.item(index, 1).text()))
        elif fetchItemCode == 2:
            dict[tw.item(index, 0).text()] = float(tw.item(index, 1).text())
        elif fetchItemCode == 3:
            dict[tw.item(index, 0).text()] = int(tw.item(index, 1).text())
        elif fetchItemCode == 4:
            dict[tw.item(index, 0).text()] = True
    return dict

def convert_tw_to_dict_with_key_value_level(tw):
    dict = {}
    for index in range(tw.rowCount()):
        if tw.item(index, 0).checkState() == QtCore.Qt.Checked and int(tw.item(index, 1).text()) != 0:
            lvl = int(tw.item(index, 1).text())
            if lvl in dict:
                dict[lvl].add(tw.item(index, 0).text())
            else:
                s = set()
                s.add(tw.item(index, 0).text())
                dict[lvl] = s
    return dict

def combine_two_dicts_key_level_value_set_of_ings(d1, d2):
    for key1 in d1:
        if key1 in d2:
            s1 = d1[key1]
            s2 = d2[key1]
            d1[key1] = s1 | s2
    for key2 in d2:
        if key2 not in d1:
            d1[key2] = d2[key2]
    return d1

#0 - fetch unchecked items, 1 - fetch checked items, 2 - fetch everything
def convert_lw_to_dict_with_int_value(lw, int_val, fetchItemCode):
    dict = {}
    for index in range(lw.count()):
        if fetchItemCode == 0:
            if lw.item(index).checkState() == QtCore.Qt.Unchecked:
                dict[lw.item(index).text()] = int_val
        elif fetchItemCode == 1:
            if lw.item(index).checkState() == QtCore.Qt.Checked:
                dict[lw.item(index).text()] = int_val
        elif fetchItemCode == 2:
            dict[lw.item(index).text()] = int_val
    return dict

def convert_lw_to_dict_with_key_value_default_level(lw, default_val):
    dict = {}
    for index in range(lw.count()):
        if lw.item(index).checkState() == QtCore.Qt.Checked:
            if default_val in dict.keys():
                dict[default_val].add(lw.item(index).text())
            else:
                dict[default_val] = set(lw.item(index).text())
    return dict


#for table widgets, iterate through rows and return a set of checked items
def convert_checked_item_in_tw_to_str_set(tw):
    toReturn = set()
    for i in range(tw.rowCount()):
        ckbtn = tw.item(i, 0)
        if ckbtn.checkState() == QtCore.Qt.Checked:
            toReturn.add(ckbtn.text())
    return toReturn

#for diagnosed diseases, iterate through rows and return a string separated by ","
def convert_checked_item_in_lw_to_str_set(lw):
    toReturn =  set()
    for i in range(lw.count()):
        ckbtn = lw.item(i)
        if ckbtn.checkState() == QtCore.Qt.Checked:
            toReturn.add(ckbtn.text())
    return toReturn

def render_checkbox_lw_for_collection(lw, content_collection, content_field_name, checked_content):
    lw.clear()
    for item in content_collection:
        ckbtnitem = QtWidgets.QListWidgetItem(item[content_field_name])
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        if checked_content and item[content_field_name] in checked_content:
            ckbtnitem.setCheckState(QtCore.Qt.Checked)
        lw.addItem(ckbtnitem)

def render_checkbox_lw_for_list(lw, list, checked_content):
    lw.clear()
    for item in list:
        ckbtnitem = QtWidgets.QListWidgetItem(item)
        ckbtnitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtnitem.setCheckState(QtCore.Qt.Unchecked)
        if checked_content and item in checked_content:
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
    tw.resizeColumnsToContents()

def update_checkbox_state_and_level_tw(tw, checked_content_dict):
    for index in range(tw.rowCount()):
        field_name = tw.item(index, 0).text()
        if field_name in checked_content_dict:
            tw.item(index, 0).setCheckState(QtCore.Qt.Checked)
            tw.item(index, 1).setText(str(checked_content_dict[field_name]))
        else:
            tw.item(index, 0).setCheckState(QtCore.Qt.Unchecked)
            tw.item(index, 1).setText("0")

# def remove_checked_items_from_tw(nutrient_tw, nutrient_dict):
#     for i in range(nutrient_tw.rowCount()):
#         if nutrient_tw.item(i,0).checkState():
#             nutrient_dict.pop(nutrient_tw.item(i,0).text(), None)
#     populate_checkbox_tw_from_dict(nutrient_tw, nutrient_dict)


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

def render_all_checkbox_level_tw(content_collection, tw, content_field_name, checked_content_dict):
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
        rowIndex += 1
    tw.resizeColumnsToContents()

# checked content dict:
# if not is_manual, it's dict of ing - (level, dis/allergy src)
# if is_manual, it's dict of ing - list of (level, dis/allergy src)
def render_checkbox_level_tw(tw, checked_content_dict, positive_direction, is_manual):
    tw.setRowCount(10000)
    tw.setColumnCount(3)
    rowIndex = 0
    if not is_manual:
        for elem, level_src_tuple in sorted(checked_content_dict.items(), key=operator.itemgetter(1), reverse=positive_direction):
            ckbtnitem = make_tw_checkbox_item(elem, False)

            levelitem = make_tw_str_item(str(level_src_tuple[0]))
            srcitem = make_tw_str_item(level_src_tuple[1])

            tw.setItem(rowIndex, 0, ckbtnitem)
            tw.setItem(rowIndex, 1, levelitem)
            tw.setItem(rowIndex, 2, srcitem)
            rowIndex += 1
    else: #NOT SORTED
        for elem in checked_content_dict:
            list_of_tup = checked_content_dict[elem]
            for level_src_tup in list_of_tup:
                ckbtnitem = make_tw_checkbox_item(elem, False)
                levelitem = make_tw_str_item(str(level_src_tup[0]))
                srcitem = make_tw_str_item(level_src_tup[1])
                tw.setItem(rowIndex, 0, ckbtnitem)
                tw.setItem(rowIndex, 1, levelitem)
                tw.setItem(rowIndex, 2, srcitem)
                rowIndex += 1
    tw.setRowCount(rowIndex)
    tw.resizeColumnsToContents()

# pos_dict and neg_dict:
# if not is_manual, it's dict of ing - (level, dis/allergy src)
# if is_manual, it's dict of ing - list of (level, dis/allergy src)
def render_checkbox_pos_and_neg_level_tw(positive_tw, negative_tw, pos_dict, neg_dict, is_manual):

    render_checkbox_level_tw(positive_tw, pos_dict, 1, is_manual)
    render_checkbox_level_tw(negative_tw, neg_dict, 0, is_manual)
    positive_tw.resizeColumnsToContents()
    negative_tw.resizeColumnsToContents()

def uncheck_all_checkbox_lw(lw):
    for index in range(lw.count()):
        lw.item(index).setCheckState(QtCore.Qt.Unchecked)

# def render_rec_nutrient_tw(nut_category, tw, diseases, remove_duplicates, is_misc):
#     relevant_nutrients = get_relevant_nutrients_from_diseases_str(diseases, remove_duplicates)
#     if is_misc:
#         rowIndex = tw.rowCount()
#     else:
#         rowIndex = 0
#     tw.setRowCount(rowIndex + Nutrient.objects(영양소분류=nut_category).count())
#     tw.setColumnCount(6)
#
#     for nutrient in Nutrient.objects(영양소분류=nut_category):
#         rec_ckbtn = QtWidgets.QTableWidgetItem()
#         rec_ckbtn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#         rec_ckbtn.setCheckState(QtCore.Qt.Unchecked)
#         nonrec_ckbtn = QtWidgets.QTableWidgetItem()
#         nonrec_ckbtn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#         nonrec_ckbtn.setCheckState(QtCore.Qt.Unchecked)
#         nutrient_item = QtWidgets.QTableWidgetItem(nutrient.영양소명)
#         level_item = QtWidgets.QTableWidgetItem("0")
#         cat_item = QtWidgets.QTableWidgetItem(nutrient.영양소분류)
#         # level_item.setBackground()
#         if nutrient.영양소명 in relevant_nutrients:
#             if relevant_nutrients[nutrient.영양소명] > 0:
#                 rec_ckbtn.setCheckState(QtCore.Qt.Checked)
#             else:
#                 nonrec_ckbtn.setCheckState(QtCore.Qt.Checked)
#             level_item.setText(str(relevant_nutrients[nutrient.영양소명]))
#         tw.setItem(rowIndex, 0, rec_ckbtn)
#         tw.setItem(rowIndex, 1, nonrec_ckbtn)
#         tw.setItem(rowIndex, 2, nutrient_item)
#         tw.setItem(rowIndex, 3, level_item)
#         tw.setItem(rowIndex, 4, cat_item)
#         rowIndex+=1
#     tw.resizeColumnsToContents()

def render_rec_nutrient_tw(nut_category, tw, rec_tw, unrec_tw, diseases, remove_duplicates, nut_level_src_dict):
    relevant_nutrients = get_relevant_nutrients_from_diseases_str(diseases, remove_duplicates)
    rowIndex = 0
    tw.setRowCount(Nutrient.objects(영양소분류=nut_category).count())
    tw.setColumnCount(3)

    for nutrient in Nutrient.objects(영양소분류=nut_category):
        ckbtn = QtWidgets.QTableWidgetItem()
        ckbtn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        ckbtn.setCheckState(QtCore.Qt.Unchecked)
        nutrient_item = make_tw_str_item(nutrient.영양소명)
        cat_item = make_tw_str_item(nutrient.영양소분류)
        tw.setItem(rowIndex, 0, ckbtn)
        tw.setItem(rowIndex, 1, nutrient_item)
        tw.setItem(rowIndex, 2, cat_item)
        if nutrient.영양소명 in relevant_nutrients:
            tw.item(rowIndex, 1).setBackground(QtGui.QColor(135,206,250))
            level, source = relevant_nutrients[nutrient.영양소명]
            nut_level_src_dict[nutrient.영양소명] = (level, source)

            ckbtn_item = make_tw_checkbox_item(nutrient.영양소명, False)
            level_item = make_tw_str_item(str(level))
            source_item = make_tw_str_item(source)
            if level > 0:
                rowIndex2 = rec_tw.rowCount()
                rec_tw.insertRow(rowIndex2)
                rec_tw.setItem(rowIndex2, 0, ckbtn_item)
                rec_tw.setItem(rowIndex2, 1, level_item)
                rec_tw.setItem(rowIndex2, 2, source_item)
            elif level < 0:
                rowIndex2 = unrec_tw.rowCount()
                unrec_tw.insertRow(rowIndex2)
                unrec_tw.setItem(rowIndex2, 0, ckbtn_item)
                unrec_tw.setItem(rowIndex2, 1, level_item)
                unrec_tw.setItem(rowIndex2, 2, source_item)
        rowIndex+=1
    tw.resizeColumnsToContents()

def set_all_ckbox_state_in_tw(tw, col, toCheck):
    for rowIndex in range(tw.rowCount()):
        if toCheck:
            tw.item(rowIndex, col).setCheckState(QtCore.Qt.Checked)
        else:
            tw.item(rowIndex, col).setCheckState(QtCore.Qt.Unchecked)

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

def get_first_checked_btn_text_in_lw(lw):
    for index in range(lw.count()):
        if lw.item(index).checkState() == QtCore.Qt.Checked:
            return lw.item(index).text()
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

def create_normal_message(msg):
    msgbox = QtWidgets.QMessageBox()
    msgbox.setText(msg)
    msgbox.exec_()

def get_relevant_nutrients_from_ingredient_str(ingredient):
    relevant_nutrient = {}
    for rel_nut, quant in Ingredient.objects.get(식품명=ingredient).식품영양소관계.items():
        relevant_nutrient[rel_nut] = quant
    return relevant_nutrient

def get_relevant_nutrients_from_diseases_str(diseases, remove_duplicates):
    relevant_nutrient = {}
    removed = {}
    for disease_str in diseases:
        disease = Disease.objects.get(질병명=disease_str)
        for rel_nutrient, level in disease.질병영양소관계.items():
            if rel_nutrient not in relevant_nutrient and rel_nutrient not in removed:
                relevant_nutrient[rel_nutrient] = (level, disease_str)
            elif remove_duplicates:
                del relevant_nutrient[rel_nutrient]
                removed[rel_nutrient] = True
            elif rel_nutrient in relevant_nutrient:
                old_level, old_disease_str = relevant_nutrient[rel_nutrient]
                if old_level > 0 and (level > old_level or level < 0): #상위레벨 유지
                    relevant_nutrient[rel_nutrient] = (level, disease_str)
                elif old_level < 0 and level < old_level:
                    relevant_nutrient[rel_nutrient] = (level, disease_str)
            # elif rel_nutrient in relevant_nutrient:
            #     lv, dis_str = relevant_nutrient[rel_nutrient]
            #     if lv > 0
            #     and relevant_nutrient[rel_nutrient] > 0:
            #     if level > relevant_nutrient[rel_nutrient] or level < 0:
            #         relevant_nutrient[rel_nutrient] = (level, disease_str)
            # elif rel_nutrient in relevant_nutrient and relevant_nutrient[rel_nutrient] < 0 and level < relevant_nutrient[rel_nutrient]:
            #     relevant_nutrient[rel_nutrient] = (level, disease_str)
    return relevant_nutrient

def get_portion_code(one_portion_first, gram_first, mortality_first, protein_first):
    code = 0
    if one_portion_first:
        code += 1
    if gram_first:
        code += 2
    if mortality_first:
        code += 4
    if protein_first:
        code += 8
    return code

def get_ing_cat_from_str(ing_obj, ing_cat):
    if ing_cat == "식품분류1":
        return ing_obj.식품분류1
    elif ing_cat == "식품분류2":
        return ing_obj.식품분류2
    elif ing_cat == "식품분류3":
        return ing_obj.식품분류3
    elif ing_cat == "식품분류4":
        return ing_obj.식품분류4
    elif ing_cat == "식품분류5":
        return ing_obj.식품분류5

def get_relevant_ingredients_from_nutrients_str(nutrients, count_for_single_nut, portion_code, printing_rep_level, extinction_level):
    pass

def insert_item_in_a_value_set_in_dict(dict, key, value_item):
    if key not in dict:
        temp_set = set()
        temp_set.add(value_item)
        dict[key] = temp_set
    else:
        temp_set = dict[key]
        temp_set.add(value_item)
        dict[key] = temp_set

def get_five_combobox_texts(cb1, cb2, cb3, cb4, cb5, le1, le2, le3, le4, le5):
    if le1.text() != "":
        str1 = le1.text()
    else:
        str1 = cb1.currentText()
    if le2.text() != "":
        str2 = le2.text()
    else:
        str2 = cb2.currentText()
    if le3.text() != "":
        str3 = le3.text()
    else:
        str3 = cb3.currentText()
    if le4.text() != "":
        str4 = le4.text()
    else:
        str4 = cb4.currentText()
    if le5.text() != "":
        str5 = le5.text()
    else:
        str5 = cb5.currentText()
    return str1, str2, str3, str4, str5

def highlight_duplicate_ingredients_page_9(tw1, tw2, tw3, tw4, tw5, lw1):
    tw1_items = get_tw_items(tw1)
    tw2_items = get_tw_items(tw2)
    tw3_items = get_tw_items(tw3)
    tw4_items = get_tw_items(tw4)
    tw5_items = get_tw_items(tw5)
    lw1_items = get_lw_items(lw1)

    highlight_dups(tw1, tw2_items | tw3_items | tw4_items | tw5_items)
    highlight_dups(tw2, tw1_items | tw3_items | tw4_items | tw5_items)
    highlight_dups(tw3, tw1_items | tw2_items | tw4_items | tw5_items)
    highlight_dups(tw4, tw1_items | tw2_items | tw3_items | tw5_items)
    highlight_dups(tw5, tw1_items | tw2_items | tw3_items | tw4_items)

def get_lw_items(lw):
    items = set()
    for index in range(lw.count()):
        items.add(lw.item(index).text())
    return items

def get_tw_items(tw):
    items = set()
    for index in range(tw.rowCount()):
        items.add(tw.item(index, 0).text())
    return items

def highlight_dups(tw, duplicate_items):
    for index in range(tw.rowCount()):
        if tw.item(index, 0).text() in duplicate_items:
            tw.item(index, 0).setBackground(QtGui.QColor(255, 128, 128))
        else:
            tw.item(index, 0).setBackground(QtGui.QColor(255, 255, 255))

def set_background_color_tw(tw, qcolor):
    for index in range(tw.rowCount()):
        set_background_color_single_item(tw.item(index, 0), qcolor)

def set_background_color_lw(lw, qcolor):
    for index in range(lw.count()):
        set_background_color_single_item(lw.item(index), qcolor)

def set_background_color_single_item(item, qcolor):
    item.setBackground(qcolor)

def set_checkstate_for_ckbtn(ckbtn, shouldCheck):
    if shouldCheck:
        ckbtn.setCheckState(QtCore.Qt.Checked)
    else:
        ckbtn.setCheckState(QtCore.Qt.Unchecked)

def find_item_index_for_str_in_tw(tw, str, col):
    for index in range(tw.rowCount()):
        if str == tw.item(index, col).text():
            return index
    return -1


def compare(ing1, ing2):
    pass
#########################
##
## Master Data Editor
##
#########################

def update_nutrient_list_from_ingredients(ingredient):
    for nutrient, level in ingredient.식품영양소관계.items():
        target_nutrient = Nutrient.objects.get(영양소명=nutrient)
        target_nutrient.포함식품리스트[ingredient.식품명] = level
        target_nutrient.save()

