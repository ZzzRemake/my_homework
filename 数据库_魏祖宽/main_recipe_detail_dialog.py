# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_recipe_detail_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 445)
        self.groupBox_total = QtWidgets.QGroupBox(Dialog)
        self.groupBox_total.setGeometry(QtCore.QRect(0, 0, 420, 391))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_total.setFont(font)
        self.groupBox_total.setTitle("")
        self.groupBox_total.setObjectName("groupBox_total")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_total)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_rdno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_rdno.setFont(font)
        self.groupBox_rdno.setTitle("")
        self.groupBox_rdno.setObjectName("groupBox_rdno")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.groupBox_rdno)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_rdno = QtWidgets.QLabel(self.groupBox_rdno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_rdno.setFont(font)
        self.label_rdno.setObjectName("label_rdno")
        self.horizontalLayout_19.addWidget(self.label_rdno)
        self.lineEdit_rdno = QtWidgets.QLineEdit(self.groupBox_rdno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_rdno.setFont(font)
        self.lineEdit_rdno.setObjectName("lineEdit_rdno")
        self.horizontalLayout_19.addWidget(self.lineEdit_rdno)
        self.verticalLayout_2.addWidget(self.groupBox_rdno)
        self.groupBox_rmno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_rmno.setFont(font)
        self.groupBox_rmno.setTitle("")
        self.groupBox_rmno.setObjectName("groupBox_rmno")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.groupBox_rmno)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_rmno = QtWidgets.QLabel(self.groupBox_rmno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_rmno.setFont(font)
        self.label_rmno.setObjectName("label_rmno")
        self.horizontalLayout_20.addWidget(self.label_rmno)
        self.lineEdit_rmno = QtWidgets.QLineEdit(self.groupBox_rmno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_rmno.setFont(font)
        self.lineEdit_rmno.setObjectName("lineEdit_rmno")
        self.horizontalLayout_20.addWidget(self.lineEdit_rmno)
        self.verticalLayout_2.addWidget(self.groupBox_rmno)
        self.groupBox_mno = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_mno.setFont(font)
        self.groupBox_mno.setTitle("")
        self.groupBox_mno.setObjectName("groupBox_mno")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.groupBox_mno)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_mno = QtWidgets.QLabel(self.groupBox_mno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_mno.setFont(font)
        self.label_mno.setObjectName("label_mno")
        self.horizontalLayout_21.addWidget(self.label_mno)
        self.lineEdit_mno = QtWidgets.QLineEdit(self.groupBox_mno)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_mno.setFont(font)
        self.lineEdit_mno.setObjectName("lineEdit_mno")
        self.horizontalLayout_21.addWidget(self.lineEdit_mno)
        self.verticalLayout_2.addWidget(self.groupBox_mno)
        self.groupBox_rdprice = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_rdprice.setFont(font)
        self.groupBox_rdprice.setTitle("")
        self.groupBox_rdprice.setObjectName("groupBox_rdprice")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.groupBox_rdprice)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_rdprice = QtWidgets.QLabel(self.groupBox_rdprice)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_rdprice.setFont(font)
        self.label_rdprice.setObjectName("label_rdprice")
        self.horizontalLayout_26.addWidget(self.label_rdprice)
        self.lineEdit_rdprice = QtWidgets.QLineEdit(self.groupBox_rdprice)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_rdprice.setFont(font)
        self.lineEdit_rdprice.setObjectName("lineEdit_rdprice")
        self.horizontalLayout_26.addWidget(self.lineEdit_rdprice)
        self.verticalLayout_2.addWidget(self.groupBox_rdprice)
        self.groupBox_rdnumber = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_rdnumber.setFont(font)
        self.groupBox_rdnumber.setTitle("")
        self.groupBox_rdnumber.setObjectName("groupBox_rdnumber")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.groupBox_rdnumber)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_rdnumber = QtWidgets.QLabel(self.groupBox_rdnumber)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_rdnumber.setFont(font)
        self.label_rdnumber.setObjectName("label_rdnumber")
        self.horizontalLayout_24.addWidget(self.label_rdnumber)
        self.lineEdit_rdnumber = QtWidgets.QLineEdit(self.groupBox_rdnumber)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_rdnumber.setFont(font)
        self.lineEdit_rdnumber.setObjectName("lineEdit_rdnumber")
        self.horizontalLayout_24.addWidget(self.lineEdit_rdnumber)
        self.verticalLayout_2.addWidget(self.groupBox_rdnumber)
        self.groupBox_rdunit = QtWidgets.QGroupBox(self.groupBox_total)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_rdunit.setFont(font)
        self.groupBox_rdunit.setTitle("")
        self.groupBox_rdunit.setObjectName("groupBox_rdunit")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.groupBox_rdunit)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_rdunit = QtWidgets.QLabel(self.groupBox_rdunit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_rdunit.setFont(font)
        self.label_rdunit.setObjectName("label_rdunit")
        self.horizontalLayout_25.addWidget(self.label_rdunit)
        self.lineEdit_rdunit = QtWidgets.QLineEdit(self.groupBox_rdunit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_rdunit.setFont(font)
        self.lineEdit_rdunit.setObjectName("lineEdit_rdunit")
        self.horizontalLayout_25.addWidget(self.lineEdit_rdunit)
        self.verticalLayout_2.addWidget(self.groupBox_rdunit)
        self.pushButton_submit = QtWidgets.QPushButton(Dialog)
        self.pushButton_submit.setGeometry(QtCore.QRect(20, 390, 150, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_submit.setFont(font)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_exit = QtWidgets.QPushButton(Dialog)
        self.pushButton_exit.setGeometry(QtCore.QRect(250, 390, 150, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_rdno.setText(_translate("Dialog", "处方药品清单编号"))
        self.label_rmno.setText(_translate("Dialog", "所属处方编号"))
        self.label_mno.setText(_translate("Dialog", "药品编号"))
        self.label_rdprice.setText(_translate("Dialog", "价格"))
        self.label_rdnumber.setText(_translate("Dialog", "数量"))
        self.label_rdunit.setText(_translate("Dialog", "数量单位"))
        self.pushButton_submit.setText(_translate("Dialog", "确认"))
        self.pushButton_exit.setText(_translate("Dialog", "返回"))
