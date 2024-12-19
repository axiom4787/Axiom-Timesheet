from PyQt5 import QtCore, QtGui, QtWidgets
from sheets_input import add_time

#TODO: load data here, get it from sheets & convert into json-like dict
data = {"50374567": "Ronan"}

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
        self.textbox.textChanged.connect(self.update_label)

    def update_label(self):
        text = str(self.textbox.text())
        if len(text) == 8:
            try:
                print("Full ID Obtained!")
                add_time(data[text])
            except:
                print("invalid ID")

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        self.label.setText(_translate("GroupBox", "Please Input Your ID # or Scan Your ID"))

    def createWindow(self):
        setupUi()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Ui_GroupBox.createWindow()