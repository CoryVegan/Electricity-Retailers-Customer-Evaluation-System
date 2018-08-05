# -*- coding: utf-8 -*-
"""
Created on Thus Jan  25 09:11:38 2018
@author: JRCHAN
Description: 准则层B（客户忠实度）-准则层C主观权重设置
"""
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import ReadWrite 
import core # Computational Algorithms

class WindowSetB2_C(QtWidgets.QTableWidget,QtWidgets.QWidget): 
    def __init__(self, parent=None): 
        super(WindowSetB2_C, self).__init__(parent)         
        #self.setWindowIcon(QIcon("res/ico/settingPath.ico"))         
        self.resize(700, 320)
        self.setWindowTitle(u"准则层B2-准则层C")
        self.initUI()
        self.center()        
        self.table.cellChanged.connect(self.cellchanged)
    #主观权重矩阵为对称矩阵，所以权重表格中内容发生变化时，对应行列的内容也要发生变化    
    def cellchanged(self):
        curCol = self.table.currentColumn()
        curRow = self.table.currentRow()
        if(self.table.currentItem().text() and curCol!=curRow):            
            text = float(self.table.currentItem().text())
            self.table.item(curCol,curRow).setText(str(round(1/text,4)))
            flag2=self.Calcu_CR_Judgment()
            if(flag2):
                for j in range(0,4):
                    self.table.item(4,j).setText(str(round(self.Ave_Wp[j].real,4)))
                self.table.item(5,0).setText(str(round(self.CI.real,6)))
                self.table.item(6,0).setText(str(self.RI.real))
                self.table.item(7,0).setText(str(round(self.CR.real,6)))
                if(self.CR.real>0.1):
                    self.table.item(7,0).setBackground(QColor(255,0,0))
                    self.table.item(7,0).setForeground(QColor(256,256,256))
                else:
                    self.table.item(7,0).setBackground(QColor(255,255,255))            
        elif(curCol!=curRow):
            self.table.item(curCol,curRow).setText('')         
    #窗格居中             
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #窗格界面初始化             
    def initUI(self):
        layout =QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        #设置窗格大小，表格行列数等
        self.table = QtWidgets.QTableWidget(8,4)
        self.table.setHorizontalHeaderLabels([u"合作基础（C6）", u"合同期限（C7）", u"增值服务（C8）", u"多联供需求（C9）"])
        self.table.setVerticalHeaderLabels([u"合作基础（C6）", u"合同期限（C7）", u"增值服务（C8）", u"多联供需求（C9）", u"重要性权重（WCij）", u"一致性指标（CI）", u"平均随机一致性指标（RI）", u"一致性比例（CR）"])
        self.table.setSpan(5, 0, 1, 4) # 其参数为： 要改变单元格的   1行数  2列数     要合并的  3行数  4列数
        self.table.setSpan(6, 0, 1, 4)
        self.table.setSpan(7, 0, 1, 4)
        #self.table.resizeColumnsToContents()   #将列调整到跟内容大小相匹配
        #self.table.resizeRowsToContents()      #将行大小调整到跟内容的大学相匹配
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header = self.table.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Result=self.Readdata()
        for i in range(0,4):
            for j in range(0,4):
                newItem = QtWidgets.QTableWidgetItem(Result[4*i+j])
                newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
                if i==j:
                    newItem.setFlags(Qt.NoItemFlags)
                    newItem.setForeground(QColor(256,256,256))
                self.table.setItem(i, j, newItem)

        self.Calcu_CR_Judgment()#进行一致性检验
        #在表格中填入数据
        for j in range(0,4):
            newItem = QtWidgets.QTableWidgetItem(str(round(self.Ave_Wp[j].real,4)))
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setFlags(Qt.NoItemFlags)
            newItem.setForeground(QColor(256,256,256))
            newItem.setBackground(QColor(255,239,213))
            self.table.setItem(4, j, newItem)           
        newItem = QtWidgets.QTableWidgetItem(str(round(self.CI.real,6)))
        newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
        newItem.setFlags(Qt.NoItemFlags)
        self.table.setItem(5, 0, newItem)            
        newItem = QtWidgets.QTableWidgetItem(str(self.RI.real))
        newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
        newItem.setFlags(Qt.NoItemFlags)
        self.table.setItem(6, 0, newItem)            
        newItem = QtWidgets.QTableWidgetItem(str(round(self.CR.real,6)))
        newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
        newItem.setFlags(Qt.NoItemFlags)
        self.table.setItem(7, 0, newItem)
        if(self.CR.real>0.1):
            self.table.item(7,0).setBackground(QColor(255,0,0))
            self.table.item(7,0).setForeground(QColor(256,256,256))
               
        layout.addWidget(self.table)
        
        empty = QtWidgets.QLabel()
        layout.addWidget(empty)

        btn_saved = QtWidgets.QPushButton(u"确定")
        btn_quit = QtWidgets.QPushButton(u"取消")
        #设置窗格布局
        buttonLayout =QtWidgets.QHBoxLayout()
        spancerItem2 =QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        buttonLayout.addItem(spancerItem2)
        buttonLayout.addWidget(btn_saved)
        buttonLayout.addWidget(btn_quit)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        btn_saved.clicked.connect(self.Savedata)
        btn_quit.clicked.connect(self.Close)
    #进行一致性指标CI、平均随机一致性指标RI、和一致性比例CR计算
    def Calcu_CR_Judgment(self):
        List=[]
        flag2=1
        for i in range(0,4):
            for j in range(0,4):
                if(self.table.item(i, j).text()):
                    text=float(self.table.item(i, j).text())
                    List.append(text)
                else:
                    flag2=0
                    break
                    break 
        if(flag2):
            self.Ave_Wp,self.CI,self.RI,self.CR = core.CR_Judgment(List,4)
        return flag2
    #取出存储在本地的上次数据            
    def Readdata(self):
        Result = ['1']*16
        # read the file and load values
        FileAdr = 'Log/DataB2toC.txt'
        ResBuff = []
        if os.path.exists(FileAdr):
            ResBuff = ReadWrite.Read(FileAdr)
        if len(ResBuff) == len(Result):
            Result = ResBuff
        return Result
     #存储本次计算结果                 
    def Savedata(self):
        ListOfStr=[]
        flag=1
        for i in range(0,4):
            for j in range(0,4):
                if(self.table.item(i, j).text()):
                    text=str(self.table.item(i, j).text())
                    ListOfStr.append(text)
                    ListOfStr.append('\n')
                else:
                    flag=0
                    self.newWindow = WindowTip()
                    self.newWindow.show()
                    #newWindow.exec_()
                    break
                    break                
        if(flag):
            ReadWrite.Write('Log/DataB2toC.txt',ListOfStr)
            self.close()
            core.SubWeightFig()
            
    def Close(self):
        self.close()