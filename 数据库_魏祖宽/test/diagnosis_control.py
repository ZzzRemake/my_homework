#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main_diagnosis_control import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication

class DiagnosisControlDialog(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self,parentWindow=None):
        print("COntrol!")
        self.parentWindow=parentWindow
        QtWidgets.QDialog.__init__(self,parentWindow)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_diagnosis_clicked(self):
        print("diagnosis")
        import diagnosis_view
        self.diagnosis_window=diagnosis_view.DiagnosisView(self)
        self.hide()
        self.diagnosis_window.show()

    @pyqtSlot()
    def on_pushButton_recipe_master_clicked(self):
        import recipe_master_view
        self.recipe_master_window=recipe_master_view.RecipeMasterView(self)
        self.hide()
        self.recipe_master_window.show()


    @pyqtSlot()
    def on_pushButton_recipe_detail_clicked(self):
        import recipe_detail_view
        self.recipe_detail_window=recipe_detail_view.RecipeDetailView(self)
        self.hide()
        self.recipe_detail_window.show()

    @pyqtSlot()
    def on_pushButton_back_clicked(self):
        self.close()
        self.parentWindow.show()
