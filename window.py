from PyQt5 import QtCore, QtGui, QtWidgets
from log_output import *
import sys
import datafetch

# Load data here, get it from sheets & convert into json-like dict
data = datafetch.data()
checkins = []

def show_popup(message):
    # Create msg_box
    window = QtWidgets.QApplication.instance()
    if window is None:
        window = QtWidgets.QApplication(sys.argv)
        
    window = QtWidgets.QGroupBox()
    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle("Message")
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.exec_()

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.closeEvent = self.closeEvent
        
        GroupBox.setObjectName("Timesheet")
        GroupBox.resize(1433, 888)
        GroupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit = QtWidgets.QPlainTextEdit(GroupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(440, 350, 521, 61))
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit.setObjectName("plainTextEdit")
        
        font = self.plainTextEdit.font()
        font.setPointSize(self.plainTextEdit.height() // 2)  # Adjust the divisor to fit the text properly
        self.plainTextEdit.setFont(font)

        self.label = QtWidgets.QLabel(GroupBox)
        self.label.setGeometry(QtCore.QRect(610, 420, 191, 16))
        self.label.setObjectName("label")

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)
        self.plainTextEdit.textChanged.connect(self.update_label)  # Connect the textChanged signal to the update_label method

    def closeEvent(self, event):
        print("window close")
        forgot_checkout()

    def update_label(self):
        text = self.plainTextEdit.toPlainText()
        if len(text) == 8:
            try:
                data[text]
                msg = add_time(text)
                show_popup(msg)

            except KeyError as e:
                print(f"Invalid ID, {e}")
                show_popup("Invalid ID, please try again.")

            self.plainTextEdit.setPlainText("")

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("Timesheet", "Timesheet"))
        self.label.setText(_translate("Timesheet", "Please Input Your ID # or Scan Your ID"))

def createWindow():
    # Create a QApplication instance if one doesn't exist
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)


    window = QtWidgets.QGroupBox()
    ui = Ui_GroupBox()
    ui.setupUi(window)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    createWindow()
