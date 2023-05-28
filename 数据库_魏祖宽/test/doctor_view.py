#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication,Qt

import doctor_dialog
import delete_dialog

class DoctorView(QtWidgets.QMainWindow,Ui_MainWindow):
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
        self.headLabel=["医生编号","医生姓名","性别","年龄","所属部门编号","所属部门","职位编号","职位","所属行业","工资","用户名"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("医生管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = doctor_dialog.DoctorDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=doctor_dialog.DoctorDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=doctor_dialog.DoctorDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("员工-医生管理")

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
        # self.tableWidget.sortByColumn(5,Qt.DescendingOrder)
        return None

    def insert_operator(self, record) -> None:
        """
        接受insert dialog 信息，并执行操作。
        :param record: dict, 接收的信息
        :return: None
        """
        # 是否重复插入
        sql = """
            SELECT doctor.dno 
            FROM `cs2347.doctor` doctor
            WHERE doctor.dno={0} 
        """.format(record['dno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            # 检查是否有经理，医院科室可以无父级部门
            sql="""
                SELECT tno
                FROM `cs2347.title`
                WHERE tno={0}
            """.format(record['dtno'])
            print(sql)
            self.cursor.execute(sql)
            tdata=self.cursor.fetchall()
            if len(tdata) == 0:
                self.label_status.setText("插入数据失败：插入的数据中没有对应的职称编号")
                self.on_pushButton_refresh_clicked()
                return None
            sql="""
                SELECT deptno
                FROM `cs2347.dept`
                WHERE deptno={0}
            """.format(record['deptno'])
            print(sql)
            self.cursor.execute(sql)
            tdata=self.cursor.fetchall()
            if len(tdata) == 0:
                self.label_status.setText("插入数据失败：插入的数据中没有对应的部门编号")
                self.on_pushButton_refresh_clicked()
                return None
            try:
                print("??")
                if record['dadmin']!='':
                    sql = "INSERT INTO `cs2347.doctor`(dno,dname,dsex,dage,deptno,dtno,dadmin)" \
                          "VALUES" \
                          "({0},{1},{2},{3},{4},{5},{6})".format(record['dno'], record['dname'], record['dsex'],
                                                    record['dage'],record['deptno'],record['dtno'],record['dadmin'])
                    print(sql)
                else:
                    sql = "INSERT INTO `cs2347.doctor`(dno,dname,dsex,dage,deptno,dtno)" \
                          "VALUES" \
                          "({0},{1},{2},{3},{4},{5})".format(record['dno'], record['dname'], record['dsex'],
                                                    record['dage'],record['deptno'],record['dtno'])
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
        dno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT manager FROM `cs2347.dept` WHERE manager={0}
        """.format(dno)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            self.label_status.setText("删除失败：有部门以该医生为主管")
            self.on_pushButton_refresh_clicked()
            return None
        try:
            sql = """
                DELETE FROM `cs2347.doctor` WHERE dno={}
            """.format(dno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('doctor', ('dno','dname','dsex','dage','deptno','dtno','dadmin')),
               )
        for i in tem:
            for key in i[1]:
                value = record[key]
                if value != "''" and value:
                    confidence = confidence + " {0}.{1}={2} AND ".format(i[0], key, record[key])
        self.tableWidget.clear()
        sql = """
            SELECT doctor.dno,doctor.dname,doctor.dsex,doctor.dage,doctor.deptno,dept.deptname,
            doctor.dtno,title.ttype,title.ttrade,salary.snumber,doctor.dadmin
            FROM `cs2347.dept` dept,`cs2347.title` title,`cs2347.salary` salary, `cs2347.doctor` doctor
            WHERE {0} doctor.deptno=dept.deptno AND doctor.dtno=title.tno AND title.sno=salary.sno
            ORDER BY doctor.dno ASC
        """.format(confidence)
        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        dno = self.tableWidget.item(self.nowColumn, 0).text()
        sql = """
            SELECT tno FROM `cs2347.title` WHERE tno={}
        """.format(record['dtno'])
        self.cursor.execute(sql)
        tdata = self.cursor.fetchall()
        sql="""
            SELECT dno FROM `cs2347.doctor` WHERE dno={}
        """.format(record['dno'])
        self.cursor.execute(sql)
        ddata=self.cursor.fetchall()
        print(ddata,dno,record['dno'])
        if tdata and (dno==record['dno'] or (dno!=record['dno'] and not ddata)):
            try:
                if record['dadmin']!='':
                    sql = """
                        UPDATE `cs2347.doctor` SET dno={0},dname={1},
                        dage={2},dsex={3},deptno={4},dtno={5},dadmin={6} WHERE dno={7}
                    """.format(record['dno'], record['dname'], record['dage'],record['dsex'],record['deptno'],
                               record['dtno'],record['dadmin'],dno)
                else:
                    sql = """
                        UPDATE `cs2347.doctor` SET dno={0},dname={1},
                        dage={2},dsex={3},deptno={4},dtno={5} WHERE dno={6}
                    """.format(record['dno'], record['dname'], record['dage'],record['dsex'],record['deptno'],
                               record['dtno'],dno)
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
            SELECT doctor.dno,doctor.dname,doctor.dsex,doctor.dage,doctor.deptno,dept.deptname,
            doctor.dtno,title.ttype,title.ttrade,salary.snumber,doctor.dadmin
            FROM `cs2347.dept` dept,`cs2347.title` title,`cs2347.salary` salary, `cs2347.doctor` doctor
            WHERE doctor.deptno=dept.deptno AND doctor.dtno=title.tno AND title.sno=salary.sno 
            ORDER BY doctor.dno ASC
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