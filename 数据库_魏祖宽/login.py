#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
login module to deal with main_login.py
"""
from PyQt5 import QtWidgets
import pymysql
from pymysql.constants import CLIENT
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt
from main_login import Ui_Dialog

import root as Root_MainWindow
import user_doctor_control as User_DoctorDialog
import user_patient_control as User_PatientDialog

class DialogLogin(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.main_window=None
        
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        
        self.pushButton_2.clicked.connect(QCoreApplication.quit)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        username=self.lineEdit_username.text()
        password=self.lineEdit_password.text()
        
        sql = "SELECT * FROM `cs2347.administrator` WHERE " \
              "`user`='{0}' and `password`= md5('{1}');".format(username, password)
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        userType=None
        if len(data)==1:
            userType=data[0][2]
        
        if userType:
            print(data)
            self.label_error.clear()
            print("login success")
            print(userType)
            self.hide()
            if userType=="root":
                self.main_window=Root_MainWindow.rootWindow(self)
                self.main_window.show()
            elif userType=="doctor":
                self.main_window=User_DoctorDialog.UserDoctorControlDialog(username,self)
                self.main_window.show()
            elif userType=="patient":
                self.main_window=User_PatientDialog.UserPatientControlDialog(username,self)
                self.main_window.show()
        else:
            print("failed!")
            self.label_error.setText("用户名或密码错误！")

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        QCoreApplication.quit()

if __name__=="__main__":
    import sys
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app=QtWidgets.QApplication(sys.argv)
    dlg=DialogLogin()
    dlg.show()
    sys.exit(app.exec_())