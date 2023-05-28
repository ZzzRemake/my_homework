#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_patient_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDate


class PatientDialogInsert(QDialog, main_patient_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateEdit_pbd.setDisplayFormat("yyyy-MM-dd")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_pno.setText(record[0])
        self.lineEdit_pname.setText(record[1])
        self.lineEdit_pid.setText(record[2])
        self.lineEdit_pino.setText(record[3])
        self.lineEdit_pmno.setText(record[4])
        self.comboBox_psex.setCurrentText(record[5])
        time=QDate.fromString(record[6],"yyyy-MM-dd")
        self.dateEdit_pbd.setDate(time)
        self.lineEdit_padd.setText(record[7])
        self.lineEdit_ptno.setText(record[8])
        self.lineEdit_pteltype.setText(record[9])
        self.lineEdit_ptelcode.setText(record[10])

    def data_slot(self):
        data = {'pno': "{}".format(self.lineEdit_pno.text()),
                'pname': "'{}'".format(self.lineEdit_pname.text()),
                'pid': "'{}'".format(self.lineEdit_pid.text()),
                'pino': "'{}'".format(self.lineEdit_pino.text()),
                'pmno': "'{}'".format(self.lineEdit_pmno.text()),
                'psex': "'{}'".format(self.comboBox_psex.currentText()),
                'pbd': "'{}'".format(self.dateEdit_pbd.text()),
                'padd': "'{}'".format(self.lineEdit_padd.text()),
                'ptno': "{}".format(self.lineEdit_ptno.text()),
                'pteltype': "'{}'".format(self.lineEdit_pteltype.text()),
                'ptelcode': "'{}'".format(self.lineEdit_ptelcode.text())}
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
