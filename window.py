from PyQt5 import QtCore, QtGui, QtWidgets
from sheets_input import add_time

#TODO: load data here, get it from sheets & convert into json-like dict
data = {"50374567": "Ronan"}
checkins = []

def show_popup(message):
    #create app if we don't have one
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    #create msg_box
    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(message)
    msg_box.setWindowTitle("Message")
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.exec_()

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName("GroupBox")
        GroupBox.resize(1433, 888)
        GroupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.plainTextEdit = QtWidgets.QPlainTextEdit(GroupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(440, 350, 521, 61))
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(GroupBox)
        self.label.setGeometry(QtCore.QRect(610, 420, 191, 16))
        self.label.setObjectName("label")

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)
        self.plainTextEdit.textChanged.connect(self.update_label)  # Connect the textChanged signal to the update_label method

    def update_label(self):
        text = self.plainTextEdit.toPlainText()
        if len(text) == 8:
            try:
                print(f"Full ID Obtained! Welcome, {data[text]}")
                #add_time(data[text])
                
                if data[text] not in checkins:
                    checkins.append(data[text])
                    show_popup(f"Welcome, {data[text]}!")
                else:
                    checkins.pop(checkins.index(data[text]))
                    show_popup(f"You're all set, {data[text]}!")
            except KeyError:
                print("Invalid ID")
                show_popup("Invalid ID")

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        self.label.setText(_translate("GroupBox", "Please Input Your ID # or Scan Your ID"))

def createWindow():
    import sys  # Import sys module
    app = QtWidgets.QApplication([])
    window = QtWidgets.QGroupBox()
    ui = Ui_GroupBox()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    createWindow()
