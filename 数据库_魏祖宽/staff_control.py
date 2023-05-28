#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_staff_control import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication

class StaffControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parentWindow=None):
        self.parentWindow=parentWindow
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_doctor_clicked(self):
        import doctor_view
        self.doctor_window=doctor_view.DoctorView(self)
        self.hide()
        self.doctor_window.show()

    @pyqtSlot()
    def on_pushButton_cashier_clicked(self):
        import cashier_view
        self.cashier_window=cashier_view.CashierView(self)
        self.hide()
        print("cash")
        self.cashier_window.show()


    @pyqtSlot()
    def on_pushButton_salary_clicked(self):
        import salary_view
        self.salary_window=salary_view.SalaryView(self)
        self.hide()
        self.salary_window.show()

    @pyqtSlot()
    def on_pushButton_title_clicked(self):
        import title_view
        self.title_window = title_view.TitleView(self)
        self.hide()
        self.title_window.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
