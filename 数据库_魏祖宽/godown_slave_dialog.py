#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_godown_slave_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class GodownSlaveDialog(QDialog, main_godown_slave_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_gsexpdate.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_gsno.setText(record[0])
        self.lineEdit_gmno.setText(record[1])
        self.lineEdit_mno.setText(record[2])
        self.lineEdit_gsnumber.setText(record[3])
        self.lineEdit_gsunit.setText(record[4])
        self.lineEdit_gsbatch.setText(record[5])
        self.lineEdit_gsprice.setText(record[6])
        time = QDateTime.fromString(record[7], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_gsexpdate.setDateTime(time)

    def data_slot(self):
        print(self.dateTimeEdit_gsexpdate.text())
        data = {'gsno': "{}".format(self.lineEdit_gsno.text()),
                'gmno': "{}".format(self.lineEdit_gmno.text()),
                'mno': "{}".format(self.lineEdit_mno.text()),
                'gsnumber': "{}".format(self.lineEdit_gsnumber.text()),
                'gsunit': "'{}'".format(self.lineEdit_gsunit.text()),
                'gsbatch': "'{}'".format(self.lineEdit_gsbatch.text()),
                'gsprice': "{}".format(self.lineEdit_gsprice.text()),
                'gsexpdate': "'{}'".format(self.dateTimeEdit_gsexpdate.text())
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
