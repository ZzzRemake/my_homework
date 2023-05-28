#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_medicine_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class MedicineDialog(QDialog, main_medicine_dialog.Ui_Dialog):
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
        self.lineEdit_mno.setText(record[0])
        self.lineEdit_mname.setText(record[1])
        self.lineEdit_mprice.setText(record[2])
        self.lineEdit_munit.setText(record[3])
        self.lineEdit_mtype.setText(record[4])

    def data_slot(self):
        data = {'mno': "{}".format(self.lineEdit_mno.text()),
                'mname': "'{}'".format(self.lineEdit_mname.text()),
                'mprice': "{}".format(self.lineEdit_mprice.text()),
                'munit': "'{}'".format(self.lineEdit_munit.text()),
                'mtype': "'{}'".format(self.lineEdit_mtype.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
