#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt

import admin_dialog
import delete_dialog

class AdminPatientView(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parentWindow=None):
        self.parentWindow=parentWindow
        self.nowColumn=-1
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        self.headLabel=["患者编号","患者姓名","患者用户名","密码"]
        self.dialogLabel=["患者用户名","密码"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("患者用户账户管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.update_dialog=admin_dialog.AdminDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)
        self.pushButton_query.hide()
        self.pushButton_insert.hide()
        self.menubar.hide()

        self.label_title.setText("账户-患者用户账户管理")

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
        return None

    def delete_operator(self) -> None:
        pno = self.tableWidget.item(self.nowColumn, 0).text()
        pname=self.tableWidget.item(self.nowColumn,2).text()
        try:
            sql = """
                UPDATE `cs2347.patient` SET padmin=NULL,ppwd=NULL
                WHERE pno={0}
            """.format(pno)
            self.cursor.execute(sql)
            self.db.commit()
            sql="""
                DELETE FROM `cs2347.administrator` WHERE `user`='{0}'
            """.format(pname)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1



    def update_operate(self, record) -> None:
        dno = self.tableWidget.item(self.nowColumn, 0).text()
        dadmin=self.tableWidget.item(self.nowColumn, 2).text()
        sql="""
            SELECT pno FROM `cs2347.patient` WHERE padmin={}
        """.format(record['username'])
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        print(record,dadmin,data)
        if record['username'] != "'{}'".format(dadmin) and data:
            self.label_status.setText("更新第{}行数据失败: 重复用户名".format(str(self.nowColumn+1)))
            return None

        try:
            sql = """
                UPDATE `cs2347.patient` SET padmin={0},ppwd=md5({1})
                WHERE pno={2}
            """.format(record['username'], record['password'], dno)
            self.cursor.execute(sql)
            self.db.commit()
            sql="""
                SELECT * FROM `cs2347.administrator` WHERE `type`='patient' AND `user`={0}
            """.format(record['username'])
            self.cursor.execute(sql)
            adata=self.cursor.fetchall()
            if adata:
                sql="""
                    UPDATE `cs2347.administrator` SET `user`={0},password=md5({1}),`type`='patient'
                    WHERE `user`={0}
                """.format(record['username'], record['password'])
            else:
                sql="""
                    INSERT INTO `cs2347.administrator`(`user`,`password`,`type`)
                    VALUES
                    ({0},md5({1}),'patient')
                """.format(record['username'], record['password'])
            self.cursor.execute(sql)
            self.db.commit()
            self.label_status.setText("更新第{}行数据成功".format(str(self.nowColumn+1)))
        except:
            self.db.rollback()
            self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn+1)))
        sql="""
        SELECT * FROM `cs2347.administrator`
        """
        self.cursor.execute(sql)
        test=self.cursor.fetchall()
        print(test)
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
            SELECT pno,pname,padmin,ppwd
            FROM `cs2347.patient`
            ORDER BY pno ASC
        """
        self.cursor.execute(sql)
        infoTuple=self.cursor.fetchall()
        self.fill_tableview(infoTuple)


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