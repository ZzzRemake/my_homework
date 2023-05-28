#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_register_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class RegisterDialog(QDialog, main_register_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_rftime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_rfvisittime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_rfno.setText(record[0])
        self.lineEdit_rfdept.setText(record[1])
        self.lineEdit_rfdoctor.setText(record[2])
        self.lineEdit_rfpatient.setText(record[3])
        self.lineEdit_rfcashier.setText(record[4])
        time = QDateTime.fromString(record[5], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_rftime.setDateTime(time)
        Vtime = QDateTime.fromString(record[6], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_rfvisittime.setDateTime(Vtime)
        self.lineEdit_rfnotes.setText(record[7])


    def data_slot(self):
        data = {'rfno': "{}".format(self.lineEdit_rfno.text()),
                'rfdept': "{}".format(self.lineEdit_rfdept.text()),
                'rfdoctor': "{}".format(self.lineEdit_rfdoctor.text()),
                'rfpatient': "{}".format(self.lineEdit_rfpatient.text()),
                'rfcashier': "{}".format(self.lineEdit_rfcashier.text()),
                'rftime': "'{}'".format(self.dateTimeEdit_rftime.text()),
                'rfvisittime': "'{}'".format(self.dateTimeEdit_rfvisittime.text()),
                'rfnotes': "'{}'".format(self.lineEdit_rfnotes.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
