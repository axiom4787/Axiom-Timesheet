from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton
import warnings

try:
    from log_output import add_time, forgot_checkout
except Exception as e:
    warnings.warn(f"{e}: SHEET_INPUT IMPORT ERROR. NO DATA WILL BE PUT INTO SHEETS! `add_time` & `forgot_checkout` WILL NOT WORK AS INTENDED")

import sys
import datafetch
import time
import threading

# Load data here, get it from sheets & convert into json-like dict
global data
data = datafetch.data()
checkins = []

def threaded_periodic_update(sl_t):
    while True:
        global data
        data = datafetch.data()
        time.sleep(sl_t)

def show_popup(message):
    # Show a popup
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle("Message")
    msg_box.setIcon(QMessageBox.Information)

    button = QPushButton("OK")
    button.setEnabled(False)
    button.clicked.connect(msg_box.accept)

    msg_box.addButton(button, QMessageBox.AcceptRole)

    QTimer.singleShot(50, lambda: button.setEnabled(True))

    msg_box.exec_()

def show_exit_conf():
    # Show an exit conformation with 2 buttons, yes or no, to determine if the user wants to quit. If so, return true.
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setText("Are you sure you want to quit?")
    msg_box.setWindowTitle("Message")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setIcon(QMessageBox.Question)

    result = msg_box.exec_()
    return result == QMessageBox.Yes

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        # Set up the main UI
        GroupBox.closeEvent = self.closeEvent

        GroupBox.setObjectName("Timesheet")
        GroupBox.resize(1433, 888)
        GroupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit = QtWidgets.QPlainTextEdit(GroupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(440, 350, 521, 61))
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit.setObjectName("plainTextEdit")

        font = self.plainTextEdit.font()
        font.setPointSize(self.plainTextEdit.height() // 2)
        self.plainTextEdit.setFont(font)

        self.label = QtWidgets.QLabel(GroupBox)
        self.label.setGeometry(QtCore.QRect(610, 420, 191, 16))
        self.label.setObjectName("label")

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)
        self.plainTextEdit.textChanged.connect(self.update_label)

    def closeEvent(self, event):
        # If the user wants to exit, exit and run `forgot_checkout()`, otherwise ignore the close event
        if show_exit_conf():
            try:
                forgot_checkout()
                print("window close")
            except Exception as e:
                warnings.warn(f"{e}!")
        else:
            event.ignore()

    def update_label(self):
        text = self.plainTextEdit.toPlainText()
        if len(text) == 8:
            try:
                data[text]
                m = add_time(text)
                show_popup(f"{m}")

            except KeyError as e:
                print(f"Invalid ID, {e}")
                show_popup("Invalid ID, please try again.")

            self.plainTextEdit.setPlainText("")

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("Timesheet", "Timesheet"))
        self.label.setText(_translate("Timesheet", "Please Input Your ID # or Scan Your ID"))

def createWindow():
    # Create the main window
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    try:
        with open("ui/app.css", "r") as a:
            app.setStyleSheet(a.read())
    except Exception as e:
        warnings.warn("{e}: This app will not be styled!")

    t = threading.Thread(target=threaded_periodic_update, args=(5,))
    t.setDaemon(True)
    t.start()

    window = QtWidgets.QGroupBox()
    ui = Ui_GroupBox()
    ui.setupUi(window)
    window.show()

    sys.exit(app.exec_())

#Testing stuff & Example usage
if __name__ == "__main__":
    t = threading.Thread(target=createWindow)
    t.start()
