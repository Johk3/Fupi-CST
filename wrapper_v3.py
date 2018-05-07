"""
#Chemical Search Tool: SQLite Database query
Version 0.3 5/4/18
-Working Query to 1 database
-Working search button and input fields
-Working query links

@author: AS
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
import os

# User interface

class Ui_MainWindow(object):
    def link(self, linkStr):

        QDesktopServices.openUrl(QUrl(linkStr))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 651)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Search_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Search_Button.setGeometry(QtCore.QRect(520, 580, 81, 31))
        self.Search_Button.setObjectName("Search_Button")
        self.Print_PDF = QtWidgets.QPushButton(self.centralwidget)
        self.Print_PDF.setGeometry(QtCore.QRect(520, 550, 81, 31))
        self.Print_PDF.setObjectName("Print_PDF")
        self.Output_View = QtWidgets.QTextBrowser(self.centralwidget)
        self.Output_View.setGeometry(QtCore.QRect(10, 10, 620, 531))
        self.Output_View.setObjectName("Output_View")
        #set Output_View to read only
        self.Output_View.setReadOnly(True)
        self.Keyword_input = QtWidgets.QLineEdit(self.centralwidget)
        self.Keyword_input.setGeometry(QtCore.QRect(70, 570, 113, 20))
        self.Keyword_input.setObjectName("Keyword_input")
        self.CAS_Input = QtWidgets.QLineEdit(self.centralwidget)
        self.CAS_Input.setGeometry(QtCore.QRect(250, 570, 113, 20))
        self.CAS_Input.setText("")
        self.CAS_Input.setObjectName("CAS_Input")
        self.label_keyword = QtWidgets.QLabel(self.centralwidget)
        self.label_keyword.setGeometry(QtCore.QRect(190, 570, 51, 21))
        self.label_keyword.setObjectName("label_keyword")
        self.label_CAS = QtWidgets.QLabel(self.centralwidget)
        self.label_CAS.setGeometry(QtCore.QRect(370, 570, 51, 21))
        self.label_CAS.setObjectName("label_CAS")
        self.WVCOlogo = QtWidgets.QLabel(self.centralwidget)
        self.WVCOlogo.setGeometry(QtCore.QRect(510, 20, 101, 101))
        self.WVCOlogo.setObjectName("WVCOlogo")
        
        ##############################################################

        # -------------------------- Button action -----------------------

        self.Search_Button.clicked.connect(self.on_click)

        # ----------------------------------------------------------------

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ----------------------- Click parameters -----------------------

    def on_click(self):
        keyValue = self.Keyword_input.text()
        casValue = self.CAS_Input.text()
        con = sqlite3.connect("restriction-list--annex-xvii--export.sqlite")
        cur = con.cursor()
        cur.execute("SELECT * FROM results WHERE CASno = ?", (casValue,))
        CasResult = cur.fetchone()
        cur.execute("SELECT * FROM results WHERE name = ?", (keyValue,))
        NameResult = cur.fetchone()
        total_query = str(CasResult) + str(NameResult)
        #self.Output_View.setText(total_query) #.setText creates a single instance vs. append

        self.Output_View.append(total_query)

        #------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chem Search Tool"))
        self.Search_Button.setText(_translate("MainWindow", "Search"))
        self.Print_PDF.setText(_translate("MainWindow", "PDF"))
        self.label_keyword.setText(_translate("MainWindow", "Key"))
        self.label_CAS.setText(_translate("MainWindow", "CAS #"))


        #-------------------------------------------------------------------



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
