#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import pymysql
from pymysql.constants import CLIENT

import diagnosis_dialog
import delete_dialog

class DiagnosisView(QtWidgets.QMainWindow, Ui_MainWindow):
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

        self.headLabel = ["诊断编码", "患者编号", "医生编号","症状描述", "诊断结论", "诊断时间",
                          "就诊费用"]
        self.dialogLabel=["诊断编码", "患者编号", "医生编号","症状描述", "诊断结论", "诊断时间",
                          "就诊费用"]

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("就诊管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = diagnosis_dialog.DiagnosisDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog = delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog = diagnosis_dialog.DiagnosisDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog = diagnosis_dialog.DiagnosisDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("就诊-就诊管理")

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
            SELECT diagnosis.dgno
            FROM `cs2347.diagnosis` diagnosis
            WHERE diagnosis.dgno={0}
        """.format(record['dgno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            try:
                sql="""
                    SELECT dno FROM `cs2347.doctor` WHERE dno={0}
                """.format(record['dno'])
                self.cursor.execute(sql)
                ddata=self.cursor.fetchall()
                sql="""
                    SELECT pno FROM `cs2347.patient` WHERE pno={0}
                """.format(record['pno'])
                self.cursor.execute(sql)
                pdata=self.cursor.fetchall()
                if not ddata:
                    self.label_status.setText("插入数据失败：医生不存在！")
                    self.on_pushButton_refresh_clicked()
                    return None
                if not pdata:
                    self.label_status.setText("插入数据失败：患者不存在！")
                    self.on_pushButton_refresh_clicked()
                    return None
                sql = "INSERT INTO `cs2347.diagnosis`(dgno,pno,dno,symptom,diagnosis,dgtime,rfee)" \
                      "VALUES" \
                      "({0},{1},{2},{3},{4},{5},{6})".format(record['dgno'], record['pno'], record['dno'],
                                                                 record['symptom'], record['diagnosis'],
                                                             record['dgtime'], record['rfee']
                                                            )
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
        dgno = self.tableWidget.item(self.nowColumn, 0).text()
        try:
            sql = """
                DELETE FROM `cs2347.diagnosis` WHERE dgno={}
            """.format(dgno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('diagnosis', ('dgno', 'pno', 'dno', 'symptom', 'diagnosis', 'dgtime', 'rfee')),
               )
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        self.tableWidget.clear()
        if confidence=='':
            sql = """
                SELECT diagnosis.dgno,diagnosis.pno,diagnosis.dno,diagnosis.symptom,diagnosis.diagnosis,
                diagnosis.dgtime,diagnosis.rfee
                FROM `cs2347.diagnosis` diagnosis
                ORDER BY diagnosis.dgno ASC
            """
        else:
            confidence=confidence[0:-4]
            sql="""
                SELECT diagnosis.dgno,diagnosis.pno,diagnosis.dno,diagnosis.symptom,diagnosis.diagnosis,
                diagnosis.dgtime,diagnosis.rfee
                FROM `cs2347.diagnosis` diagnosis
                WHERE {0}
                ORDER BY diagnosis.dgno ASC
            """.format(confidence)

        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        dgno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT dno FROM `cs2347.doctor` WHERE dno={0}
        """.format(record['dno'])
        self.cursor.execute(sql)
        ddata = self.cursor.fetchall()
        sql = """
            SELECT pno FROM `cs2347.patient` WHERE pno={0}
        """.format(record['pno'])
        self.cursor.execute(sql)
        pdata = self.cursor.fetchall()
        sql = """
            SELECT dgno FROM `cs2347.diagnosis` WHERE dgno={0}
        """.format(record['dgno'])
        self.cursor.execute(sql)
        dgdata = self.cursor.fetchall()
        print(ddata,pdata,dgdata)
        if ddata and pdata and (record['dgno']==dgno or (record['dgno']!=dgno and not dgdata)):
            try:
                sql = """
                    UPDATE `cs2347.diagnosis` SET dgno={0},pno={1},
                    dno={2},symptom={3},diagnosis={4},dgtime={5},rfee={6}
                    WHERE dgno={7}
                """.format(record['dgno'], record['pno'], record['dno'], record['symptom'],
                           record['diagnosis'], record['dgtime'], record['rfee'], dgno)
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                self.label_status.setText("更新第{}行数据成功".format(str(self.nowColumn+1)))
            except:
                self.db.rollback()
                self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn+1)))
        else:
            self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn + 1)))

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
            SELECT diagnosis.dgno,diagnosis.pno,diagnosis.dno,diagnosis.symptom,diagnosis.diagnosis,
            diagnosis.dgtime,diagnosis.rfee
            FROM `cs2347.diagnosis` diagnosis
            ORDER BY diagnosis.dgno ASC
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
