import sys
import re
import math
import csv
import string

import numpy as np

from PyQt5 import QtGui, QtWidgets, QtCore
from stackedwid1 import StackedWid1 

class MyFoodRecommender(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super(MyFoodRecommender, self).__init__(parent)
    
    self.ui = StackedWid1()
    self.ui.setupUi(self)
    
    self.setupFlow()
    
  def setupFlow(self):
    
    pass
    
    
def main():
   app = QtWidgets.QApplication(sys.argv)
   
   ex = MyFoodRecommender()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()