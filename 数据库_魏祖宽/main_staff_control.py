# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_staff_control.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(502, 287)
        self.pushButton_doctor = QtWidgets.QPushButton(Dialog)
        self.pushButton_doctor.setGeometry(QtCore.QRect(0, 0, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_doctor.setFont(font)
        self.pushButton_doctor.setObjectName("pushButton_doctor")
        self.pushButton_cashier = QtWidgets.QPushButton(Dialog)
        self.pushButton_cashier.setGeometry(QtCore.QRect(0, 70, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_cashier.setFont(font)
        self.pushButton_cashier.setObjectName("pushButton_cashier")
        self.pushButton_salary = QtWidgets.QPushButton(Dialog)
        self.pushButton_salary.setGeometry(QtCore.QRect(0, 140, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_salary.setFont(font)
        self.pushButton_salary.setObjectName("pushButton_salary")
        self.pushButton_title = QtWidgets.QPushButton(Dialog)
        self.pushButton_title.setGeometry(QtCore.QRect(0, 210, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton_title.setFont(font)
        self.pushButton_title.setObjectName("pushButton_title")
        self.pushButton_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_back.setGeometry(QtCore.QRect(270, 170, 200, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName("pushButton_back")
        self.label_welcome = QtWidgets.QLabel(Dialog)
        self.label_welcome.setGeometry(QtCore.QRect(270, 70, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_welcome.setFont(font)
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_welcome.setObjectName("label_welcome")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_doctor.setText(_translate("Dialog", "医生"))
        self.pushButton_cashier.setText(_translate("Dialog", "收银员"))
        self.pushButton_salary.setText(_translate("Dialog", "工资"))
        self.pushButton_title.setText(_translate("Dialog", "职称"))
        self.pushButton_back.setText(_translate("Dialog", "返回"))
        self.label_welcome.setText(_translate("Dialog", "员工管理"))
