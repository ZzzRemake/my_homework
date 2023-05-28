#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_recipe_master_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class RecipeMasterDialog(QDialog, main_recipe_master_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_rmtime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_rmno.setText(record[0])
        self.lineEdit_dgno.setText(record[1])
        self.lineEdit_dno.setText(record[2])
        self.lineEdit_pno.setText(record[3])
        self.lineEdit_rmage.setText(record[4])
        time = QDateTime.fromString(record[5], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_rmtime.setDateTime(time)



    def data_slot(self):
        data = {'rmno': "{}".format(self.lineEdit_rmno.text()),
                'dgno': "{}".format(self.lineEdit_dgno.text()),
                'dno': "{}".format(self.lineEdit_dno.text()),
                'pno': "{}".format(self.lineEdit_pno.text()),
                'rmage': "{}".format(self.lineEdit_rmage.text()),
                'rmtime': "'{}'".format(self.dateTimeEdit_rmtime.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
