#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_title_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class TitleDialog(QDialog, main_title_dialog.Ui_Dialog):
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
        self.lineEdit_tno.setText(record[0])
        self.lineEdit_sno.setText(record[1])
        self.lineEdit_ttype.setText(record[2])
        self.lineEdit_ttrade.setText(record[3])
        self.lineEdit_tfee.setText(record[4])

    def data_slot(self):
        data = {'tno': "{}".format(self.lineEdit_tno.text()),
                'sno': "{}".format(self.lineEdit_sno.text()),
                'ttype': "'{}'".format(self.lineEdit_ttype.text()),
                'ttrade': "'{}'".format(self.lineEdit_ttrade.text()),
                'tfee':"{}".format(self.lineEdit_tfee.text())
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
