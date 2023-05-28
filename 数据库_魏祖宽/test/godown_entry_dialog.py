#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main_godown_entry_dialog
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QDateEdit
from PyQt5.QtCore import pyqtSignal, QDateTime


class GodownEntryDialog(QDialog, main_godown_entry_dialog.Ui_Dialog):
    _dataSignal = pyqtSignal(type({}))

    def __init__(self, parentNew=None):
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.dateTimeEdit_gmdate.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.pushButton_submit.clicked.connect(self.data_slot)
        self.pushButton_exit.clicked.connect(self.close_slot)

    def fill_data(self, record):
        """
        父窗口传入子窗口数据
        :param record: tuple
        :return: None
        """
        self.lineEdit_gmno.setText(record[0])
        time = QDateTime.fromString(record[1], "yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_gmdate.setDateTime(time)
        self.lineEdit_gmname.setText(record[2])


    def data_slot(self):
        data = {'gmno': "{}".format(self.lineEdit_gmno.text()),
                'gmdate': "'{}'".format(self.dateTimeEdit_gmdate.text()),
                'gmname': "'{}'".format(self.lineEdit_gmname.text()),
                }
        self._dataSignal.emit(data)
        self.close()

    def close_slot(self):
        self.close()
