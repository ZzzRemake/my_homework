#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_salary_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class SalaryDialog(QDialog, main_salary_dialog.Ui_Dialog):
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
        self.lineEdit_sno.setText(record[0])
        self.lineEdit_slevel.setText(record[1])
        self.lineEdit_snumber.setText(record[2])

    def data_slot(self):
        data = {'sno': "{}".format(self.lineEdit_sno.text()),
                'slevel': "'{}'".format(self.lineEdit_slevel.text()),
                'snumber': "{}".format(self.lineEdit_snumber.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
