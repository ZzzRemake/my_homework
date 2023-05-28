#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_delete_dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

class deleteDialog(QDialog,main_delete_dialog.Ui_Dialog):

    _deleteSignal=pyqtSignal()
    def __init__(self,parentNew=None):
            self.parentWindow = parentNew
            QDialog.__init__(self, parentNew)
            self.setupUi(self)

            self.pushButton_delete.clicked.connect(self.delete_slot)
            self.pushButton_exit.clicked.connect(self.close_slot)

    def delete_slot(self):
        self._deleteSignal.emit()
        self.close()
    def close_slot(self):
        self.close()