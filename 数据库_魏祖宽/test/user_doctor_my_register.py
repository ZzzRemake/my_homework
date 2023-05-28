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
class DoctorMyRegisterView(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,username,parentWindow=None):
        self.username=username
        self.parentWindow=parentWindow
        self.nowColumn=-1
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        self.headLabel=["挂号单编号","挂号科室","挂号医生","挂号患者","收银员","挂号时间"
            ,"预约就诊时间","挂号费","备注","状态", "操作"]

        QtWidgets.QMainWindow.__init__(self, parentWindow)
        self.setupUi(self)
        self.retranslateUi_2(self)

        self.tableWidget.cellClicked.connect(self.item2lineEdit)

        self.delete_dialog=delete_dialog.deleteDialog(self)
        self.delete_dialog._deleteSignal.connect(self.delete_operator)

        self.on_pushButton_refresh_clicked()

    def retranslateUi_2(self, parent):
        self.setWindowTitle("我的挂号")
        self.label_title.setText("我的挂号")
        self.tableWidget.setColumnCount(len(self.headLabel))
        self.tableWidget.setHorizontalHeaderLabels(self.headLabel)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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
                if column==6 or (column== 9 and i=="已失效"):
                    item.setForeground(Qt.red)
                elif (column== 9 and i=="有效挂号"):
                    item.setForeground(Qt.green)
                self.tableWidget.setItem(int(row), int(column), item)
            item = myPushButton(row, self)
            item.dataSignal.connect(self.show_delete_dialog)
            item.setFont(font)
            item.setBaseSize(50, 30)
            item.setText(_translate("MainWindow", "删除"))
            self.tableWidget.setCellWidget(int(row), int(10), item)

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
                SELECT register.rfno,dept.deptname,doctor.dname,patient.pname,cashier.cashname,
                register.rftime,register.rfvisittime,title.tfee,register.rfnotes
                FROM `cs2347.register_form` register, `cs2347.doctor` doctor,
                `cs2347.patient` patient,`cs2347.cashier` cashier, `cs2347.dept` dept,
                `cs2347.title` title
                WHERE (register.rfdoctor=doctor.dno AND register.rfpatient=patient.pno 
                AND register.rfdept=dept.deptno AND register.rfcashier=cashier.cashno
                AND title.tno=doctor.dtno AND doctor.dadmin='{1}')
                AND ( dept.deptname LIKE '%{0}%' OR patient.pname LIKE '%{0}%'
                OR doctor.dname LIKE '%{0}%' OR cashier.cashname LIKE '%{0}%'
                OR register.rftime LIKE '%{0}%' OR register.rfvisittime LIKE '%{0}%'
                OR register.rfnotes LIKE '%{0}%')
                ORDER BY register.rfno ASC
            """.format(message,self.username)
        else:
            sql = """
                SELECT register.rfno,dept.deptname,doctor.dname,patient.pname,cashier.cashname,
                register.rftime,register.rfvisittime,title.tfee,register.rfnotes
                FROM `cs2347.register_form` register, `cs2347.doctor` doctor,
                `cs2347.patient` patient,`cs2347.cashier` cashier, `cs2347.dept` dept,
                `cs2347.title` title
                WHERE (register.rfdoctor=doctor.dno AND register.rfpatient=patient.pno 
                AND register.rfdept=dept.deptno AND register.rfcashier=cashier.cashno
                AND title.tno=doctor.dtno AND doctor.dadmin='{1}')
                AND ( dept.deptname LIKE '%{0}%' OR patient.pname LIKE '%{0}%'
                OR doctor.dname LIKE '%{0}%' OR cashier.cashname LIKE '%{0}%'
                OR register.rftime LIKE '%{0}%' OR register.rfvisittime LIKE '%{0}%'
                OR register.rfnotes LIKE '%{0}%'
                OR register.rfno={0} OR register.rftime={0} OR register.rfvisittime={0}
                OR title.tfee={0})
                ORDER BY register.rfno ASC
            """.format(message,self.username)

        print(sql)
        self.cursor.execute(sql)
        infoTuple = self.cursor.fetchall()
        infoList=[]
        nowTimestamp=QDateTime.currentSecsSinceEpoch()
        for x in infoTuple:
            former=QDateTime.fromString(x[-4].strftime('%Y-%m-%d %H:%M:%S'),"yyyy-MM-dd HH:mm:ss").toSecsSinceEpoch()
            latter=QDateTime.fromString(x[-3].strftime('%Y-%m-%d %H:%M:%S'),"yyyy-MM-dd HH:mm:ss").toSecsSinceEpoch()
            if former<=nowTimestamp and nowTimestamp<=latter:
                status="有效挂号"
            else:
                status="已失效"
            infoList.append(list(x)+[status])

        self.fill_tableview(infoList)

    def delete_operator(self)->None:
        if self.delete_row<0:
            print("error: -1")
            return None
        print(self.delete_row)
        rfno = self.tableWidget.item(self.delete_row, 0).text()
        self.delete_row=-1
        try:
            sql="""
                DELETE FROM `cs2347.register_form` WHERE RFno={} 
            """.format(rfno)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            print(Exception)
            self.db.rollback()

        self.on_pushButton_refresh_clicked()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.hide()
        self.parentWindow.show()

    @pyqtSlot()
    def on_pushButton_refresh_clicked(self):
        self.tableWidget.clear()
        sql="""
            SELECT register.rfno,dept.deptname,doctor.dname,patient.pname,cashier.cashname,
            register.rftime,register.rfvisittime,title.tfee,register.rfnotes
            FROM `cs2347.register_form` register, `cs2347.doctor` doctor,
            `cs2347.patient` patient,`cs2347.cashier` cashier, `cs2347.dept` dept,
            `cs2347.title` title
            WHERE register.rfdoctor=doctor.dno AND register.rfpatient=patient.pno 
            AND register.rfdept=dept.deptno AND register.rfcashier=cashier.cashno
            AND title.tno=doctor.dtno AND doctor.dadmin='{0}'
            ORDER BY register.rfno ASC
        """.format(self.username)
        print(sql)
        self.cursor.execute(sql)
        infoTuple=self.cursor.fetchall()
        infoList=[]
        nowTimestamp=QDateTime.currentSecsSinceEpoch()
        for x in infoTuple:
            print(x[-4].strftime('%Y-%m-%d %H:%M:%S'),type(x[-4].strftime('%Y-%m-%d %H:%M:%S')))
            former=QDateTime.fromString(x[-4].strftime('%Y-%m-%d %H:%M:%S'),"yyyy-MM-dd HH:mm:ss").toSecsSinceEpoch()
            latter=QDateTime.fromString(x[-3].strftime('%Y-%m-%d %H:%M:%S'),"yyyy-MM-dd HH:mm:ss").toSecsSinceEpoch()
            if former<=nowTimestamp and nowTimestamp<=latter:
                status="有效挂号"
            else:
                status="已失效"
            infoList.append(list(x)+[status])

        self.fill_tableview(infoList)
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

    @pyqtSlot(int)
    def show_delete_dialog(self,row):
        self.delete_row=row
        self.delete_dialog.show()


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