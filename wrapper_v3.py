"""
#Chemical Search Tool: SQLite Database query
Version 0.3 5/4/18
-Working Query to 1 database
-Working search button and input fields
-Working query links

@author: AS
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
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

        self.databases = []
        self.i = 1

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
        # set Output_View to read only
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
        for i in range(len(self.for_pdf_header)):
            check = 15
            font = 35
            if len(self.for_pdf_header[i]) > 20:
                font = 20
            if len(self.for_pdf_header[i]) > 60:
                font = 10
            pdf.cell(w=70)
            pdf.set_font("Arial", style="B", size=font)
            pdf.cell(40, 10, "".join(self.for_pdf_header[i]), ln=0, align="C")
            pdf.ln(check)
            check += 15
        pdf.ln(20)
        pdf.cell(w=40)
        for i in range(len(self.for_pdf)):
            font = 13
            if len(self.for_pdf[i]) > 50:
                font = 10
            if len(self.for_pdf[i]) > 110:
                font = 5
            pdf.set_font("Arial", size=font)
            pdf.cell(100, 10, "".join(self.for_pdf[i]), ln=1, align="C")
            pdf.cell(w=40)

        pdf.output("Test.pdf")
        self.Output_View.append("\nPDF file made.")

    def on_click_clear(self):
        self.Output_View.clear()
        self.for_pdf_header.clear()
        self.for_pdf.clear()

    def on_click(self):
        keyValue = self.Keyword_input.text()
        casValue = self.CAS_Input.text()
        results = []
        if keyValue or casValue:
            # For loops for all of the databses in database folder
            if self.i == 1:
                for filenames in os.listdir("database"):
                    if "".join(filenames)[len("".join(filenames)) - 2: len("".join(filenames))] == "db":
                        self.databases.append("".join(filenames))
                    elif "".join(filenames)[len("".join(filenames)) - 6: len("".join(filenames))] == "sqlite":
                        self.databases.append("".join(filenames))

                self.i += 1

            for database in self.databases:
                print("READING {}...".format(database))
                con = sqlite3.connect("database/" + str(database))
                cur = con.cursor()
                casresult = None
                nameresult = None
                if casValue != "":
                    cur.execute("SELECT * FROM results WHERE CASno = ?", (casValue,))
                    casresult = cur.fetchone()

                elif keyValue != "":
                    cur.execute("SELECT * FROM results WHERE UPPER(name) LIKE UPPER(?)", (keyValue,))
                    nameresult = cur.fetchone()
                cur.execute("SELECT * FROM results WHERE UPPER(name) LIKE UPPER('%{}%')".format(keyValue))
                results.append(cur.fetchone())

                if casresult != None or nameresult != None:
                    break

            # self.Output_View.setText(total_query) #.setText creates a single instance vs. append

            # IF both casresult and nameresult are true do this
            if casresult is not None and nameresult is not None:
                # Checks if they both are same so it doesnt write extra stuff
                if nameresult == casresult:
                    if self.for_pdf_header:
                        self.for_pdf_header.append("".join(nameresult[0]))
                        self.for_pdf.append("ECno: " + nameresult[2])
                        self.for_pdf.append("CASno: " + nameresult[3])
                        self.for_pdf.append("Condition: " + nameresult[5])

                        if casresult[1]:
                            self.Output_View.append("The Keyword: {} was found\nECno: {}\nCASno: {}"
                                                    "\nCondition: {}".format(nameresult[0],
                                                                             nameresult[2],
                                                                             nameresult[3],
                                                                             nameresult[5]))
                            return self.Output_View.append(
                                "\n{} <--> Description: {}\n".format(casresult[0], casresult[1]))

                        if nameresult[1]:
                            self.Output_View.append("The Keyword: {} was found\nECno: {}\nCASno: {}"
                                                    "\nCondition: {}".format(nameresult[0],
                                                                             nameresult[2],
                                                                             nameresult[3],
                                                                             nameresult[5]))
                            return self.Output_View.append(
                                "\n{} <--> Description: {}\n".format(nameresult[0], nameresult[1]))

                        return self.Output_View.append("\n\nThe Keyword: {} was found\nECno: {}\nCASno: {}"
                                                       "\nCondition: {}".format(nameresult[0],
                                                                                nameresult[2],
                                                                                nameresult[3],
                                                                                nameresult[5]))
                    self.for_pdf_header.append("".join(nameresult[0]))
                    self.for_pdf.append("ECno: " + nameresult[2])
                    self.for_pdf.append("CASno: " + nameresult[3])
                    self.for_pdf.append("Entryno: " + nameresult[4])
                    self.for_pdf.append("Condition: " + nameresult[5])
                    if casresult[1]:
                        self.Output_View.append("The Keyword: {} was found\nECno: {}\nCASno: {}"
                                                "\nCondition: {}".format(nameresult[0],
                                                                         nameresult[2],
                                                                         nameresult[3],
                                                                         nameresult[5]))
                        return self.Output_View.append("\n{} <--> Description: {}\n".format(casresult[0], casresult[1]))

                    if nameresult[1]:
                        self.Output_View.append("The Keyword: {} was found\nECno: {}\nCASno: {}"
                                                "\nCondition: {}".format(nameresult[0],
                                                                         nameresult[2],
                                                                         nameresult[3],
                                                                         nameresult[5]))
                        return self.Output_View.append(
                            "\n{} <--> Description: {}\n".format(nameresult[0], nameresult[1]))

                    return self.Output_View.append("The Keyword: {} was found\nECno: {}\nCASno: {}"
                                                   "\nCondition: {}".format(nameresult[0],
                                                                            nameresult[2],
                                                                            nameresult[3],
                                                                            nameresult[5]))
                if self.for_pdf_header:
                    self.for_pdf_header.append(casresult[0])
                    self.for_pdf_header.append(nameresult[0])
                    self.for_pdf.append("{} ECno: {}".format(nameresult[0], nameresult[2]))
                    self.for_pdf.append("{} ECno: {}".format(casresult[0], casresult[2]))
                    self.for_pdf.append("{} CASno: {}".format(nameresult[0], nameresult[3]))
                    self.for_pdf.append("{} CASno: {}".format(casresult[0], casresult[3]))
                    self.for_pdf.append("{} Condition: {}".format(nameresult[0], nameresult[5]))
                    self.for_pdf.append("{} Condition: {}".format(casresult[0], casresult[5]))
                    self.Output_View.append(
                        "\n\nKeyword: {} found & CAS number: {} found".format(nameresult[0], casresult[0]))
                    if casresult[1]:
                        self.Output_View.append("\n{} <--> Description: {}\n".format(casresult[0], casresult[1]))

                    if nameresult[1]:
                        self.Output_View.append("\n{} <--> Description: {}\n".format(nameresult[0], nameresult[1]))

                    return self.Output_View.append(
                        "{} ECno: {}\n{} ECno: {}\n{} CASno: {}\n{} CASno: {}\n{} Condition: {}\n{} Condition: {}".format(
                            nameresult[0], nameresult[2], casresult[0], casresult[2], nameresult[0], nameresult[3],
                            casresult[0], casresult[3],
                            nameresult[0], nameresult[5], casresult[0], casresult[5]))

                self.for_pdf_header.append(casresult[0])
                self.for_pdf_header.append(nameresult[0])
                self.for_pdf.append("{} ECno: {}".format(nameresult[0], nameresult[2]))
                self.for_pdf.append("{} ECno: {}".format(casresult[0], casresult[2]))
                self.for_pdf.append("{} CASno: {}".format(nameresult[0], nameresult[3]))
                self.for_pdf.append("{} CASno: {}".format(casresult[0], casresult[3]))
                self.for_pdf.append("{} Condition: {}".format(nameresult[0], nameresult[5]))
                self.for_pdf.append("{} Condition: {}".format(casresult[0], casresult[5]))
                self.Output_View.append(
                    "Keyword: {} found & CAS number: {} found".format(nameresult[0], casresult[0]))
                if casresult[1]:
                    self.Output_View.append("\n{} <--> Description: {}\n".format(casresult[0], casresult[1]))

                if nameresult[1]:
                    self.Output_View.append("\n{} <--> Description: {}\n".format(nameresult[0], nameresult[1]))

                return self.Output_View.append("{} ECno: {}\n{} ECno: {}\n{} CASno: {}\n{} CASno: {}\n{} Condition: {"
                                               "}\n{} Condition: {}".format(
                    nameresult[0], nameresult[2], casresult[0], casresult[2], nameresult[0], nameresult[3],
                    casresult[0], casresult[3],
                    nameresult[0], nameresult[5], casresult[0], casresult[5]))

                # If casresult or nameresult was not found
            elif casresult is None and nameresult is None:
                if keyValue:
                    # if there are any suggestions that the user might have asked then show them the suggestions
                    if results:
                        for result in results:
                            return self.Output_View.append("Did you perhaps mean {}?".format(result[0]))
                    return self.Output_View.append(
                        "Keyword {} is not proper or it has not yet been assigned to our database\n".format(keyValue))
                if not casresult:
                    return self.Output_View.append(
                        "CAS number {} is not proper or it has not yet been assigned to our database\n".format(
                            casValue))

            # If nothing in casresult or nameresult then do this
            elif casresult is None or nameresult is None:
                # Just shows the user the keyword he searched for
                if casresult is None:
                    if self.for_pdf_header:
                        self.for_pdf_header.append("".join(nameresult[0]))
                        self.for_pdf.append("ECno: " + nameresult[2])
                        self.for_pdf.append("CASno: " + nameresult[3])
                        self.for_pdf.append("Condition: " + nameresult[5])
                        self.Output_View.append("\n\nThe keyword {} was found:\n".format(keyValue))
                        if nameresult[1]:
                            self.Output_View.append("Description: {}\n".format(nameresult[1]))

                        return self.Output_View.append(
                            "ECno: {}\nCASno: {}\nCondition: {}".format(nameresult[2], nameresult[3], nameresult[5]))

                    self.for_pdf_header.append("".join(nameresult[0]))
                    self.for_pdf.append("ECno: " + nameresult[2])
                    self.for_pdf.append("CASno: " + nameresult[3])
                    self.for_pdf.append("Condition: " + nameresult[5])
                    self.Output_View.append("The keyword {} was found:\n".format(keyValue))
                    if nameresult[1]:
                        self.Output_View.append("Description: {}\n".format(nameresult[1]))
                    return self.Output_View.append(
                        "ECno: {}\nCASno: {}\nCondition: {}".format(nameresult[2], nameresult[3], nameresult[5]))
                # Shows the user the CAS number he searched for
                elif nameresult is None:
                    # If text already in the text box then add 2 lines
                    if self.for_pdf_header:
                        self.for_pdf_header.append("".join(casresult[0]))
                        self.for_pdf.append("ECno: " + casresult[2])
                        self.for_pdf.append("CASno: " + casresult[3])
                        self.for_pdf.append("Condition: " + casresult[5])

                        self.Output_View.append("\n\nThe CAS number {} was found:\n".format(casValue))
                        if casresult[1]:
                            self.Output_View.append("Description: {}\n".format(casresult[1]))

                        return self.Output_View.append(
                            "Keyword: {}\nECno: {}\nCASno: {}\nCondition: {}".format(casresult[0],
                                                                                     casresult[2],
                                                                                     casresult[3],
                                                                                     casresult[5]))
                    self.for_pdf_header.append("".join(casresult[0]))
                    self.for_pdf.append("ECno: " + casresult[2])
                    self.for_pdf.append("CASno: " + casresult[3])
                    self.for_pdf.append("Condition: " + casresult[5])

                    self.Output_View.append("The CAS number {} was found:\n".format(casValue))
                    if casresult[1]:
                        self.Output_View.append("Description: {}\n".format(casresult[1]))

                    return self.Output_View.append(
                        "Keyword: {}\nECno: {}\nCASno: {}\nCondition: {}".format(casresult[0],
                                                                                 casresult[2],
                                                                                 casresult[3],
                                                                                 casresult[5]))

            # else:
            #     self.Output_View.append(total_query)
        # If the user did not input anything do this
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

        # -------------------------------------------------------------------


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
