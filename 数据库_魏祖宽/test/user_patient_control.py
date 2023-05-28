#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_user_patient_control import Ui_Dialog
from PyQt5 import QtWidgets

from PyQt5.QtCore import pyqtSlot,QCoreApplication

class UserPatientControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,admin,parentWindow=None):
        self.parentWindow=parentWindow
        self.username=admin
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)
        self.label_welcome.setText("欢迎，"+self.username)

    @pyqtSlot()
    def on_pushButton_register_clicked(self):
        import user_patient_register
        self.user_patient_register=user_patient_register.UserPatientRegisterDialog(self.username,self)
        self.hide()
        self.user_patient_register.show()

    @pyqtSlot()
    def on_pushButton_diagnosis_clicked(self):
        import user_patient_diagnosis
        self.patient_diagnosis=user_patient_diagnosis.PatientDiagnosisView(self.username,self)
        self.hide()
        self.patient_diagnosis.show()


    @pyqtSlot()
    def on_pushButton_fee_clicked(self):
        import user_patient_fee
        self.fee_window=user_patient_fee.PatientFeeView(self.username,self)
        self.hide()
        self.fee_window.show()

    @pyqtSlot()
    def on_pushButton_user_clicked(self):
        import user_patient_infomation
        self.user_patient_infomation = user_patient_infomation.UserPatientInfoDialog(self.username,self)
        self.hide()
        self.user_patient_infomation.show()

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
    window=UserPatientControlDialog("p_test")
    window.show()
    sys.exit(app.exec_())