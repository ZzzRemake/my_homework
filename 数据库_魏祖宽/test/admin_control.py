#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_user_control import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication

class UserControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parentWindow=None):
        self.parentWindow=parentWindow
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_root_clicked(self):
        import password_dialog as root_dialog
        self.root_dialog=root_dialog.PasswordDialog("root","root",self)
        self.hide()
        self.root_dialog.show()

    @pyqtSlot()
    def on_pushButton_doctor_clicked(self):
        import admin_doctor_view
        self.admin_doctor_view=admin_doctor_view.AdminDoctorView(self)
        self.hide()
        self.admin_doctor_view.show()


    @pyqtSlot()
    def on_pushButton_patient_clicked(self):
        import admin_patient_view
        self.admin_patient_view=admin_patient_view.AdminPatientView(self)
        self.hide()
        self.admin_patient_view.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
