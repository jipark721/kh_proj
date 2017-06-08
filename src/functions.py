from PyQt5 import QtGui, QtWidgets, QtCore

def make_str_item(content):
    return QtWidgets.QTableWidgetItem(content)

def make_checkbox_item(content):
    item = QtWidgets.QTableWidgetItem(content)
    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    item.setCheckState(QtCore.Qt.Unchecked)
    return item

