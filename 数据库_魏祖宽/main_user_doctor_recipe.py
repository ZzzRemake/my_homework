# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_user_doctor_recipe.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(401, 334)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 401, 281))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_back.setGeometry(QtCore.QRect(100, 280, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName("pushButton_back")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_back.setText(_translate("Dialog", "返回"))
