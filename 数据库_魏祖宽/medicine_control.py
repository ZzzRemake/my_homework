#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_medicine_control import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication

class MedicineControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parentWindow=None):
        self.parentWindow=parentWindow
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_medicine_clicked(self):
        import medicine_view
        self.medicine_window=medicine_view.MedicineView(self)
        self.hide()
        self.medicine_window.show()

    @pyqtSlot()
    def on_pushButton_godown_entry_clicked(self):
        import godown_entry_view
        self.godown_entry_window=godown_entry_view.GodownEntryView(self)
        self.hide()
        print("cash")
        self.godown_entry_window.show()


    @pyqtSlot()
    def on_pushButton_godown_slave_clicked(self):
        import godown_slave_view
        self.godown_slave_window=godown_slave_view.GodownSlaveView(self)
        self.hide()
        self.godown_slave_window.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
