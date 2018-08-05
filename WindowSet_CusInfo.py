# -*- coding: utf-8 -*-
"""
Created on Thus Feb  1 15:32:21 2018
@author: JRCHAN
Description: 以excel的形式导入客户信息，并对定量定性指标进行处理。
"""
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import ReadWrite 
import core# Computational Algorithms 

class WindowSet_CusInfo(QtWidgets.QTableWidget,QtWidgets.QWidget): 
    def __init__(self, Infilename,parent=None): 
        super(WindowSet_CusInfo, self).__init__(parent)         
        #self.setWindowIcon(QIcon("res/ico/settingPath.ico"))         
        self.resize(1080, 600)
        self.setWindowTitle(u"客户信息录入")
        self.PreviewFile(Infilename)
        self.initUI()        
        self.center()        
    #读取导入的客户信息并进行预览          
    def PreviewFile(self,Infilename):
        if os.path.exists(Infilename):
            data = xlrd.open_workbook(Infilename)
            self.exceltable = data.sheets()[0]
            
            rows=self.exceltable.nrows   #获取行数 
            cols=self.exceltable.ncols   #获取列数
            for i in range(0,rows):
                for j in range(0,cols):
                    if self.exceltable.cell(i,j).value == u"客户":
                        self.KehuRow=i
                        self.KehuCol=j
                        break
                        break
            self.counter = 0 #客户数量
            maxcounter=len(self.exceltable.col_values(self.KehuCol))
            for i in range(0,maxcounter-self.KehuRow-4):
                if self.exceltable.cell(self.KehuRow+4+self.counter,self.KehuCol).value != '':
                    self.counter += 1
    #窗格居中           
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #窗格初始化          
    def initUI(self):
        layout =QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        
        ColUseable=20
        #设置窗格大小、表格行列数等
        self.table = QtWidgets.QTableWidget(self.counter+4,ColUseable+1)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        self.table.setColumnWidth(3, 180)
        self.table.setColumnWidth(1, 250)
        
        self.table.setSpan(0, 0, 4, 1)
        self.table.setSpan(0, 1, 4, 1) # 其参数为： 要改变单元格的   1行数  2列数     要合并的  3行数  4列数
        self.table.setSpan(0, 2, 1, 8)
        self.table.setSpan(0, 10, 1, 4)
        self.table.setSpan(0, 14, 1, 7)
        
        self.table.setSpan(1, 2, 2, 1)
        self.table.setSpan(1, 3, 2, 1)
        self.table.setSpan(1, 4, 2, 1)
        self.table.setSpan(1, 5, 2, 1)
        self.table.setSpan(1, 6, 3, 1)
        self.table.setSpan(1, 7, 1, 3)
        self.table.setSpan(1, 10, 3, 1)
        self.table.setSpan(1, 11, 3, 1)
        self.table.setSpan(1, 12, 3, 1)
        self.table.setSpan(1, 13, 3, 1)
        self.table.setSpan(1, 14, 3, 1)
        self.table.setSpan(1, 15, 1, 2)
        self.table.setSpan(1, 16, 1, 3)
        self.table.setSpan(1, 20, 2, 1)
        
        self.table.setSpan(2, 7, 1, 3)
        self.table.setSpan(2, 15, 2, 1)
        self.table.setSpan(2, 16, 2, 1)
        self.table.setSpan(2, 17, 2, 1)
        self.table.setSpan(2, 18, 2, 1)
        self.table.setSpan(2, 19, 2, 1)
        
        self.table.setSpan(3, 2, 1, 2)
        
        #设置表头
        HeaderLine0=([u"序号",u"客户",u"售电盈利", u"客户忠实度", u"售电风险"])
        HeaderLine0Index=[0,1,2,10,14]
        for i in range(0,4):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine0[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            self.table.setItem(0, HeaderLine0Index[i], newItem)        
 
        HeaderLine1=([u"2016年平均电价",u"平均电价（根据峰谷平电价估算；峰谷平耗电量相同）", u"电费成本占总成本比例", u"年均总用电量",u"用电量是增长趋势还是降低趋势", u"用电特性",
                     u"是否与华能有过合作", u"倾向于长期合同还是短期合作", u"所需增值服务的种类数量",u"所需其他能源的种类数量",
                     u"企业性质",u"所在行业", u"企业类型", u"年利润"])
        HeaderLine1Index=[2,3,4,5,6,7,10,11,12,13,14,15,17,20]
        for i in range(0,14):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine1[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            self.table.setItem(1, HeaderLine1Index[i], newItem)

        HeaderLine2=([u"峰谷平用电比例",u"类别", u"细目", u"是否高新技术产业",u"单位能耗是否低于省同行业平均水平",u"单位能耗是否低于全国同行业平均水平"])
        HeaderLine2Index=[7,15,16,17,18,19]
        for i in range(0,6):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine2[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            self.table.setItem(2, HeaderLine2Index[i], newItem)

        HeaderLine3=([u"（元/千瓦时）",u"（%）", u"（万千瓦时）", u"（%）",u"（%）",u"（%）",u"（万）"])
        HeaderLine3Index=[2,4,5,7,8,9,20]
        for i in range(0,7):
            newItem = QtWidgets.QTableWidgetItem(HeaderLine3[i])
            newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
            self.table.setItem(3, HeaderLine3Index[i], newItem)              

        #将客户信息显示在表格中
        for i in range(0,self.counter):
            for j in range(0,21):
                if j==0:
                    content=str(i+1)
                else:
                    content=str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j-1).value)
                newItem = QtWidgets.QTableWidgetItem(content)
                newItem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
                self.table.setItem(i+4, j, newItem)  
        
        layout.addWidget(self.table)
        
        empty = QtWidgets.QLabel()
        layout.addWidget(empty)

        btn_saved = QtWidgets.QPushButton(u"确定")
        btn_quit = QtWidgets.QPushButton(u"取消")
        #表格布局
        buttonLayout =QtWidgets.QHBoxLayout()
        spancerItem2 =QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        buttonLayout.addItem(spancerItem2)
        buttonLayout.addWidget(btn_saved)
        buttonLayout.addWidget(btn_quit)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        btn_saved.clicked.connect(self.Savedata)
        btn_quit.clicked.connect(self.Close)

                
    def Savedata(self):
        List=self.DataTrans()
        wrj,Name=core.ObjWeightCal(List)
        core.ObjWeightFig(wrj,Name)
        #将客户名字存储
        ListOfName=[]
        for i in range(0,self.counter):
            ListOfName.append(str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol).value))
            ListOfName.append('\n')
        ReadWrite.Write('Log/CusName.txt',ListOfName)
        self.close()

    #根据预定规则量化定性指标    
    def DataTrans(self):
        numsList = []
        IndusTypeValue=core.IndusType()
        for i in range(0,self.counter):
            numsList.append([])
            CompanyType=0
            FengGuPing=[]
            for j in range(0,19):
                if j==4:
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'快速降低':
                        content= 1
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'缓慢降低':
                        content= 3
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'降低':
                        content= 4
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'持平':
                        content= 5
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'增长':
                        content= 6
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'缓慢增长':
                        content= 7
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'快速增长':
                        content= 9
                elif j==5 or j==6 or j==7:
                    FengGuPing.append(float(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value))
                    if j==7:
                        content= core.Muti2SingDimen(FengGuPing)                    
                elif j==8:
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'否':
                        content= 1
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'是':
                        content= 9
                elif j==9:
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'短期':
                        content= 1
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'都可以':
                        content= 5
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'长期':
                        content= 9
                elif j==12:
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'外商独资':
                        content= 1
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'民营':
                        content= 3
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'合资':
                        content= 5
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'股份制':
                        content= 7
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'其他国企':
                        content= 8
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'央企':
                        content= 9
                elif j==13:
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'农、林、牧、渔业':
                        content= IndusTypeValue[0]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'采矿业':
                        content= IndusTypeValue[1]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'制造业':
                        content= IndusTypeValue[2]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'电力、燃气及水的生产和供应':
                        content= IndusTypeValue[3]  
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'建筑业':
                        content= IndusTypeValue[4]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'交通运输、仓储、邮政业':
                        content= IndusTypeValue[5]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'金融、房地产、商务及居民服务业':
                        content= IndusTypeValue[6]
                    elif str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'公共事业及管理组织':
                        content= IndusTypeValue[7]
                elif j==15 or j==16 or j==17 :
                    if str(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)==u'是':
                        CompanyType += 1
                    if j==17:
                        if CompanyType==3:
                            content= 9
                        elif CompanyType==2:
                            content= 6
                        elif CompanyType==1:
                            content= 3
                        else:
                            content= 1
                elif j==18:
                    val = float(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)
                    if val<-1000:
                        content= 1
                    elif val>=-1000 and val<-500:
                        content= 2
                    elif val>=-500 and val<0:
                        content= 3
                    elif val>=0 and val<500:
                        content= 4
                    elif val>=500 and val<1000:
                        content= 5
                    elif val>=1000 and val<1500:
                        content= 6
                    elif val>=1500 and val<2000:
                        content= 7
                    elif val>=2000 and val<2500:
                        content= 8
                    elif val>=2500:
                        content= 9                           
                elif j==1 or j==2 or j==3 or j==10 or j==11:                     
                    content=float(self.exceltable.cell(self.KehuRow+4+i,self.KehuCol+j+1).value)
                if  j!=0 and j!=5 and j!=6 and j!=14 and j!=15 and j!=16 :                    
                    numsList[i].append(content)
        return numsList

        
    def Close(self):
        self.close()
