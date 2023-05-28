#!/usr/bin/python3
# -*- coding: utf-8 -*-
import main_recipe_detail_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class RecipeDetailDialog(QDialog, main_recipe_detail_dialog.Ui_Dialog):
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
        self.lineEdit_rdno.setText(record[0])
        self.lineEdit_rmno.setText(record[1])
        self.lineEdit_mno.setText(record[2])
        self.lineEdit_rdprice.setText(record[3])
        self.lineEdit_rdnumber.setText(record[4])
        self.lineEdit_rdunit.setText(record[5])



    def data_slot(self):
        data = {'rdno': "{}".format(self.lineEdit_rdno.text()),
                'rmno': "{}".format(self.lineEdit_rmno.text()),
                'mno': "{}".format(self.lineEdit_mno.text()),
                'rdprice': "{}".format(self.lineEdit_rdprice.text()),
                'rdnumber': "{}".format(self.lineEdit_rdnumber.text()),
                'rdunit': "'{}'".format(self.lineEdit_rdunit.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
