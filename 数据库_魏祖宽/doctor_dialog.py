#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_doctor_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class DoctorDialog(QDialog, main_doctor_dialog.Ui_Dialog):
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
        self.lineEdit_dno.setText(record[0])
        self.lineEdit_dname.setText(record[1])
        self.comboBox_dsex.setCurrentText(record[2])
        self.lineEdit_dage.setText(record[3])
        self.lineEdit_deptno.setText(record[4])
        self.lineEdit_dtno.setText(record[5])
        self.lineEdit_dtno.setText(record[6])

    def data_slot(self):
        data = {'dno': "{}".format(self.lineEdit_dno.text()),
                'dname': "'{}'".format(self.lineEdit_dname.text()),
                'dsex': "'{}'".format(self.comboBox_dsex.currentText()),
                'dage': "{}".format(self.lineEdit_dage.text()),
                'deptno': "{}".format(self.lineEdit_deptno.text()),
                'dtno': "{}".format(self.lineEdit_dtno.text()),
                'dadmin':"'{}'".format(self.lineEdit_dadmin.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
