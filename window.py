from PyQt5 import QtCore, QtGui, QtWidgets


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
        if len(str(text)) == 8:
            print("Full ID Obtained!")

    def retranslateUi(self, GroupBox):
        _translate = QtCore.QCoreApplication.translate
        GroupBox.setWindowTitle(_translate("GroupBox", "GroupBox"))
        self.label.setText(_translate("GroupBox", "Please Input Your ID # or Scan Your ID"))

    def createWindow():
        setupUi()
        retranslateUi()
        window.show()
        sys.exit(app.exec_())
    