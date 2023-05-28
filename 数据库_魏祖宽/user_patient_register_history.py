#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_search_operator import Ui_MainWindow
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSlot, QCoreApplication,QDateTime,Qt,pyqtSignal
import delete_dialog

class myPushButton(QtWidgets.QPushButton):
    dataSignal = pyqtSignal(int)

    def __init__(self, row, parent=None):
        print('button!')
        super().__init__(parent)
        self.row = row
        self.clicked.connect(self.send_row)

    def send_row(self):
        print('send!')
        self.dataSignal.emit(self.row)

class PatientRegisterValidView(QtWidgets.QMainWindow,Ui_MainWindow):
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
        self.headLabel=["挂号单编号","挂号医生","部门","患者"
            ,"备注","挂号时间","预约就诊时间"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)

        self.tableWidget.cellClicked.connect(self.item2lineEdit)

        self.on_pushButton_refresh_clicked()

    def retranslateUi_2(self, parent):
        self.setWindowTitle("历史挂号")
        self.label_title.setText("历史挂号")
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
                SELECT register.rfno,doctor.dname,dept.deptname,patient.pname,register.rfnotes,
                register.rftime,register.rfvisittime
                FROM `cs2347.register_form` register,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.dept` dept
                WHERE register.rfdept=dept.deptno AND register.rfdoctor=doctor.dno
                 AND register.rfpatient=patient.pno AND patient.padmin='{1}'
                 AND (doctor.dname LIKE '%{0}%' OR dept.deptname LIKE '%{0}%'
                 OR patient.pname LIKE '%{0}%' OR register.rfnotes LIKE '%{0}%'
                 OR register.rftime LIKE '%{0}%' OR register.rfvisittime LIKE '%{0}%')
                ORDER BY register.rfno ASC
            """.format(message,self.username)
        else:
            sql = """
                SELECT register.rfno,doctor.dname,dept.deptname,patient.pname,register.rfnotes,
                register.rftime,register.rfvisittime
                FROM `cs2347.register_form` register,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.dept` dept
                WHERE register.rfdept=dept.deptno AND register.rfdoctor=doctor.dno
                 AND register.rfpatient=patient.pno AND patient.padmin='{1}'
                 AND (doctor.dname LIKE '%{0}%' OR dept.deptname LIKE '%{0}%'
                 OR patient.pname LIKE '%{0}%' OR register.rfnotes LIKE '%{0}%'
                 OR register.rftime LIKE '%{0}%' OR register.rfvisittime LIKE '%{0}%'
                 OR register.rfno={0})
                ORDER BY register.rfno ASC
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
                SELECT register.rfno,doctor.dname,dept.deptname,patient.pname,register.rfnotes,
                register.rftime,register.rfvisittime
                FROM `cs2347.register_form` register,`cs2347.doctor` doctor,`cs2347.patient` patient,
                `cs2347.dept` dept
                WHERE register.rfdept=dept.deptno AND register.rfdoctor=doctor.dno
                 AND register.rfpatient=patient.pno AND patient.padmin='{0}'
                ORDER BY register.rfno ASC
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