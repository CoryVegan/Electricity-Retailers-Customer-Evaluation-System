# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 19:39:52 2017
@author: JRCHAN
Description: This is the mainwindow after logining.
"""
import core# computational algorithms and results visualization 
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
import WindowSetA_B,WindowSetB1_C,WindowSetB2_C,WindowSetB3_C
import WindowSet_CusPar,WindowSet_CusInfo,WindowSortedCus

MainFile = "File\主窗口.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainFile)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(" ")
        jpg=QPixmap('File/backgroundpic.jpg')
        self.labelpic.setPixmap(jpg)
        self.labelpic.show()
        png=QPixmap('File/EvaluaStrupic.PNG')     
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()
        
        #关联信号
        self.ButtonShow.clicked.connect(self.EvaluaStruShow)
        
        self.Button11.clicked.connect(self.OpenWindowSetA_B)
        self.Button12.clicked.connect(self.OpenWindowSetB1_C)
        self.Button13.clicked.connect(self.OpenWindowSetB2_C)
        self.Button14.clicked.connect(self.OpenWindowSetB3_C)
        self.Button15.clicked.connect(self.SubWeightShow)
        
        self.Button21.clicked.connect(self.OpenWindowSet_CusPar)
        self.Button22.clicked.connect(self.OpenWindowSet_CusInfo)
        self.Button23.clicked.connect(self.ObjWeightShow)
        
        self.Button31.clicked.connect(self.OpenWholeWeightCal)        
        self.Button32.clicked.connect(self.OpenITOPSIS) 
    #Show logo
    def EvaluaStruShow(self):
        png=QPixmap('File/EvaluaStrupic.PNG')     
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()
    #click信号打开新窗格    
    def OpenWindowSetA_B(self):
        self.another1 = WindowSetA_B.WindowSetA_B()
        self.another1.show()
    def OpenWindowSetB1_C(self):
        self.another2 = WindowSetB1_C.WindowSetB1_C()
        self.another2.show()
    def OpenWindowSetB2_C(self):
        self.another3 = WindowSetB2_C.WindowSetB2_C()
        self.another3.show()
    def OpenWindowSetB3_C(self):
        self.another4 = WindowSetB3_C.WindowSetB3_C()
        self.another4.show()        
    def SubWeightShow(self):
        png=QPixmap('Img/主观权重展示图.PNG')     
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()
    #用户参数设置 
    def OpenWindowSet_CusPar(self):
        self.another5 = WindowSet_CusPar.WindowSet_CusPar()
        self.another5.show()     
    def OpenWindowSet_CusInfo(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, u'选择文件','./',"Excel files(*.xlsx *.xls)") #,"Txt files(*.txt)"
        if '.xlsx' in str(filename) or '.xls' in str(filename):           
            #self.PreviewFile()  
            self.another6 = WindowSet_CusInfo.WindowSet_CusInfo(filename[0])
            self.another6.show()    
    def ObjWeightShow(self):
        png=QPixmap('Img/客观权重展示图.PNG')     
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()
                
    def OpenWholeWeightCal(self):
        core.WholeWeightCal()
        png=QPixmap('Img/综合权重展示图.PNG')
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()        
    def OpenITOPSIS(self):
        sorted_Ci,sorted_CusName=core.ITOPSISCal()
        core.PlotCurve(sorted_Ci)
        png=QPixmap("Img/电力客户评估结果图.png")
        self.labelcontent.setPixmap(png)
        self.labelcontent.show()        
        self.another7 = WindowSortedCus.WindowSortedCus(sorted_Ci,sorted_CusName)
        self.another7.show()
        

