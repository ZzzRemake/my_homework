#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_fee_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class FeeDialog(QDialog, main_fee_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_fdate.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_fno.setText(record[0])
        self.lineEdit_fnumber.setText(record[1])
        Vtime = QDateTime.fromString(record[6], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_fdate.setDateTime(Vtime)
        self.lineEdit_rno.setText(record[3])
        self.lineEdit_cno.setText(record[4])
        self.lineEdit_pno.setText(record[5])
        self.lineEdit_frecipefee.setText(record[6])
        self.lineEdit_fdiscount.setText(record[7])
        self.lineEdit_fsum.setText(record[8])


    def data_slot(self):
        data = {'fno': "{}".format(self.lineEdit_fno.text()),
                'fnumber': "{}".format(self.lineEdit_fnumber.text()),
                'fdate': "'{}'".format(self.dateTimeEdit_fdate.text()),
                'rno': "{}".format(self.lineEdit_rno.text()),
                'cno': "{}".format(self.lineEdit_cno.text()),
                'pno': "'{}'".format(self.lineEdit_pno.text()),
                'frecipefee': "{}".format(self.lineEdit_frecipefee.text()),
                'fdiscount': "{}".format(self.lineEdit_fdiscount.text()),
                'fsum': "{}".format(self.lineEdit_fsum.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
