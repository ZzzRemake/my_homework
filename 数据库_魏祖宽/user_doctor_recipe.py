#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from pymysql.constants import CLIENT
from main_user_doctor_recipe import Ui_Dialog

from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import pyqtSlot, QCoreApplication,QDateTime,Qt,pyqtSignal

class UserDoctorRecipeView(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,rmno,parentWindow=None):
        self.rmno=rmno
        self.parentWindow=parentWindow
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)

        self.db = pymysql.connect(host="124.71.219.185",
                                  user="root",
                                  password="uestc2022!",
                                  charset="utf8mb4",
                                  database="cs2347.his",
                                  client_flag=CLIENT.MULTI_STATEMENTS)

        self.cursor = self.db.cursor()

        sql="""
            SELECT medicine.mname,medicine.mprice,recipe_detail.rdnumber,medicine.munit
            FROM `cs2347.medicine` medicine, `cs2347.recipe_detail` recipe_detail,
            `cs2347.recipe_master` recipe_master
            WHERE recipe_master.rmno={0} AND recipe_detail.rmno=recipe_master.rmno 
            AND medicine.mno=recipe_detail.mno
        """.format(str(self.rmno))
        self.cursor.execute(sql)
        data=self.cursor.fetchall()
        total=0.0
        self.textBrowser.append("药品清单")
        for i,x in enumerate(data):
            s="药品{0}：{1}    单价{2}, 共{3}{4}".format(str(i+1),x[0],str(x[1]),str(x[2]),x[3])
            total=total+float(x[1])*float(x[2])
            self.textBrowser.append(s)
        self.textBrowser.append("总共花费{0}元！".format(str(total)))


    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()