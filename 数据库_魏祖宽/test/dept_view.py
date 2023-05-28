#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt

import dept_dialog
import delete_dialog

class DeptView(QtWidgets.QMainWindow,Ui_MainWindow):
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

        self.headLabel=["部门编号","部门名称","父级部门编号","父级部门名称","部门经理编号","部门经理名称"]
        self.dialogLabel=["部门编号","部门名称","父级部门编号","部门经理编号",]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("部门管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)


        self.insert_dialog = dept_dialog.DeptDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=dept_dialog.DeptDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=dept_dialog.DeptDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("部门管理")

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
            SELECT dept.deptno 
            FROM `cs2347.dept` dept
            WHERE dept.deptno={0} 
        """.format(record['deptno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            # 检查是否有经理，医院科室可以无父级部门
            sql="""
                SELECT dno
                FROM `cs2347.doctor`
                WHERE dno={0}
            """.format(record['manager'])
            print(sql)
            self.cursor.execute(sql)
            print("?")
            data=self.cursor.fetchall()
            print("?")
            if len(data) == 0:
                self.label_status.setText("插入数据失败：插入的数据中没有对应的医生编号")
                self.on_pushButton_refresh_clicked()
                return None
            try:
                sql = "INSERT INTO `cs2347.dept`(deptno,deptname,parentdeptno,manager)" \
                      "VALUES" \
                      "({0},{1},{2},{3})".format(record['deptno'], record['deptname'], record['parentdeptno'],
                                                record['manager'])
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                self.label_status.setText("插入数据成功")
            except:
                self.db.rollback()
                self.label_status.setText("插入数据失败")

        else:
            print("?")
            self.reconnect_db()
            self.label_status.setText("插入数据失败：试图插入拥有已存在的编号的记录")
        self.on_pushButton_refresh_clicked()
        return None

    def delete_operator(self) -> None:
        deptno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT parentdeptno FROM `cs2347.dept` WHERE parentdeptno={} AND deptno<>parentdeptno
        """.format(deptno)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            self.label_status.setText("删除失败：有部分部门以该部门为父级部门")
            self.on_pushButton_refresh_clicked()
            return None
        try:
            sql = """
                DELETE FROM `cs2347.dept` WHERE deptno={}
            """.format(deptno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('dept', ('deptno','deptname','parentdeptno','manager')),
               )
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        self.tableWidget.clear()
        sql = """
            SELECT dept.deptno,dept.deptname,dept.parentdeptno,pdept.deptname,dept.manager,doctor.dname
            FROM `cs2347.dept` dept,`cs2347.dept` pdept, `cs2347.doctor` doctor
            WHERE {0} dept.parentdeptno=pdept.deptno AND doctor.dno=dept.manager
            ORDER BY dept.deptno ASC
        """.format(confidence)
        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        deptno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT deptno FROM `cs2347.dept` WHERE deptno={}
        """.format(record['parentdeptno'])
        self.cursor.execute(sql)
        parentdata = self.cursor.fetchall()
        sql = """
            SELECT dno FROM `cs2347.doctor` WHERE dno={}
        """.format(record['manager'])
        self.cursor.execute(sql)
        ddata = self.cursor.fetchall()
        if (ddata and parentdata) or record['deptno']==record['parentdeptno']:
            try:
                sql = """
                    UPDATE `cs2347.dept` SET deptno={0},deptname={1},
                    parentdeptno={2},manager={3} WHERE deptno={4}
                """.format(record['deptno'], record['deptname'], record['parentdeptno'], record['manager'],deptno)
                print(sql)
                self.cursor.execute(sql)
                self.db.commit()
                self.label_status.setText("更新第{}行数据成功".format(str(self.nowColumn+1)))
            except:
                self.db.rollback()
                self.label_status.setText("更新第{}行数据失败".format(str(self.nowColumn+1)))
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
        sql="""SELECT dept.deptno,dept.deptname,dept.parentdeptno,
        pdept.deptname,dept.manager,doctor.dname 
        FROM `cs2347.dept` dept, `cs2347.dept` pdept, `cs2347.doctor` doctor
        WHERE dept.parentdeptno=pdept.deptno AND dept.manager=doctor.dno
        ORDER BY dept.deptno ASC
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