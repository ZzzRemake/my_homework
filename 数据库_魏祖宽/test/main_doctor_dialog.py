# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_doctor_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(532, 504)
        self.groupBox_total = QtWidgets.QGroupBox(Dialog)
        self.groupBox_total.setGeometry(QtCore.QRect(0, 0, 531, 431))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_total.setFont(font)
        self.groupBox_total.setTitle("")
        self.groupBox_total.setObjectName("groupBox_total")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_total)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_dno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dno.setFont(font)
        self.groupBox_dno.setTitle("")
        self.groupBox_dno.setObjectName("groupBox_dno")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_dno)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_dno = QtWidgets.QLabel(self.groupBox_dno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dno.setFont(font)
        self.label_dno.setObjectName("label_dno")
        self.horizontalLayout_8.addWidget(self.label_dno)
        self.lineEdit_dno = QtWidgets.QLineEdit(self.groupBox_dno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_dno.setFont(font)
        self.lineEdit_dno.setObjectName("lineEdit_dno")
        self.horizontalLayout_8.addWidget(self.lineEdit_dno)
        self.verticalLayout.addWidget(self.groupBox_dno)
        self.groupBox_dname = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dname.setFont(font)
        self.groupBox_dname.setTitle("")
        self.groupBox_dname.setObjectName("groupBox_dname")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_dname)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_dname = QtWidgets.QLabel(self.groupBox_dname)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dname.setFont(font)
        self.label_dname.setObjectName("label_dname")
        self.horizontalLayout_9.addWidget(self.label_dname)
        self.lineEdit_dname = QtWidgets.QLineEdit(self.groupBox_dname)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_dname.setFont(font)
        self.lineEdit_dname.setObjectName("lineEdit_dname")
        self.horizontalLayout_9.addWidget(self.lineEdit_dname)
        self.verticalLayout.addWidget(self.groupBox_dname)
        self.groupBox_dsex = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dsex.setFont(font)
        self.groupBox_dsex.setTitle("")
        self.groupBox_dsex.setObjectName("groupBox_dsex")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupBox_dsex)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_dsex = QtWidgets.QLabel(self.groupBox_dsex)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dsex.setFont(font)
        self.label_dsex.setObjectName("label_dsex")
        self.horizontalLayout_10.addWidget(self.label_dsex)
        self.comboBox_dsex = QtWidgets.QComboBox(self.groupBox_dsex)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_dsex.setFont(font)
        self.comboBox_dsex.setObjectName("comboBox_dsex")
        self.comboBox_dsex.addItem("")
        self.comboBox_dsex.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox_dsex)
        self.verticalLayout.addWidget(self.groupBox_dsex)
        self.groupBox_dage = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dage.setFont(font)
        self.groupBox_dage.setTitle("")
        self.groupBox_dage.setObjectName("groupBox_dage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_dage)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_dage = QtWidgets.QLabel(self.groupBox_dage)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dage.setFont(font)
        self.label_dage.setObjectName("label_dage")
        self.horizontalLayout_4.addWidget(self.label_dage)
        self.lineEdit_dage = QtWidgets.QLineEdit(self.groupBox_dage)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_dage.setFont(font)
        self.lineEdit_dage.setObjectName("lineEdit_dage")
        self.horizontalLayout_4.addWidget(self.lineEdit_dage)
        self.verticalLayout.addWidget(self.groupBox_dage)
        self.groupBox_deptno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_deptno.setFont(font)
        self.groupBox_deptno.setTitle("")
        self.groupBox_deptno.setObjectName("groupBox_deptno")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_deptno)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_deptno = QtWidgets.QLabel(self.groupBox_deptno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_deptno.setFont(font)
        self.label_deptno.setObjectName("label_deptno")
        self.horizontalLayout_3.addWidget(self.label_deptno)
        self.lineEdit_deptno = QtWidgets.QLineEdit(self.groupBox_deptno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_deptno.setFont(font)
        self.lineEdit_deptno.setObjectName("lineEdit_deptno")
        self.horizontalLayout_3.addWidget(self.lineEdit_deptno)
        self.verticalLayout.addWidget(self.groupBox_deptno)
        self.groupBox_dtno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dtno.setFont(font)
        self.groupBox_dtno.setTitle("")
        self.groupBox_dtno.setObjectName("groupBox_dtno")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_dtno)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_dtno = QtWidgets.QLabel(self.groupBox_dtno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dtno.setFont(font)
        self.label_dtno.setObjectName("label_dtno")
        self.horizontalLayout_2.addWidget(self.label_dtno)
        self.lineEdit_dtno = QtWidgets.QLineEdit(self.groupBox_dtno)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_dtno.setFont(font)
        self.lineEdit_dtno.setObjectName("lineEdit_dtno")
        self.horizontalLayout_2.addWidget(self.lineEdit_dtno)
        self.verticalLayout.addWidget(self.groupBox_dtno)
        self.groupBox_dadmin = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_dadmin.setFont(font)
        self.groupBox_dadmin.setTitle("")
        self.groupBox_dadmin.setObjectName("groupBox_dadmin")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_dadmin)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_dadmin = QtWidgets.QLabel(self.groupBox_dadmin)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_dadmin.setFont(font)
        self.label_dadmin.setObjectName("label_dadmin")
        self.horizontalLayout.addWidget(self.label_dadmin)
        self.lineEdit_dadmin = QtWidgets.QLineEdit(self.groupBox_dadmin)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_dadmin.setFont(font)
        self.lineEdit_dadmin.setObjectName("lineEdit_dadmin")
        self.horizontalLayout.addWidget(self.lineEdit_dadmin)
        self.verticalLayout.addWidget(self.groupBox_dadmin)
        self.pushButton_submit = QtWidgets.QPushButton(Dialog)
        self.pushButton_submit.setGeometry(QtCore.QRect(70, 450, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_submit.setFont(font)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_exit = QtWidgets.QPushButton(Dialog)
        self.pushButton_exit.setGeometry(QtCore.QRect(320, 450, 150, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_dno.setText(_translate("Dialog", "医生编号"))
        self.label_dname.setText(_translate("Dialog", "医生姓名"))
        self.label_dsex.setText(_translate("Dialog", "性别"))
        self.comboBox_dsex.setItemText(0, _translate("Dialog", "男"))
        self.comboBox_dsex.setItemText(1, _translate("Dialog", "女"))
        self.label_dage.setText(_translate("Dialog", "年龄"))
        self.label_deptno.setText(_translate("Dialog", "所属部门编号"))
        self.label_dtno.setText(_translate("Dialog", "职位编号"))
        self.label_dadmin.setText(_translate("Dialog", "登录用户名（空置表示无登录账户）"))
        self.pushButton_submit.setText(_translate("Dialog", "提交"))
        self.pushButton_exit.setText(_translate("Dialog", "返回"))
