from PyQt5 import QtGui, QtWidgets, QtCore

def make_tw_str_item(content):
    return QtWidgets.QTableWidgetItem(content)

def make_tw_checkbox_item(content):
    item = QtWidgets.QTableWidgetItem(content)
    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    item.setCheckState(QtCore.Qt.Unchecked)
    return item

def make_lw_str_item(content):
    return QtWidgets.QListWidgetItem(content)

def make_lw_checkbox_item(content):
    item = QtWidgets.QListWidgetItem(content)
    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    item.setCheckState(QtCore.Qt.Unchecked)
    return item

