#!/usr/bin/python3
# -*- coding: utf-8 -*-


from main_root import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot,QCoreApplication


class rootWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parentWindow=None):
        self.parentWindow=parentWindow
        QtWidgets.QMainWindow.__init__(self,parentWindow)
        self.setupUi(self)
        self.setWindowTitle("管理员控制面板")

    @pyqtSlot()
    def on_pushButton_patient_clicked(self):
        import patient_view
        self.patient_window=patient_view.PatientWindow(self)
        self.hide()

        self.patient_window.show()

    @pyqtSlot()
    def on_pushButton_dept_clicked(self):
        import dept_view
        self.dept_window=dept_view.DeptView(self)
        self.hide()
        self.dept_window.show()

    @pyqtSlot()
    def on_pushButton_staff_clicked(self):
        import staff_control
        self.staff_control=staff_control.StaffControlDialog(self)
        self.hide()
        self.staff_control.show()

    @pyqtSlot()
    def on_pushButton_medicine_clicked(self):
        import medicine_control
        self.medicine_control=medicine_control.MedicineControlDialog(self)
        self.hide()
        self.medicine_control.show()

    @pyqtSlot()
    def on_pushButton_register_clicked(self):
        import register_view
        self.register_control=register_view.RegisterView(self)
        self.hide()
        self.register_control.show()

    @pyqtSlot()
    def on_pushButton_diagnosis_clicked(self):
        import diagnosis_control
        self.diagnosis_view=diagnosis_control.DiagnosisControlDialog(self)
        self.hide()
        self.diagnosis_view.show()

    @pyqtSlot()
    def on_pushButton_charge_clicked(self):
        import fee_view
        self.fee_view=fee_view.FeeView(self)
        self.hide()
        self.fee_view.show()

    @pyqtSlot()
    def on_pushButton_user_clicked(self):
        import admin_control
        self.user_control=admin_control.UserControlDialog(self)
        self.hide()
        self.user_control.show()

    @pyqtSlot()
    def on_pushButton_exit_clicked(self):
        QCoreApplication.quit()

    @pyqtSlot()
    def on_pushButton_switch_clicked(self):
        self.close()
        self.parentWindow.lineEdit_username.clear()
        self.parentWindow.lineEdit_password.clear()
        self.parentWindow.show()

if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=rootWindow()
    window.show()
    sys.exit(app.exec_())