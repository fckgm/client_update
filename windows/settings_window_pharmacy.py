# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window_pharmacy.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Client_settings(object):
    def setupUi(self, Client_settings):
        Client_settings.setObjectName("Client_settings")
        Client_settings.resize(270, 240)
        self.centralwidget = QtWidgets.QWidget(Client_settings)
        self.centralwidget.setObjectName("centralwidget")
        self.lab_group = QtWidgets.QLabel(self.centralwidget)
        self.lab_group.setGeometry(QtCore.QRect(20, 30, 61, 16))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(9)
        self.lab_group.setFont(font)
        self.lab_group.setObjectName("lab_group")
        self.cb_group = QtWidgets.QComboBox(self.centralwidget)
        self.cb_group.setGeometry(QtCore.QRect(110, 25, 141, 21))
        self.cb_group.setObjectName("cb_group")
        self.lab_pharmacy = QtWidgets.QLabel(self.centralwidget)
        self.lab_pharmacy.setGeometry(QtCore.QRect(20, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(9)
        self.lab_pharmacy.setFont(font)
        self.lab_pharmacy.setObjectName("lab_pharmacy")
        self.et_pharmacy = QtWidgets.QLineEdit(self.centralwidget)
        self.et_pharmacy.setGeometry(QtCore.QRect(110, 68, 141, 21))
        self.et_pharmacy.setObjectName("et_pharmacy")
        self.lab_device = QtWidgets.QLabel(self.centralwidget)
        self.lab_device.setGeometry(QtCore.QRect(20, 110, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lab_device.setFont(font)
        self.lab_device.setObjectName("lab_device")
        self.cb_device = QtWidgets.QComboBox(self.centralwidget)
        self.cb_device.setGeometry(QtCore.QRect(110, 107, 141, 21))
        self.cb_device.setObjectName("cb_device")
        self.lab_status = QtWidgets.QLabel(self.centralwidget)
        self.lab_status.setGeometry(QtCore.QRect(20, 210, 111, 16))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        self.lab_status.setFont(font)
        self.lab_status.setStyleSheet("")
        self.lab_status.setText("")
        self.lab_status.setObjectName("lab_status")
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(110, 145, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(9)
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.btn_update = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update.setGeometry(QtCore.QRect(215, 190, 35, 35))
        self.btn_update.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_update.setIcon(icon)
        self.btn_update.setObjectName("btn_update")
        self.btn_quit_and_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit_and_start.setGeometry(QtCore.QRect(170, 190, 35, 35))
        self.btn_quit_and_start.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/quit_and_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_quit_and_start.setIcon(icon1)
        self.btn_quit_and_start.setObjectName("btn_quit_and_start")
        Client_settings.setCentralWidget(self.centralwidget)

        self.retranslateUi(Client_settings)
        QtCore.QMetaObject.connectSlotsByName(Client_settings)

    def retranslateUi(self, Client_settings):
        _translate = QtCore.QCoreApplication.translate
        Client_settings.setWindowTitle(_translate("Client_settings", "Настройка клиента"))
        self.lab_group.setText(_translate("Client_settings", "Группа:"))
        self.lab_pharmacy.setText(_translate("Client_settings", "Аптека:"))
        self.lab_device.setText(_translate("Client_settings", "Устройство:"))
        self.btn_save.setText(_translate("Client_settings", "Записать"))
