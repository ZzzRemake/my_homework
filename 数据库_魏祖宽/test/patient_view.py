#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import pymysql
from pymysql.constants import CLIENT

import patient_dialog
import delete_dialog

class PatientWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.parentWindow = parent
        self.nowColumn = -1
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()

        self.headLabel = ["患者编号", "患者姓名", "身份证号",
                          "社会保障卡号", "医疗卡识别号", "患者性别",
                          "出生日期", "患者地址", "联系方式编号", "联系方式", "联系号码"]

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("患者管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = patient_dialog.PatientDialogInsert(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog = delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog = patient_dialog.PatientDialogInsert(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog = patient_dialog.PatientDialogInsert(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("患者管理")

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

    def insert_operator(self, record) -> None:
        """
        接受insert dialog 信息，并执行操作。
        :param record: dict, 接收的信息
        :return: None
        """
        sql = """
            SELECT patient.pno,patient_tel.ptno 
            FROM `cs2347.patient` patient, `cs2347.patient_tel` patient_tel 
            WHERE patient.pno={0} AND patient_tel.ptno={1}
        """.format(record['pno'], record['ptno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            try:
                sql = "INSERT INTO `cs2347.patient`(pno,pname,pid,pino,pmno,psex,pbd,padd)" \
                      "VALUES" \
                      "({0},{1},{2},{3},{4},{5},{6},{7})".format(record['pno'], record['pname'], record['pid'],
                                                                 record['pino'], record['pmno'], record['psex'],
                                                                 record['pbd'], record['padd']
                                                                 )
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
            try:
                sql = "INSERT INTO `cs2347.patient_tel`(ptno,pno,pteltype,ptelcode)VALUES" \
                      "({0},{1},{2},{3})".format(record['ptno'], record['pno'], record['pteltype'], record['ptelcode'])
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
            self.label_status.setText("插入数据成功")
        else:
            self.reconnect_db()

            self.label_status.setText("插入数据失败：试图插入拥有已存在的编号的记录")
        self.on_pushButton_refresh_clicked()

    def delete_operator(self) -> None:
        pno = self.tableWidget.item(self.nowColumn, 0).text()
        ptno = self.tableWidget.item(self.nowColumn, 8).text()
        sql = """
            SELECT ptno FROM `cs2347.patient_tel` WHERE pno={0}
        """.format(pno)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        try:
            sql = """
                DELETE FROM `cs2347.patient_tel` WHERE ptno={}
            """.format(ptno)
            self.cursor.execute(sql)
            self.db.commit()
            if len(data) == 1:
                sql = """
                    DELETE FROM `cs2347.patient` WHERE pno={}
                """.format(pno)
                self.cursor.execute(sql)
                self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('patient', ('pno', 'pname', 'pid', 'pino', 'pmno', 'psex', 'pbd', 'padd')),
               ('patient_tel', ('ptno', 'pno', 'pteltype', 'ptelcode'))
               )
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        self.tableWidget.clear()
        sql = """
            SELECT patient.pno,patient.pname,patient.pid,patient.pino,patient.pmno,
            patient.psex,patient.pbd,patient.padd,patient_tel.ptno,patient_tel.pteltype,patient_tel.ptelcode
            FROM `cs2347.patient` patient, `cs2347.patient_tel` patient_tel
            WHERE {0} patient.pno=patient_tel.ptno
            ORDER BY patient.pno ASC
        """.format(confidence)
        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        pno = self.tableWidget.item(self.nowColumn, 0).text()
        ptno = self.tableWidget.item(self.nowColumn, 8).text()
        try:
            sql = """
                UPDATE `cs2347.patient` SET pno={0},pname={1},
                pid={2},pino={3},pmno={4},psex={5},pbd={6},padd={7}
                WHERE pno={8}
            """.format(record['pno'], record['pname'], record['pid'], record['pino'],
                       record['pmno'], record['psex'], record['pbd'], record['padd'], pno)
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            sql = """
                UPDATE `cs2347.patient_tel` SET ptno={0},pno={1},pteltype={2},ptelcode={3}
                WHERE ptno={4} 
            """.format(record['ptno'], record['pno'], record['pteltype'], record['ptelcode'], ptno)
            self.cursor.execute(sql)
            self.db.commit()
            self.label_status.setText("更新第{}行数据成功".format(str(self.nowColumn+1)))
        except:
            self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn+1)))
            self.db.rollback()

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
        print("refresh")
        self.tableWidget.clear()
        sql = """
            SELECT patient.pno,patient.pname,patient.pid,patient.pino,patient.pmno,
            patient.psex,patient.pbd,patient.padd,patient_tel.ptno,patient_tel.pteltype,patient_tel.ptelcode
            FROM `cs2347.patient` patient, `cs2347.patient_tel` patient_tel
            WHERE patient.pno=patient_tel.pno
            ORDER BY patient.pno ASC
        """
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
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
