# -*- coding: utf-8 -*-
"""
Created on Tue Feb  13 17:12:25 2018
@author: JRCHAN
Description: 展示已经计算好的排序结果
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

class WindowSortedCus(QtWidgets.QTableWidget,QtWidgets.QWidget): 
    def __init__(self,sorted_Ci,sorted_CusName, parent=None): 
        super(WindowSortedCus, self).__init__(parent)                 
        self.resize(2*self.sizeHint())
        self.setWindowTitle(u"排序结果展示")
        self.initUI(sorted_Ci,sorted_CusName)
        self.center()                
    #窗格居中              
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
               
    def initUI(self,sorted_Ci,sorted_CusName):
        #设置界面布局
        layout =QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        self.table = QtWidgets.QTableWidget(28,2)
        self.table.setHorizontalHeaderLabels([u"客户（排序越小越优）", u"综合评价测度"])
        for i in range(len(sorted_Ci)):
            textFont = QFont("song", 13, QFont.Bold) 
            newItem = QtWidgets.QTableWidgetItem(str(sorted_CusName[i]))
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)#行列均居中
            newItem.setFont(textFont) 
            self.table.setItem(i,0,newItem)
            newItem = QtWidgets.QTableWidgetItem(str(round(sorted_Ci[i],5)))
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setFont(textFont) 
            self.table.setItem(i,1,newItem)
        for x in range(2):  
            headItem = self.table.horizontalHeaderItem(x)   #获得水平方向表头的Item对象  
            headItem.setFont(textFont)         
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        #self.table.resizeColumnsToContents()   #将列调整到跟内容大小相匹配
        #self.table.resizeRowsToContents()      #将行大小调整到跟内容的大学相匹配
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header = self.table.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.setLayout(layout)