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
from fpdf import FPDF

# User interface

class Ui_MainWindow(object):
    def link(self, linkStr):

        QDesktopServices.openUrl(QUrl(linkStr))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 651)

        self.for_pdf_header = []
        self.for_pdf = []

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Search_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Search_Button.setGeometry(QtCore.QRect(520, 580, 81, 31))
        self.Search_Button.setObjectName("Search_Button")

        self.Clear_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Clear_Button.setGeometry(QtCore.QRect(0, 600, 81, 31))
        self.Clear_Button.setObjectName("clear_Button")

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
        self.label_keyword.setGeometry(QtCore.QRect(8, 568, 60, 21))
        self.label_keyword.setObjectName("label_keyword")

        self.label_CAS = QtWidgets.QLabel(self.centralwidget)
        self.label_CAS.setGeometry(QtCore.QRect(205, 568, 51, 21))
        self.label_CAS.setObjectName("label_CAS")

        self.WVCOlogo = QtWidgets.QLabel(self.centralwidget)
        self.WVCOlogo.setGeometry(QtCore.QRect(510, 20, 101, 101))
        self.WVCOlogo.setObjectName("WVCOlogo")
        
        ##############################################################

        # -------------------------- Button action -----------------------

        self.Search_Button.clicked.connect(self.on_click)
        self.Clear_Button.clicked.connect(self.on_click_clear)
        self.Print_PDF.clicked.connect(self.on_click_pdf)

        # ----------------------------------------------------------------

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ----------------------- Click parameters -----------------------

    def on_click_pdf(self):
        if not self.for_pdf_header or not self.for_pdf:
            return self.Output_View.append("\nPDF File could not be made because you havent searched for anything")
        pdf = FPDF(format="letter")
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(w=80)
        pdf.set_font("Arial", style="B", size=40)
        pdf.cell(40,10,"".join(self.for_pdf_header), ln=0, align="C")
        pdf.ln(20)
        pdf.cell(w=40)
        pdf.set_font("Arial", size=5)
        pdf.cell(100,10, "".join(self.for_pdf), ln=1,align="C")
        pdf.output("Test.pdf")
        self.Output_View.append("\nPDF file made.")

    def on_click_clear(self):
        self.Output_View.clear()
        self.for_pdf_header.clear()
        self.for_pdf.clear()

    def on_click(self):
        keyValue = self.Keyword_input.text()
        casValue = self.CAS_Input.text()
        if keyValue or casValue:
            con = sqlite3.connect("restriction-list--annex-xvii--export.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM results WHERE CASno = ?", (casValue,))
            casresult = cur.fetchone()
            cur.execute("SELECT * FROM results WHERE UPPER(name) LIKE UPPER(?)", (keyValue,))
            nameresult = cur.fetchone()
            cur.execute("SELECT * FROM results WHERE UPPER(name) LIKE UPPER('%{}%')".format(keyValue))
            results = cur.fetchone()
            total_query = str(casresult) + str(nameresult)
            #self.Output_View.setText(total_query) #.setText creates a single instance vs. append
            if casresult is not None and nameresult is not None:
                self.for_pdf_header.append(casresult[0] + " & " + nameresult[0])
                self.for_pdf.append("".join(casresult[0]) + ": " + str(casresult[5]) + "    " + "".join(nameresult[0]) + ": " +  str(nameresult[5]))
                return self.Output_View.append("Keyword: {}\nCAS: {}".format(nameresult, casresult))

            elif casresult is None and nameresult is None:
                if results:
                    return self.Output_View.append("Did you perhaps mean {}?".format(results[0]))
                return self.Output_View.append("Keyword {} or CAS {} are not proper or they have not yet been assigned to our database\n".format(keyValue, casValue))

            elif casresult is None or nameresult is None:
                if casresult is None:
                    self.for_pdf_header.append("".join(nameresult[0]))
                    self.for_pdf.append(" ".join(nameresult))
                    self.Output_View.append("The keyword {} was found:\n".format(keyValue) + str(nameresult))
                elif nameresult is None:
                    self.for_pdf_header.append("".join(casresult[0]))
                    self.for_pdf.append(" ".join(casresult))
                    self.Output_View.append("The CAS number {} was found:\n".format(casValue) + str(casresult))

            else:
                self.Output_View.append(total_query)

        else:
            return self.Output_View.append("Give me a keyword or a CAS number!")

        # ------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chem Search Tool"))
        self.Search_Button.setText(_translate("MainWindow", "Search"))
        self.Clear_Button.setText(_translate("MainWindow", "Clear"))
        self.Print_PDF.setText(_translate("MainWindow", "PDF"))
        self.label_keyword.setText(_translate("MainWindow", "Keyword"))
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
