#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT

import main_user_patient_infomation
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateEdit
from PyQt5.QtCore import pyqtSlot, QDate, QCoreApplication


class UserPatientInfoDialog(QDialog, main_user_patient_infomation.Ui_Dialog):

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
            SELECT patient.pno,patient.pname,patient.psex,patient.pbd,patient.pid,
            patient.pino,patient.pmno,patient.padd,patient_tel.pteltype,patient_tel.ptelcode
            FROM  `cs2347.patient` patient,`cs2347.patient_tel` patient_tel
            WHERE patient.padmin='{0}' AND patient_tel.pno=patient.pno
        """.format(self.username)
        print(sql)
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        print(data)
        if len(data)>=1:
            self.fill_data(data[0])

        self.set_edit_status()

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_pno.setText(str(record[0]))
        self.lineEdit_pname.setText(record[1])
        self.comboBox_psex.setCurrentText(str(record[2]))
        time=QDate.fromString(record[3].strftime('%Y-%m-%d %H:%M:%S'),"yyyy-MM-dd")
        self.dateEdit_pbd.setDate(time)
        self.lineEdit_pid.setText(record[4])
        self.lineEdit_pino.setText(record[5])
        self.lineEdit_pmno.setText(record[6])
        self.lineEdit_padd.setText(record[7])
        self.lineEdit_pteltype.setText(record[8])
        self.lineEdit_ptelcode.setText(record[9])

    def set_edit_status(self)->None:
        self.lineEdit_pno.setEnabled(False)
        self.lineEdit_pname.setEnabled(self.isChange)
        self.comboBox_psex.setEnabled(False)
        self.dateEdit_pbd.setEnabled(False)
        self.lineEdit_pid.setEnabled(False)
        self.lineEdit_pino.setEnabled(self.isChange)
        self.lineEdit_pmno.setEnabled(self.isChange)
        self.lineEdit_padd.setEnabled(self.isChange)
        self.lineEdit_pteltype.setEnabled(self.isChange)
        self.lineEdit_ptelcode.setEnabled(self.isChange)

    @pyqtSlot()
    def on_pushButton_edit_clicked(self):
        _translate = QCoreApplication.translate
        self.isChange = not self.isChange
        self.set_edit_status()
        if self.isChange==False:
            self.pushButton_edit.setText(_translate("Dialog","编辑资料"))
            pname=self.lineEdit_pname.text()
            psex=self.comboBox_psex.currentText()
            pino=self.lineEdit_pino.text()
            pmno=self.lineEdit_pmno.text()
            padd=self.lineEdit_padd.text()
            pteltype=self.lineEdit_pteltype.text()
            ptelcode=self.lineEdit_ptelcode.text()

            try:
                sql="""
                    UPDATE `cs2347.patient` SET pname='{0}',psex='{1}',
                    pino='{2}', pmno='{3}', padd='{4}' WHERE padmin='{5}'
                """.format(pname,psex,pino,pmno,padd,self.username)
                self.cursor.execute(sql)
                self.db.commit()
                sql="""
                    UPDATE `cs2347.patient_tel` SET ptelcode='{0}',pteltype='{1}'
                     WHERE `cs2347.patient`.padmin='{2}' AND `cs2347.patient`.pno=`cs2347.patient_tel`.pno
                """.format(ptelcode,pteltype,self.username)
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
        self.password_dialog=password_dialog.PasswordDialog(self.username,"patient",self)
        self.hide()
        self.password_dialog.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
