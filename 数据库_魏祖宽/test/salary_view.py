#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt

import salary_dialog
import delete_dialog

class SalaryView(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parentWindow=None):
        print("cash?")
        self.parentWindow=parentWindow
        self.nowColumn=-1
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        self.headLabel=["工资编号","工资等级","工资数量"]
        self.dialogLabel=["工资编号","工资等级","工资数量"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("工资管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = salary_dialog.SalaryDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=salary_dialog.SalaryDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=salary_dialog.SalaryDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("员工-工资管理")

        self.on_pushButton_refresh_clicked()

    def retranslateUi_2(self, parent):
        self.tableWidget.setColumnCount(len(self.headLabel))
        self.tableWidget.setHorizontalHeaderLabels(self.headLabel)

    def fill_tableview(self, infoTuple):
        """
        将查询到的数据重新展现到表中
        :param infoTuple: tuple of tuple : query of data
        :return: None
        """
        self.tableWidget.setRowCount(len(infoTuple))
        _translate = QCoreApplication.translate

        for row, record in enumerate(infoTuple):
            for column, i in enumerate(record):
                self.tableWidget.setItem(int(row), int(column), QtWidgets.QTableWidgetItem(str(i)))

        self.retranslateUi_2(self)
        self.tableWidget.sortByColumn(5,Qt.DescendingOrder)
        return None

    def insert_operator(self, record) -> None:
        """
        接受insert dialog 信息，并执行操作。
        :param record: dict, 接收的信息
        :return: None
        """
        # 是否重复插入
        sql = """
            SELECT sno
            FROM `cs2347.salary`
            WHERE sno={0} 
        """.format(record['sno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            try:
                sql = "INSERT INTO `cs2347.salary`(sno,slevel,snumber)" \
                      "VALUES" \
                      "({0},{1},{2})".format(record['sno'], record['slevel'], record['snumber'])
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                self.label_status.setText("插入数据成功")
            except Exception:
                self.db.rollback()
                self.label_status.setText("插入数据失败")

        else:
            self.label_status.setText("插入数据失败：试图插入拥有已存在的编号的记录")
        self.on_pushButton_refresh_clicked()
        return None

    def delete_operator(self) -> None:
        sno = self.tableWidget.item(self.nowColumn, 0).text()
        try:
            sql = """
                DELETE FROM `cs2347.salary` WHERE sno={}
            """.format(sno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('salary', ('sno','slevel','snumber')),
               )
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        confidence=confidence[0:-4]
        self.tableWidget.clear()
        if confidence=="":
            sql = """
                SELECT salary.sno,salary.slevel,salary.snumber
                FROM `cs2347.salary` salary
                ORDER BY salary.sno ASC
            """.format(confidence)
        else:
            sql = """
                SELECT salary.sno,salary.slevel,salary.snumber
                FROM `cs2347.salary` salary
                WHERE {0} 
                ORDER BY salary.sno ASC
            """.format(confidence)
        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        sno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT sno FROM `cs2347.salary` WHERE sno={}
        """.format(record['sno'])
        self.cursor.execute(sql)
        sdata = self.cursor.fetchall()
        if sno==record['sno'] or (sno!=record['sno'] and not sdata):
            try:
                sql = """
                    UPDATE `cs2347.salary` SET sno={0},slevel={1},
                    snumber={2} WHERE sno={3}
                """.format(record['sno'], record['slevel'], record['snumber'],sno)
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                self.label_status.setText("更新第{}行数据成功".format(str(self.nowColumn+1)))
            except:
                self.db.rollback()
        else:
            self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn+1)))
        self.on_pushButton_refresh_clicked()

    @pyqtSlot(int, int)
    def on_tableWidget_cellClicked(self, c, r):
        self.nowColumn = c
        self.label_status.setText("选定第{}行数据".format(str(c+1)))
        print(self.nowColumn)

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.hide()
        self.parentWindow.show()

    @pyqtSlot()
    def on_pushButton_refresh_clicked(self):
        self.tableWidget.clear()
        sql="""
            SELECT salary.sno,salary.slevel,salary.snumber
            FROM `cs2347.salary` salary
            ORDER BY salary.sno ASC
        """
        self.cursor.execute(sql)
        infoTuple=self.cursor.fetchall()
        self.fill_tableview(infoTuple)

    @pyqtSlot()
    def on_pushButton_insert_clicked(self):
        self.insert_dialog.show()

    @pyqtSlot()
    def on_pushButton_delete_clicked(self):
        if self.nowColumn >= 0:
            self.delete_dialog.show()

    @pyqtSlot()
    def on_pushButton_update_clicked(self):
        if self.nowColumn >= 0:
            data = []
            for i in range(len(self.headLabel)):
                if self.headLabel[i] in self.dialogLabel:
                    data.append(self.tableWidget.item(self.nowColumn, i).text())
            self.update_dialog.fill_data(data)
            self.update_dialog.show()

    @pyqtSlot()
    def on_pushButton_query_clicked(self):
        self.query_dialog.show()

    def reconnect_db(self):
        """
        重连数据库
        :return:bool
        """
        self.db.close()
        try:
            self.db = pymysql.connect(host="124.71.219.185",
                                      user="root",
                                      password="uestc2022!",
                                      charset="utf8mb4",
                                      database="cs2347.his",
                                      client_flag=CLIENT.MULTI_STATEMENTS)

            self.cursor = self.db.cursor()
            return True
        except Exception:
            print(Exception)
            return False