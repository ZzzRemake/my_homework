#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
login module to deal with main_login.py
"""
from PyQt5 import QtWidgets
import pymysql
from pymysql.constants import CLIENT
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt

from main_password_dialog import Ui_Dialog


class PasswordDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self,username="",userType='root', parent=None):
        self.username=username
        self.parentWindow=parent
        self.userType=userType
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.lineEdit_newpwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_newpwd_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_oldpwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.main_window = None

        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()

    @pyqtSlot()
    def on_pushButton_submit_clicked(self):
        oldpwd = self.lineEdit_oldpwd.text()
        if self.userType=='root':
            sql = "SELECT type FROM `cs2347.administrator` WHERE " \
                  "`user`='{0}' and `password`= md5('{1}');".format(self.userType, oldpwd)
        elif self.userType=='doctor':
            sql = "SELECT dno FROM `cs2347.doctor` WHERE " \
                  "dadmin='{0}' and dpwd=md5('{1}')".format(self.username,oldpwd)
        elif self.userType=='patient':
            sql = "SELECT pno FROM `cs2347.patient` WHERE " \
                  "padmin='{0}' and ppwd=md5('{1}')".format(self.username,oldpwd)
        print(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 1:
            newpwd=self.lineEdit_newpwd.text()
            newpwd_2=self.lineEdit_newpwd_2.text()
            print(sql)
            if newpwd==newpwd_2:
                try:
                    print(newpwd,len(newpwd))
                    sql = "UPDATE `cs2347.administrator` SET" \
                          " `password`=md5('{0}') WHERE `user`='{1}'; ".format(newpwd,self.username)
                    self.cursor.execute(sql)
                    print(sql)
                    self.db.commit()
                    if self.userType=="doctor":
                        sql = "UPDATE `cs2347.doctor` SET" \
                              " `dpwd`=md5('{0}') WHERE `dadmin`='{1}'; ".format(newpwd,self.username)
                    elif self.userType == "patient":
                        sql = "UPDATE `cs2347.patient` SET" \
                              " `ppwd`=md5('{0}') WHERE `padmin`='{1}'; ".format(newpwd,self.username)

                    if self.userType != "root":
                        print(sql)
                        self.cursor.execute(sql)
                        self.db.commit()

                    self.lineEdit_newpwd.clear()
                    self.lineEdit_newpwd_2.clear()
                    self.lineEdit_oldpwd.clear()
                    self.label.setText("设置密码成功！")
                except:
                    self.db.rollback()
            else:
                self.label.setText("两次输入的新密码不同！")
        else:
            self.lineEdit_newpwd.clear()
            self.lineEdit_newpwd_2.clear()
            self.lineEdit_oldpwd.clear()
            self.label.setText("旧密码错误！")

    @pyqtSlot()
    def on_pushButton_exit_clicked(self):
        self.close()
        self.parentWindow.show()
