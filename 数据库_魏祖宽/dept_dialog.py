#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_dept_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, QDate


class DeptDialog(QDialog, main_dept_dialog.Ui_Dialog):
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
        self.lineEdit_deptno.setText(record[0])
        self.lineEdit_deptname.setText(record[1])
        self.lineEdit_parentdeptno.setText(record[2])
        self.lineEdit_manager.setText(record[3])

    def data_slot(self):
        data = {'deptno': "{}".format(self.lineEdit_deptno.text()),
                'deptname': "'{}'".format(self.lineEdit_deptname.text()),
                'parentdeptno': "{}".format(self.lineEdit_parentdeptno.text()),
                'manager': "{}".format(self.lineEdit_manager.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
