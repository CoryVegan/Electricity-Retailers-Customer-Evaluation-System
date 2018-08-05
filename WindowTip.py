# -*- coding: utf-8 -*-
"""
Created on Thus Jan  25 16:42:21 2018
@author: JRCHAN
Description: 输入检验，提示输入所有参数
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class WindowTip(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WindowTip, self).__init__(parent) 
        self.resize(250, 100)
        self.setWindowTitle(u"警告") 
        self.newWindowUI()
        self.center()
    #窗格居中
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #弹出小窗格，提示输入所有参数  
    def newWindowUI(self):
        user = QtWidgets.QLabel(u"  请输入所有参数!")
        user.setFont(QFont("Roman times",18)) 
        layout =QtWidgets.QVBoxLayout()
        layout.addWidget(user)
        self.setLayout(layout)