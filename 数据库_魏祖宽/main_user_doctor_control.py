# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_user_doctor_control.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(441, 283)
        self.label_help = QtWidgets.QLabel(Dialog)
        self.label_help.setGeometry(QtCore.QRect(180, 110, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_help.setFont(font)
        self.label_help.setAlignment(QtCore.Qt.AlignCenter)
        self.label_help.setObjectName("label_help")
        self.pushButton_current_register = QtWidgets.QPushButton(Dialog)
        self.pushButton_current_register.setGeometry(QtCore.QRect(0, 0, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_current_register.setFont(font)
        self.pushButton_current_register.setObjectName("pushButton_current_register")
        self.pushButton_user = QtWidgets.QPushButton(Dialog)
        self.pushButton_user.setGeometry(QtCore.QRect(0, 210, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_user.setFont(font)
        self.pushButton_user.setObjectName("pushButton_user")
        self.label_welcome = QtWidgets.QLabel(Dialog)
        self.label_welcome.setGeometry(QtCore.QRect(180, 20, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_welcome.setFont(font)
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_welcome.setObjectName("label_welcome")
        self.pushButton_diagnosis = QtWidgets.QPushButton(Dialog)
        self.pushButton_diagnosis.setGeometry(QtCore.QRect(0, 140, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_diagnosis.setFont(font)
        self.pushButton_diagnosis.setObjectName("pushButton_diagnosis")
        self.pushButton_my_register = QtWidgets.QPushButton(Dialog)
        self.pushButton_my_register.setGeometry(QtCore.QRect(0, 70, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_my_register.setFont(font)
        self.pushButton_my_register.setObjectName("pushButton_my_register")
        self.pushButton_switch = QtWidgets.QPushButton(Dialog)
        self.pushButton_switch.setGeometry(QtCore.QRect(200, 200, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_switch.setFont(font)
        self.pushButton_switch.setObjectName("pushButton_switch")
        self.pushButton_exit = QtWidgets.QPushButton(Dialog)
        self.pushButton_exit.setGeometry(QtCore.QRect(310, 200, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_help.setText(_translate("Dialog", "点击按钮进入各管理模块！"))
        self.pushButton_current_register.setText(_translate("Dialog", "当天挂号"))
        self.pushButton_user.setText(_translate("Dialog", "个人信息"))
        self.label_welcome.setText(_translate("Dialog", "欢迎"))
        self.pushButton_diagnosis.setText(_translate("Dialog", "患者就诊"))
        self.pushButton_my_register.setText(_translate("Dialog", "我的挂号"))
        self.pushButton_switch.setText(_translate("Dialog", "切换用户"))
        self.pushButton_exit.setText(_translate("Dialog", "退出程序"))
