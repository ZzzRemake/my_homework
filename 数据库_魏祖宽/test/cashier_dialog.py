#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_cashier_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class CashierDialog(QDialog, main_cashier_dialog.Ui_Dialog):
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
        self.lineEdit_cashno.setText(record[0])
        self.lineEdit_cashname.setText(record[1])
        self.lineEdit_cashage.setText(record[2])
        self.comboBox_cashsex.setCurrentText(record[3])
        self.lineEdit_cashcertno.setText(record[4])

    def data_slot(self):
        data = {'cashno': "{}".format(self.lineEdit_cashno.text()),
                'cashname': "'{}'".format(self.lineEdit_cashname.text()),
                'cashage': "{}".format(self.lineEdit_cashage.text()),
                'cashsex': "'{}'".format(self.comboBox_cashsex.currentText()),
                'cashcertno': "'{}'".format(self.lineEdit_cashcertno.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
