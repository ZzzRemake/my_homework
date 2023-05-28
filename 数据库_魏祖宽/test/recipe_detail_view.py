#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_operator import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QCoreApplication

import recipe_detail_dialog
import delete_dialog

class RecipeDetailView(QtWidgets.QMainWindow,Ui_MainWindow):
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
        self.headLabel=["处方药品清单编号","所属处方编号","药品编号","药品名称","价格","数量","数量单位"]
        self.dialogLabel=["处方药品清单编号","所属处方编号","药品编号","价格","数量","数量单位",]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)
        self.setWindowTitle("处方药品清单管理")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        self.insert_dialog = recipe_detail_dialog.RecipeDetailDialog(self)
        self.insert_dialog._dataSignal.connect(self.insert_operator)
        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)
        self.query_dialog=recipe_detail_dialog.RecipeDetailDialog(self)
        self.query_dialog._dataSignal.connect(self.query_operate)
        self.update_dialog=recipe_detail_dialog.RecipeDetailDialog(self)
        self.update_dialog._dataSignal.connect(self.update_operate)

        self.label_title.setText("就诊-处方药品清单管理")

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
            SELECT rdno
            FROM `cs2347.recipe_detail`
            WHERE rdno={0} 
        """.format(record['rdno'])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) == 0:
            sql="SELECT rmno " \
                "FROM `cs2347.recipe_master` " \
                "WHERE rmno={0}".format(record['rmno'])
            self.cursor.execute(sql)
            rmdata = self.cursor.fetchall()
            sql="SELECT mno " \
                "FROM `cs2347.medicine` " \
                "WHERE mno={0}".format(record['mno'])
            self.cursor.execute(sql)
            mdata = self.cursor.fetchall()
            if not rmdata :
                self.label_status.setText("插入数据失败: 处方不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            if not mdata:
                self.label_status.setText("插入数据失败：药品不存在！")
                self.on_pushButton_refresh_clicked()
                return None
            try:
                print(record)
                sql = "INSERT INTO `cs2347.recipe_detail`(rdno,rmno,mno,rdprice,rdnumber," \
                      "rdunit) " \
                      "VALUES " \
                      "({0},{1},{2},{3},{4},{5})".format(record['rdno'], record['rmno'],record['mno'],
                                                                 record['rdprice'], record['rdnumber'], record['rdunit']
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
        rdno = self.tableWidget.item(self.nowColumn, 0).text()
        try:
            sql = """
                DELETE FROM `cs2347.recipe_detail` WHERE rdno={}
            """.format(rdno)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        self.on_pushButton_refresh_clicked()
        self.nowColumn = -1

    def query_operate(self, record) -> None:
        confidence = ""
        tem = (('recipe_detail', ('rdno','rmno','mno','rdprice','rdnumber','rdunit',),),
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
            SELECT recipe_detail.rdno,recipe_detail.rmno,recipe_detail.mno,medicine.mname,
            recipe_detail.rdprice,recipe_detail.rdnumber,recipe_detail.rdunit
            FROM `cs2347.recipe_detail` recipe_detail, `cs2347.medicine` medicine
            WHERE {0} medicine.mno=recipe_detail.mno
            ORDER BY recipe_detail.rdno ASC
        """.format(confidence)

        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        self.fill_tableview(infoTuple)
        self.label_status.setText("查询数据成功")

    def update_operate(self, record) -> None:
        rdno = self.tableWidget.item(self.nowColumn, 0).text()
        rddata=None
        mdata=None
        rmdata=None
        if record['rdno']!='':
            sql = """
                SELECT rdno FROM `cs2347.recipe_detail` WHERE rdno={}
            """.format(record['rdno'])
            self.cursor.execute(sql)
            rddata = self.cursor.fetchall()
        if record['mno']!='':
            sql = """
                SELECT mno FROM `cs2347.medicine` WHERE mno={}
            """.format(record['mno'])
            self.cursor.execute(sql)
            mdata = self.cursor.fetchall()
        if record['rmno']!='':
            sql = """
                SELECT rmno FROM `cs2347.recipe_master` WHERE rmno={}
            """.format(record['rmno'])
            self.cursor.execute(sql)
            rmdata = self.cursor.fetchall()

        if rmdata and mdata and (rdno==record['rdno'] or (rdno!=record['rdno'] and not rddata)):
            try:
                sql = """
                    UPDATE `cs2347.recipe_detail` SET rdno={0},rmno={1},mno={2},rdprice={3},
                    rdnumber={4},rdunit={5}
                    WHERE rdno={6}
                """.format(record['rdno'], record['rmno'], record['mno'],record['rdprice'],
                           record['rdnumber'],record['rdunit'],rdno)
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
            SELECT recipe_detail.rdno,recipe_detail.rmno,recipe_detail.mno,medicine.mname,
            recipe_detail.rdprice,recipe_detail.rdnumber,recipe_detail.rdunit
            FROM `cs2347.recipe_detail` recipe_detail, `cs2347.medicine` medicine
            WHERE medicine.mno=recipe_detail.mno
            ORDER BY recipe_detail.rdno ASC
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