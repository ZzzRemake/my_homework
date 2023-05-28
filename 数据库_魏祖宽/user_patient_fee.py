#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_search_operator import Ui_MainWindow
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSlot, QCoreApplication,QDateTime,Qt,pyqtSignal


class PatientFeeView(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,username,parentWindow=None):
        self.username=username
        self.parentWindow=parentWindow
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        self.headLabel=["发票单编号","发票号码","日期","处方编号"
            ,"诊断医生","收银员","患者","应收金额","免折扣金","实收名额"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)

        self.tableWidget.cellClicked.connect(self.item2lineEdit)

        self.on_pushButton_refresh_clicked()

    def retranslateUi_2(self, parent):
        self.setWindowTitle("个人缴费")
        self.label_title.setText("个人缴费")
        self.tableWidget.setColumnCount(len(self.headLabel))
        self.tableWidget.setHorizontalHeaderLabels(self.headLabel)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

    def fill_tableview(self, infoTuple):
        """
        将查询到的数据重新展现到表中
        :param infoTuple: tuple of tuple : query of data
        :return: None
        """
        self.tableWidget.setRowCount(len(infoTuple))
        _translate = QCoreApplication.translate
        font = QtGui.QFont()
        font.setPointSize(12)
        for row, record in enumerate(infoTuple):
            for column, i in enumerate(record):
                if i is None:
                    i=""
                item=QtWidgets.QTableWidgetItem(str(i))
                self.tableWidget.setItem(int(row), int(column), item)

        self.retranslateUi_2(self)
        return None

    def query_operate(self, message) -> None:
        """
        通过message 元信息搜索
        :param message: str
        :return: None
        """
        if message=="":
            self.on_pushButton_refresh_clicked()
            return None
        self.tableWidget.clear()
        if not is_number(message):
            sql = """
                SELECT fee.fno,fee.fnumber,fee.fdate,fee.rno,doctor.dname, cashier.cashname,
                patient.pname,fee.frecipefee, fee.fdiscount, fee.fsum
                FROM `cs2347.fee` fee,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.cashier` cashier, `cs2347.diagnosis` diagnosis,
                `cs2347.recipe_master` recipe_master
                WHERE fee.dgno=diagnosis.dgno AND diagnosis.dno=doctor.dno
                 AND fee.rno=recipe_master.rmno AND fee.cno=cashier.cashno
                AND  patient.pno=fee.pno AND patient.padmin='{1}'
                AND ( fee.fdate LIKE '%{0}%' OR doctor.dname  LIKE '%{0}%' 
                OR cashier.cashname LIKE '%{0}%' OR patient.pname LIKE '%{0}%'
                )
                ORDER BY fee.fno ASC
            """.format(message,self.username)
        else:
            sql = """
                SELECT fee.fno,fee.fnumber,fee.fdate,fee.rno,doctor.dname, cashier.cashname,
                patient.pname,fee.frecipefee, fee.fdiscount, fee.fsum
                FROM `cs2347.fee` fee,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.cashier` cashier, `cs2347.diagnosis` diagnosis,
                `cs2347.recipe_master` recipe_master
                WHERE fee.dgno=diagnosis.dgno AND diagnosis.dno=doctor.dno
                 AND fee.rno=recipe_master.rmno AND fee.cno=cashier.cashno
                AND  patient.pno=fee.pno AND patient.padmin='{1}'
                AND ( fee.fdate LIKE '%{0}%' OR doctor.dname  LIKE '%{0}%' 
                OR cashier.cashname LIKE '%{0}%' OR patient.pname LIKE '%{0}%'
                OR fee.fno={0} OR fee.fnumber={0} OR fee.rno={0} OR fee.frecipefee={0}
                OR fee.fdiscount={0} OR fee.fsum={0}
                )
                ORDER BY fee.fno ASC
            """.format(message,self.username)

        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()

        self.fill_tableview(infoTuple)


    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.hide()
        self.parentWindow.show()

    @pyqtSlot()
    def on_pushButton_refresh_clicked(self):
        self.tableWidget.clear()
        sql="""
                SELECT fee.fno,fee.fnumber,fee.fdate,fee.rno,doctor.dname, cashier.cashname,
                patient.pname,fee.frecipefee, fee.fdiscount, fee.fsum
                FROM `cs2347.fee` fee,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.cashier` cashier, `cs2347.diagnosis` diagnosis,
                `cs2347.recipe_master` recipe_master
                WHERE fee.dgno=diagnosis.dgno AND diagnosis.dno=doctor.dno
                 AND fee.rno=recipe_master.rmno AND fee.cno=cashier.cashno
                AND  patient.pno=fee.pno AND patient.padmin='{0}'
                ORDER BY fee.fno ASC
        """.format(self.username)
        print(sql)
        self.cursor.execute(sql)
        infoTuple=self.cursor.fetchall()

        self.fill_tableview(infoTuple)
        self.lineEdit_search.clear()


    @pyqtSlot()
    def on_pushButton_query_clicked(self):
        searchMsg=self.lineEdit_search.text()
        self.query_operate(searchMsg)

    @pyqtSlot(int,int)
    def item2lineEdit(self,row,column):
        item = self.tableWidget.item(row,column)
        if item:
            print(item.text())
            self.lineEdit_search.clear()
            self.lineEdit_search.setText(item.text())


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError,ValueError):
        pass
    return False