#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_user_doctor_control import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication

class UserDoctorControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,admin,parentWindow=None):
        self.parentWindow=parentWindow
        self.username=admin
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)
        self.label_welcome.setText("欢迎，"+self.username)

    @pyqtSlot()
    def on_pushButton_current_register_clicked(self):
        import user_doctor_current_register
        self.doctor_current_register=user_doctor_current_register.DoctorCurrentRegisterView(self)
        self.hide()
        self.doctor_current_register.show()

    @pyqtSlot()
    def on_pushButton_my_register_clicked(self):
        import user_doctor_my_register
        self.doctor_my_register=user_doctor_my_register.DoctorMyRegisterView(self.username,self)
        self.hide()
        self.doctor_my_register.show()


    @pyqtSlot()
    def on_pushButton_diagnosis_clicked(self):
        import user_doctor_diagnosis
        self.doctor_diagnosis=user_doctor_diagnosis.DoctorDiagnosisView(self.username,self)
        self.hide()
        self.doctor_diagnosis.show()

    @pyqtSlot()
    def on_pushButton_user_clicked(self):
        import user_doctor_infomation
        self.user_doctor_imfomation = user_doctor_infomation.UserDoctorInfoDialog(self.username,self)
        self.hide()
        self.user_doctor_imfomation.show()

    @pyqtSlot()
    def on_pushButton_exit_clicked(self):
        QCoreApplication.quit()

    @pyqtSlot()
    def on_pushButton_switch_clicked(self):
        self.close()
        self.parentWindow.lineEdit_username.clear()
        self.parentWindow.lineEdit_password.clear()
        self.parentWindow.show()

if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=UserDoctorControlDialog("doc_nishi")
    window.show()
    sys.exit(app.exec_())