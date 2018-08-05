# -*- coding: utf-8 -*-
"""
Created on Thus Jan  25 12:42:11 2018
@author: JRCHAN
Description: 计算参数设置界面，包括用电特性期望向量值和电力客户所在行业季度增长率两部分内容。
"""
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ReadWrite  

class WindowSet_CusPar(QtWidgets.QTableWidget,QtWidgets.QWidget): 
    def __init__(self, parent=None): 
        super(WindowSet_CusPar, self).__init__(parent)         
        #self.setWindowIcon(QIcon("res/ico/settingPath.ico"))         
        self.resize(600, 400)
        self.setWindowTitle(u"计算参数设置")
        self.initUI()
        self.center()        
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
        self.table = QtWidgets.QTableWidget(13,3)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setSpan(0, 0, 1, 3) # 其参数为： 要改变单元格的   1行数  2列数     要合并的  3行数  4列数
        self.table.setSpan(3, 0, 1, 3)
        
        #设置表头
        HeaderLine0=([u"用电特性期望值",u"所在行业季度增长率"])
        HeaderLine0Index=[0,3]
        for i in range(0,2):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine0[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setForeground(QColor(200,111,30))
            newItem.setFlags(Qt.NoItemFlags)
            newItem.setBackground(QColor(245,245,245))
            self.table.setItem(HeaderLine0Index[i], 0, newItem)

        HeaderLine1=([u"峰（%）",u"谷（%）",u"平（%）",u"定性指标",u"  两季度前增长率（%） ",u"  一季度前增长率（%） ",u"农、林、牧、渔业",u"采矿业",u"制造业",u"电力、燃气及水的生产和供应",u"建筑业",u"交通运输、仓储、邮政业",u"金融、房地产、商务及居民服务业",u"公共事业及管理组织"])
        HeaderLine1Index=[1,1,1,4,4,4,5,6,7,8,9,10,11,12]
        HeaderLine1Index2=[0,1,2,0,1,2,0,0,0,0,0,0,0,0] 
        for i in range(0,14):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine1[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            newItem.setForeground(QColor(256,256,256))
            newItem.setFlags(Qt.NoItemFlags)
            self.table.setItem(HeaderLine1Index[i], HeaderLine1Index2[i], newItem)
            
        #self.table.resizeColumnsToContents()   #将列调整到跟内容大小相匹配
        #self.table.resizeRowsToContents()      #将行大小调整到跟内容的大学相匹配
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header = self.table.verticalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        Result=self.Readdata()
        index=0
        for i in range(2,13):
            for j in range(0,3):
                if i==2 or ( i!=3 and i!=4 and j!=0):
                    newItem = QtWidgets.QTableWidgetItem(str(Result[index]))
                    newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(i, j, newItem)
                    index += 1
        layout.addWidget(self.table)
        
        empty = QtWidgets.QLabel()
        layout.addWidget(empty)

        btn_saved = QtWidgets.QPushButton(u"确定")
        btn_quit = QtWidgets.QPushButton(u"取消")
        #设置界面布局
        buttonLayout =QtWidgets.QHBoxLayout()
        spancerItem2 =QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        buttonLayout.addItem(spancerItem2)
        buttonLayout.addWidget(btn_saved)
        buttonLayout.addWidget(btn_quit)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        btn_saved.clicked.connect(self.Savedata)
        btn_quit.clicked.connect(self.Close)

                            
    def Readdata(self):
        Result = ['1']*19
        # read the file and load values
        FileAdr = 'Log/CusPar.txt'
        ResBuff = []
        if os.path.exists(FileAdr):
            ResBuff = ReadWrite.Read(FileAdr)
        if len(ResBuff) == len(Result):
            Result = ResBuff
        return Result
                
    def Savedata(self):
        ListOfStr=[]
        flag=1
        for i in range(2,13):
            for j in range(0,3):
                if i==2 or ( i!=3 and i!=4 and j!=0):
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
            ReadWrite.Write('Log/CusPar.txt',ListOfStr)
            self.close()
        
    def Close(self):
        self.close()