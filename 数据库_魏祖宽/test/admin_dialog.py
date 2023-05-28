#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_admin_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class AdminDialog(QDialog, main_admin_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_username.setText(record[0])
        self.lineEdit_password.setText(record[1])

    def data_slot(self):
        data = {'username': "'{}'".format(self.lineEdit_username.text()),
                'password': "'{}'".format(self.lineEdit_password.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
