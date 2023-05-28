#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_diagnosis_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class DiagnosisDialog(QDialog,  main_diagnosis_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_dgtime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_dgno.setText(record[0])
        self.lineEdit_pno.setText(record[1])
        self.lineEdit_dno.setText(record[2])
        self.lineEdit_symptom.setText(record[3])
        self.lineEdit_diagnosis.setText(record[4])
        time = QDateTime.fromString(record[5], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_dgtime.setDateTime(time)
        self.lineEdit_rfee.setText(record[6])


    def data_slot(self):
        data = {'dgno': "{}".format(self.lineEdit_dgno.text()),
                'pno': "{}".format(self.lineEdit_pno.text()),
                'dno': "{}".format(self.lineEdit_dno.text()),
                'symptom': "'{}'".format(self.lineEdit_symptom.text()),
                'diagnosis': "'{}'".format(self.lineEdit_diagnosis.text()),
                'dgtime': "'{}'".format(self.dateTimeEdit_dgtime.text()),
                'rfee': "{}".format(self.lineEdit_rfee.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
