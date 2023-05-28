#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication

import fee_dialog
import delete_dialog

class FeeView(QtWidgets.QMainWindow,Ui_MainWindow):
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
        self.headLabel=["发票单编号","发票号码","日期","处方编号","收银员编号",
                        "收银员姓名","患者编号","患者姓名","应收金额","减免折扣金额","实收金额"]
        self.dialogLabel=["发票单编号","发票号码","日期","处方编号","收银员编号",
                        "患者编号","应收金额","减免折扣金额","实收金额"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("费用管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = fee_dialog.FeeDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.insert_dialog.groupBox_fsum.hide()
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=fee_dialog.FeeDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=fee_dialog.FeeDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)
        self.update_dialog.groupBox_fsum.hide()

        self.label_title.setText("费用管理")

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
            SELECT fno
            FROM `cs2347.fee`
            WHERE fno={0} 
        """.format(record['fno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            sql="SELECT rmno " \
                "FROM `cs2347.recipe_master` " \
                "WHERE rmno={0}".format(record['rno'])
            self.cursor.execute(sql)
            rmdata = self.cursor.fetchall()
            sql="SELECT cashno " \
                "FROM `cs2347.cashier` " \
                "WHERE cashno={0}".format(record['cno'])
            self.cursor.execute(sql)
            cdata = self.cursor.fetchall()
            sql="SELECT pno " \
                "FROM `cs2347.patient` " \
                "WHERE pno={0}".format(record['pno'])
            self.cursor.execute(sql)
            pdata = self.cursor.fetchall()
            if not rmdata :
                self.label_status.setText("插入数据失败: 处方不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not cdata:
                self.label_status.setText("插入数据失败：收银员不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not pdata:
                self.label_status.setText("插入数据失败：患者不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if float(record['frecipefee'])-float(record['fdiscount'])<0:
                self.label_status.setText("插入数据失败：折扣金额不得小于应付金额！")
                self.on_pushButton_refresh_clicked()
                return None
            try:
                print(record)
                sql = "INSERT INTO `cs2347.fee`(fno,fnumber,fdate,rno,cno,pno," \
                      "frecipefee,fdiscount,fsum) " \
                      "VALUES " \
                      "({0},{1},{2},{3},{4}," \
                      "{5},{6},{7},{8})".format(record['fno'], record['fnumber'],
                                                    record['fdate'],record['rno'],
                                                    record['cno'], record['pno'],
                                                     record['frecipefee'],record['fdiscount'],
                                                    "{0}-{1}".format(record['frecipefee'],record['fdiscount'])
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
        fno = self.tableWidget.item(self.nowColumn, 0).text()
        try:
            sql = """
                DELETE FROM `cs2347.fee` WHERE fno={}
            """.format(fno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('fee', ('fno','fnumber','fdate','rno','cno','pno','frecipefee','fdiscount','fsum'),),
               )
        print(record)
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        if record['frecipefee']!='' and record['fdiscount']!='':
            if float(record['frecipefee'])-float(record['fdiscount'])<-(1e-6):
                self.label_status.setText("查询数据失败：金额错误！")
                return None
            if record['fsum']!='' and abs(float(record['frecipefee']) - float(record['fdiscount'])-float(record['fsum']))>1e-6:
                self.label_status.setText("查询数据失败：金额错误！")
                return None

        self.tableWidget.clear()
        sql = """
            SELECT fee.fno,fee.fnumber,fee.fdate,recipe_master.rmno,
            fee.cno,cashier.cashno,fee.pno,patient.pname,fee.frecipefee,
            fee.fdiscount,fee.fsum
            FROM `cs2347.fee` fee, `cs2347.patient` patient,
            `cs2347.cashier` cashier,`cs2347.recipe_master` recipe_master
            WHERE {0} recipe_master.rmno=fee.rno AND cashier.cashno=fee.cno
            AND patient.pno=fee.pno
            ORDER BY fee.fno ASC
        """.format(confidence)


        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        fno = self.tableWidget.item(self.nowColumn, 0).text()
        fdata=None
        rmdata=None
        cdata=None
        pdata=None
        if record['fno']!='':
            sql = """
                SELECT fno FROM `cs2347.fee` WHERE fno={}
            """.format(record['fno'])
            self.cursor.execute(sql)
            fdata = self.cursor.fetchall()
        if record['cno']!='':
            sql = """
                SELECT cashno FROM `cs2347.cashier` WHERE cashno={}
            """.format(record['cno'])
            self.cursor.execute(sql)
            cdata = self.cursor.fetchall()
        if record['pno']!='':
            sql = """
                SELECT pno FROM `cs2347.patient` WHERE pno={}
            """.format(record['pno'])
            self.cursor.execute(sql)
            pdata = self.cursor.fetchall()
        if record['rno']!='':
            sql = """
                SELECT rmno FROM `cs2347.recipe_master` WHERE rmno={}
            """.format(record['rno'])
            self.cursor.execute(sql)
            rmdata = self.cursor.fetchall()
        print(float(record['frecipefee'])-float(record['fdiscount']))
        if float(record['frecipefee'])-float(record['fdiscount'])<-(1e-6):
            self.label_status.setText("更新第{}行数据失败: 金额错误".format(str(self.nowColumn+1)))
            self.on_pushButton_refresh_clicked()
            return None
        if rmdata and pdata and cdata and (fno==record['fno'] or (fno!=record['fno'] and not fdata)):
            try:
                sql = """
                    UPDATE `cs2347.fee` SET fno={0},fnumber={1},fdate={2},
                    rno={3},cno={4},pno={5},frecipefee={6},fdiscount={7},fsum={8}
                    WHERE fno={9}
                """.format(record['fno'], record['fnumber'], record['fdate'],record['rno'],
                           record['cno'],record['pno'],record['frecipefee'], record['fdiscount'],
                           "{0}-{1}".format(record['frecipefee'],record['fdiscount']),fno)
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
            SELECT fee.fno,fee.fnumber,fee.fdate,recipe_master.rmno,
            fee.cno,cashier.cashno,fee.pno,patient.pname,fee.frecipefee,
            fee.fdiscount,fee.fsum
            FROM `cs2347.fee` fee, `cs2347.patient` patient,
            `cs2347.cashier` cashier, `cs2347.recipe_master` recipe_master
            WHERE recipe_master.rmno=fee.rno AND cashier.cashno=fee.cno
            AND patient.pno=fee.pno
            ORDER BY fee.fno ASC
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