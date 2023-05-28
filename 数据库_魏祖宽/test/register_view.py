#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt

import register_dialog
import delete_dialog

class RegisterView(QtWidgets.QMainWindow,Ui_MainWindow):
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
        self.headLabel=["挂号单编号","科室编号","挂号科室","医生编号","挂号医生","患者编号","挂号患者","收银员编号","收银员","挂号时间"
            ,"预约就诊时间","挂号费","备注"]
        self.dialogLabel=["挂号单编号","科室编号","医生编号","患者编号","收银员编号","挂号时间",
                          "预约就诊时间","备注"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("挂号管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    #    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = register_dialog.RegisterDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=register_dialog.RegisterDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=register_dialog.RegisterDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("挂号管理")

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
        # 是否重复插入
        sql = """
            SELECT rfno
            FROM `cs2347.register_form`
            WHERE rfno={0} 
        """.format(record['rfno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            sql="SELECT dno " \
                "FROM `cs2347.doctor` " \
                "WHERE dno={0}".format(record['rfdoctor'])
            self.cursor.execute(sql)
            ddata = self.cursor.fetchall()
            sql="SELECT pno " \
                "FROM `cs2347.patient` " \
                "WHERE pno={0}".format(record['rfpatient'])
            self.cursor.execute(sql)
            pdata = self.cursor.fetchall()
            sql="SELECT cashno " \
                "FROM `cs2347.cashier` " \
                "WHERE cashno={0}".format(record['rfcashier'])
            self.cursor.execute(sql)
            cdata = self.cursor.fetchall()
            sql="SELECT deptno " \
                "FROM `cs2347.dept` " \
                "WHERE deptno={0}".format(record['rfdept'])
            self.cursor.execute(sql)
            deptdata = self.cursor.fetchall()
            if not ddata :
                self.label_status.setText("插入数据失败: 医生不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not pdata:
                self.label_status.setText("插入数据失败：患者不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not cdata:
                self.label_status.setText("插入数据失败：收银员不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not deptdata:
                self.label_status.setText("插入数据失败：部门不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            print(sql)
            try:
                sql = "INSERT INTO `cs2347.register_form`(rfno,rfdept,rfdoctor,rfpatient,rfcashier," \
                      "rftime,rfvisittime,rfnotes) " \
                      "VALUES " \
                      "({0},{1},{2},{3},{4},{5},{6},{7})".format(record['rfno'], record['rfdept'],record['rfdoctor'],
                                                                 record['rfcashier'],
                                                                 record['rfpatient'], record['rftime'],
                                                                 record['rfvisittime'],
                                                                 record['rfnotes']
                                                                 )
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
        rfno = self.tableWidget.item(self.nowColumn, 0).text()
        try:
            sql = """
                DELETE FROM `cs2347.register_form` WHERE rfno={}
            """.format(rfno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('register', ('rfno','rfdept','rfdoctor','rfpatient','rfcashier','rftime',
                                 'rfvisittime','rfnotes')),
               )
        print(record)
        for i in tem:
            for key in i[1]:
                print(i,key)
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        self.tableWidget.clear()
        sql = """
            SELECT register.rfno,register.rfdept,dept.deptname,register.rfdoctor,
            doctor.dname,register.rfpatient,patient.pname,register.rfcashier,
            cashier.cashname,
            register.rftime,register.rfvisittime,title.tfee,register.rfnotes
            FROM `cs2347.register_form` register, `cs2347.doctor` doctor,
            `cs2347.patient` patient,`cs2347.cashier` cashier, `cs2347.dept` dept,
            `cs2347.title` title
            WHERE {0} register.rfdoctor=doctor.dno AND register.rfpatient=patient.pno 
            AND register.rfdept=dept.deptno AND register.rfcashier=cashier.cashno
            AND title.tno=doctor.dtno
            ORDER BY register.rfno ASC
        """.format(confidence)

        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        rfno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT rfno FROM `cs2347.register_form` WHERE rfno={}
        """.format(record['rfno'])
        self.cursor.execute(sql)
        rfdata = self.cursor.fetchall()

        if rfno==record['rfno'] or (rfno!=record['rfno'] and not rfdata):
            try:
                sql = """
                    UPDATE `cs2347.register_form` SET rfno={0},rfdept={1},rfdoctor={2},rfpatient={3},
                    rfcashier={4},rftime={5},rfvisittime={6},rfnotes={7}
                    WHERE rfno={8}
                """.format(record['rfno'], record['rfdept'], record['rfdoctor'],record['rfpatient'],
                           record['rfcashier'],record['rftime'],record['rfvisittime'],
                           record['rfnotes'],rfno)
                print(sql)
                print("?")
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
            SELECT register.rfno,register.rfdept,dept.deptname,register.rfdoctor,
            doctor.dname,register.rfpatient,patient.pname,register.rfcashier,
            cashier.cashname,
            register.rftime,register.rfvisittime,title.tfee,register.rfnotes
            FROM `cs2347.register_form` register, `cs2347.doctor` doctor,
            `cs2347.patient` patient,`cs2347.cashier` cashier, `cs2347.dept` dept,
            `cs2347.title` title
            WHERE register.rfdoctor=doctor.dno AND register.rfpatient=patient.pno 
            AND register.rfdept=dept.deptno AND register.rfcashier=cashier.cashno
            AND title.tno=doctor.dtno
            ORDER BY register.rfno ASC
        """
        print(sql)
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