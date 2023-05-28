#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT

import main_user_doctor_infomation
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QPushButton
from PyQt5.QtCore import pyqtSlot, QDate, QCoreApplication


class UserDoctorInfoDialog(QDialog, main_user_doctor_infomation.Ui_Dialog):

    def __init__(self,username, parentNew=None):
        self.username=username
        self.parentWindow = parentNew
        self.isChange=False
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        sql="""
            SELECT doctor.dno,doctor.dname,doctor.dsex,doctor.dage,dept.deptname,title.ttype
            FROM  `cs2347.doctor` doctor,`cs2347.dept` dept,`cs2347.title` title
            WHERE doctor.dadmin='{0}' AND doctor.deptno=dept.deptno AND doctor.dtno=title.tno
        """.format(self.username)
        print(sql)
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        if len(data)==1:
            self.fill_data(data[0])

        self.set_edit_status()

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_dno.setText(str(record[0]))
        self.lineEdit_dname.setText(record[1])
        self.comboBox_dsex.setCurrentText(str(record[2]))
        self.lineEdit_dage.setText(str(record[3]))
        self.lineEdit_dept.setText(record[4])
        self.lineEdit_title.setText(record[5])

    def set_edit_status(self)->None:
        self.lineEdit_dno.setEnabled(False)
        self.lineEdit_dname.setEnabled(self.isChange)
        self.comboBox_dsex.setEnabled(self.isChange)
        self.lineEdit_dage.setEnabled(self.isChange)
        self.lineEdit_dept.setEnabled(False)
        self.lineEdit_title.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        _translate = QCoreApplication.translate
        self.isChange = not self.isChange
        self.set_edit_status()
        if self.isChange==False:
            self.pushButton_edit.setText(_translate("Dialog","编辑资料"))
            dname=self.lineEdit_dname.text()
            dsex=self.comboBox_dsex.currentText()
            dage=self.lineEdit_dage.text()
            sql="""
                UPDATE `cs2347.doctor` SET dname='{0}',dsex='{1}',
                dage={2} WHERE dadmin='{3}'
            """.format(dname,dsex,dage,self.username)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except Exception:
                print(Exception)
                self.db.rollback()
        else:
            self.pushButton_edit.setText(_translate("Dialog","提交编辑"))

    @pyqtSlot()
    def on_pushButton_password_clicked(self):
        import password_dialog
        self.password_dialog=password_dialog.PasswordDialog(self.username,"doctor",self)
        self.hide()
        self.password_dialog.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
