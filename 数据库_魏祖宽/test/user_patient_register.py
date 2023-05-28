#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT

import main_user_patient_register
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit,QDateTimeEdit,QTextEdit,QLabel
from PyQt5.QtCore import pyqtSlot, QDate, QCoreApplication,QDateTime


class UserPatientRegisterDialog(QDialog, main_user_patient_register.Ui_Dialog):

    def __init__(self,username, parentNew=None):
        self.username=username
        self.fee=0
        self.parentWindow = parentNew
        QDialog.__init__(self, parentNew)
        self.setupUi(self)
        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()
        self.set_origin_status()
        self.comboBox_dept.currentIndexChanged.connect(self.dept_to_doctor)
        self.comboBox_doctor.currentIndexChanged.connect(self.doctor_to_fee)

    def set_origin_status(self)->None:
        nowDatetime=QDateTime.currentDateTime()
        self.dateTimeEdit_time.setDateTime(nowDatetime)
        self.comboBox_dept.clear()
        self.comboBox_dept.addItem("请选择预约科室")
        self.comboBox_doctor.clear()
        self.comboBox_doctor.addItem("请选择预约医生")
        self.textEdit.clear()
        self.label_fee.clear()
        self.label_fee.setText("预约费用：0.00元")
        self.label_warning.clear()

        sql="""
        SELECT deptno,deptname FROM `cs2347.dept`
        """
        self.cursor.execute(sql)
        dept=self.cursor.fetchall()
        self.dept2no={}
        for id,name in dept:
            self.comboBox_dept.addItem(name)
            self.dept2no[name]=id

    def dept_to_doctor(self,index):
        self.comboBox_doctor.clear()
        self.comboBox_doctor.addItem("请选择预约医生")
        if index<=0:
            return None
        deptname=self.comboBox_dept.itemText(index)

        self.deptno=self.dept2no[deptname]
        sql="""
            SELECT dno,dname FROM `cs2347.doctor` WHERE deptno={0}
        """.format(str(self.deptno))
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        self.doctor2no={}
        for id,name in data:
            self.comboBox_doctor.addItem(name)
            self.doctor2no[name]=id

    def doctor_to_fee(self,index):
        if index<=0:
            return None
        print(index)
        print(self.doctor2no)
        self.dno=self.doctor2no[self.comboBox_doctor.itemText(index)]
        sql="""
        SELECT title.tfee FROM `cs2347.doctor` doctor, `cs2347.title` title
        WHERE doctor.dno={0} AND doctor.dtno=title.tno
        """.format(str(self.dno))
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        if len(data)==1:
            print(data)
            self.fee=data[0][0]
            self.label_fee.setText("预约费用：{0}元".format(str(self.fee)))


    @pyqtSlot()
    def on_pushButton_submit_clicked(self):
        nowDateTime=QDateTime.currentDateTime().toSecsSinceEpoch()
        regDateTime=self.dateTimeEdit_time.dateTime().toSecsSinceEpoch()
        if regDateTime<nowDateTime:
            self.label_warning.setText("错误：预约时间不合法")
            return None
        if self.comboBox_dept.currentIndex()==0 or self.comboBox_doctor.currentIndex()==0:
            self.label_warning.setText("错误：请正确选择科室或医生！")
            return None
        regTime=self.dateTimeEdit_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        nowTime=QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        strText=self.textEdit.toPlainText()

        sql="""
        SELECT pno FROM `cs2347.patient` WHERE padmin='{0}'
        """.format(self.username)
        print(sql)
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        if len(data)==1:
            self.pno=data[0][0]
        else:
            print(data)
            print("Error in pno!")
            return None
        try:
            sql="""
                INSERT INTO `cs2347.register_form` (
                    RFcashier, RFdept,RFdoctor,RFnotes,RFpatient,RFtime,RFvisittime
                ) VALUES (
                    NULL,{0},{1},'{2}',{3},'{4}','{5}'
                )
            """.format(str(self.deptno),str(self.dno),strText,str(self.pno),regTime,nowTime)
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            self.label_warning.setText("挂号成功！")
        except Exception:
            print(Exception)
            self.db.rollback()
            self.label_warning.setText("挂号失败！")
        self.set_origin_status()


    @pyqtSlot()
    def on_pushButton_now_clicked(self):
        import user_patient_register_valid
        self.patient_register_valid=user_patient_register_valid.PatientRegisterValidView(self.username,self)
        self.hide()
        self.patient_register_valid.show()

    @pyqtSlot()
    def on_pushButton_history_clicked(self):
        import user_patient_register_history
        self.patient_register_history=user_patient_register_history.PatientRegisterValidView(self.username,self)
        self.hide()
        self.patient_register_history.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
