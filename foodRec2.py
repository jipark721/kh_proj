import sys
import re
import math
import csv
import string

import numpy as np

from PyQt5 import QtGui, QtWidgets, QtCore

import mongodb.utils as utils
from stackedwid1 import StackedWid1

class MyFoodRecommender(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyFoodRecommender, self).__init__(parent)

        self.ui = StackedWid1()
        self.ui.setupUi(self)

        self.setupLogic()


    def setupLogic(self):
        # page_4_1
        self.ui.btn_checkUniqID.clicked.connect(self.checkUniqID)
        self.ui.btn_registerClient.clicked.connect(self.registerClient)
        # page_4_2
        self.ui.btn_findbyID.clicked.connect(self.findByID)
        self.ui.btn_findbyName.clicked.connect(self.findByName)
        #self.ui.btn_

    def findByName(self):
        pass

    def findByID(self):
        pass

    def registerClient(self):
        pass
        # if len(self.ui.lineEdit_ID_4_1.text()) == 0 or len(self.ui.lineEdit_name_4_1.text()) == 0 :
        #     msgbox = QtWidgets.QMessageBox()
        #     msgbox.setIcon(QtWidgets.QMessageBox.Warning)
        #     msgbox.setText("ID, 이름, 생년월일은 필수입니다.")
        #     msgbox.setWindowTitle("Error")
        #     msgbox.exec_()
        # else:
        #     #id, name, sex, birthdate, address, height, weight, isPreg, isBFeeding, officeVisitDateList, diagDiseases
        #     id = self.ui.lineEdit_ID_4_1.text()
        #     name = self.ui.lineEdit_name_4_1.text()
        #     sex = "남자" if self.ui.radioBtn_male_4_1.isChecked else "여자"
        #     tempbdate = self.ui.dateEdit_birthdate_4_1.date()
        #     birthdate = self.ui.dateEdit_birthdate_4_1.date()
        #     address = self.ui.lineEdit_address_4_1.text()
        #     height = self.ui.lineEdit_height_4_1.text()
        #     weight = self.ui.spinBox_weight_4_1
        #
        #     utils.addOnePatient()



    def checkUniqID(self):
        uniqIDChecked = False
        while (uniqIDChecked == False):
            idCand = self.ui.lineEdit_ID_4_1.text()
            if utils.getPatientById(idCand).hasNext():
                self.ui.lineEdit_ID_4_1.setText("")
                msgbox = QtWidgets.QMessageBox()
                msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                msgbox.setText("동일한 ID가 존재합니다. 다른 ID를 시도해주세요")
                msgbox.setWindowTitle("Error")
                msgbox.exec_()
            else:
                uniqIDChecked = True


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MyFoodRecommender()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
