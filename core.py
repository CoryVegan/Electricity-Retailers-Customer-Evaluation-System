# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 23:00:06 2018
@author: JRCHAN
Description: 
Computational algorithms and results visualization. 
    
"""
import numpy as np
import math
import copy
import matplotlib.pyplot as plt
plt.ioff()
import matplotlib.font_manager

#import os
def CR_Judgment(Result,r):
    if r==3:
        x = np.array([Result[0:r], Result[r:2*r], Result[2*r:3*r]])
    elif r==4:
        x = np.array([Result[0:r], Result[r:2*r], Result[2*r:3*r], Result[3*r:4*r]])
    elif r==5:
        x = np.array([Result[0:r], Result[r:2*r], Result[2*r:3*r], Result[3*r:4*r], Result[4*r:5*r]])    
    e,v = np.linalg.eig(x)    
    sorted_e=np.argsort(e)
    Wp=v[:,sorted_e[r-1]]
    sum_Wp=sum(Wp)
    Ave_Wp=Wp/sum_Wp
    lamda = e[sorted_e[r-1]]
    CI=(lamda-r)/(r-1)
    RI=[0, 0, 0.52, 0.89, 1.11]
    CR=CI/RI[r-1]
   
    return Ave_Wp,CI,RI[r-1],CR
#峰谷平三指标归一指标
def Muti2SingDimen(FengGuPingB):
    Result = Read2('Log/CusPar.txt')
    FengGuPingA=Result[0:3]
    a=0
    b=0
    c=0
    for i in range(0,3):
        a += (FengGuPingA[i]*FengGuPingB[i])
        b += (FengGuPingA[i]**2)
        c += (FengGuPingB[i]**2)
    cosAB = a/((b*c)**0.5)
    return cosAB
#行业类型   
def IndusType():
    Result = Read2('Log/CusPar.txt')
    IndusTypeValue=[]
    for i in range(0,8):
        IndusTypeValue.append(float(Result[3+2*i]+Result[4+2*i])/2)
    return IndusTypeValue
#客观权重计算   
def ObjWeightCal(numsList_In):
    numsList=copy.deepcopy(numsList_In)
    Xij=np.array(numsList_In)
    np.savetxt("Log/客户原始信息矩阵X.txt",Xij)
    #归一化求pij
    for column in range(len(numsList[0])):
        Max_Xj=numsList[0][column]
        Min_Xj=numsList[0][column]
        for i in range(len(numsList)):
            if Max_Xj<numsList[i][column]:
                Max_Xj=numsList[i][column]
            if Min_Xj>numsList[i][column]:
                Min_Xj=numsList[i][column]
        for i in range(len(numsList)):
            if (Max_Xj-Min_Xj)!=0:
                numsList[i][column]=((numsList[i][column])-Min_Xj)/(Max_Xj-Min_Xj)
            else:
                numsList[i][column]=0

    #删除全为0的列
    col_del=[]
    for column in range(len(numsList[0])):
        Flag=1
        for i in range(len(numsList)):
            if numsList[i][column]!= 0:
                Flag=0
        if Flag==1:
            col_del.append(column)
    
    numsList_del=[]        
    for i in range(len(numsList)):
        numsList_del.append([])
        for column in range(len(numsList[0])):
            if column not in col_del:
                numsList_del[i].append(numsList[i][column])                      
    #计算评估指标信息熵E
    ej = []
    for column in range(len(numsList_del[0])):
        total=0
        for i in range(len(numsList_del)):
            total += numsList_del[i][column]
        for i in range(len(numsList_del)):
            numsList_del[i][column] = numsList_del[i][column]/ total
    for column in range(len(numsList_del[0])):
        ej_value=0
        for i in range(len(numsList_del)):
            if numsList_del[i][column] != 0:
                ej_value += (numsList_del[i][column] * math.log(numsList_del[i][column]))
        ej_value=-ej_value/math.log(len(numsList_del))
        ej.append(ej_value)
    #计算评估指标原始客观权重Wt
    Wtj = []
    total=0
    for column in range(len(numsList_del[0])):
        total += ej[column]
    for column in range(len(numsList_del[0])):
        Wtj_value = (1-ej[column])/(len(numsList_del[0])-total)
        Wtj.append(Wtj_value)        
    #计算客观权重Wo
    total=0
    numej=0
    for column in range(len(numsList_del[0])):
        if ej[column] != 1:
            total += ej[column]
            numej+=1
    E=total/numej
    wrj = []
    for column in range(len(numsList_del[0])):
            wrj.append((1+E-ej[column])/numej)
     
    whole_wrj=[]
    index=0
    for column in range(len(numsList[0])):
        if column in col_del:
            whole_wrj.append(0)
            index += 1
        else:
            whole_wrj.append(wrj[column-index])

    WeightWrite('Log/ObjWeight.txt',whole_wrj)
    a=np.array(whole_wrj)
    Index=np.argsort(a)
    WeightName=[u"平均电价", u"电费成本占总成本比例", u"年均总用电量", u"用电量是增长/降低趋势", u"峰/谷/平用电量比例",
                   u"合作基础", u"合同期限", u"增值服务", u"多联供需求",
                   u"企业性质", u"所在行业", u"企业类型", u"年利润"]
    sorted_whole_wrj=[]
    sorted_WeightName=[]             
    for i in range(0,13):
        b=Index[i]
        sorted_whole_wrj.append(whole_wrj[b])
        sorted_WeightName.append(WeightName[b])   
   
    return sorted_whole_wrj,sorted_WeightName 
#客观指标权重图示
def ObjWeightFig(sorted_whole_wrj,sorted_WeightName):
    fig2 = plt.figure(1,figsize=(25,18)) 
    myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=20)
    title_myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=38)
    plt.title(u'客观权重展示图',fontproperties=title_myfont)
    plt.barh(range(len(sorted_whole_wrj)), sorted_whole_wrj,align='center',alpha=0.8,color='teal')
    for b,a in zip(range(len(sorted_whole_wrj)),sorted_whole_wrj):    
        plt.text(a+0.004, b, '%.3f' % a, ha='center', va= 'center',size=20)
    plt.xticks(size=25)    
    plt.yticks(range(len(sorted_whole_wrj)), sorted_WeightName,fontproperties=myfont)
    plt.grid(linestyle = "--",axis= 'x')
    #ax = plt.gca()
    #ax.spines['top'].set_visible(False)  #去掉上边框
    #ax.spines['right'].set_visible(False) #去掉右边框
    plt.xlim(0,max(sorted_whole_wrj)+0.01)
    plt.savefig("Img/客观权重展示图.png") #保存图                    
    plt.cla()
    plt.close()
#主观指标权重计算            
def SubWeightCal():
    Result = Read2('Log/DataAtoB.txt')
    w1t,CI,RI,CR = CR_Judgment(Result,3)
    Result = Read2('Log/DataB1toC.txt')
    w2j_1,CI,RI,CR = CR_Judgment(Result,5)        
    Result = Read2('Log/DataB2toC.txt')
    w2j_2,CI,RI,CR = CR_Judgment(Result,4)
    Result = Read2('Log/DataB3toC.txt')
    w2j_3,CI,RI,CR = CR_Judgment(Result,4)
    SubWeight=[]
    for i in range(0,5):
        SubWeight.append(w1t[0].real*w2j_1[i].real)
    for i in range(0,4):
        SubWeight.append(w1t[1].real*w2j_2[i].real)        
    for i in range(0,4):
        SubWeight.append(w1t[2].real*w2j_3[i].real)
    WeightWrite('Log/SubWeight.txt',SubWeight)
    a=np.array(SubWeight)
    Index=np.argsort(a)
    SubWeightName=[u"平均电价", u"电费成本占总成本比例", u"年均总用电量", u"用电量是增长/降低趋势", u"峰/谷/平用电量比例",
                   u"合作基础", u"合同期限", u"增值服务", u"多联供需求",
                   u"企业性质", u"所在行业", u"企业类型", u"年利润"]
    sorted_SubWeight=[]
    sorted_SubWeightName=[]             
    for i in range(0,13):
        b=Index[i]
        sorted_SubWeight.append(SubWeight[b])
        sorted_SubWeightName.append(SubWeightName[b])   
    return sorted_SubWeight,sorted_SubWeightName
#主观指标权重图示    
def SubWeightFig():
    sorted_SubWeight,sorted_SubWeightName= SubWeightCal() 
    fig1 = plt.figure(1,figsize=(25,18)) 
    myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=20)
    title_myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=38)
    plt.title(u'主观权重展示图',fontproperties=title_myfont)
    plt.barh(range(len(sorted_SubWeight)), sorted_SubWeight,align='center',alpha=0.6,color='teal')
    for b,a in zip(range(len(sorted_SubWeight)),sorted_SubWeight):    
        plt.text(a+0.004, b, '%.3f' % a, ha='center', va= 'center',size=20)
    plt.xticks(size=25)    
    plt.yticks(range(len(sorted_SubWeight)), sorted_SubWeightName,fontproperties=myfont)
    plt.grid(linestyle = "--",axis= 'x')
    #ax = plt.gca()
    #ax.spines['top'].set_visible(False)  #去掉上边框
    #ax.spines['right'].set_visible(False) #去掉右边框
    plt.xlim(0,max(sorted_SubWeight)+0.01)
    plt.savefig("Img/主观权重展示图.png") #保存图                    
    plt.cla()
    plt.close()
#综合指标权重计算     
def WholeWeightCal():
    SubWeight= Read2('Log/SubWeight.txt')
    ObjWeight= Read2('Log/ObjWeight.txt')
    total=0
    for i in range(0,len(SubWeight)):
        total += ((SubWeight[i]*ObjWeight[i])**0.5)    
    WholeWeight=[]
    for i in range(0,len(SubWeight)):
        WholeWeight.append(((SubWeight[i]*ObjWeight[i])**0.5)/total)
    WeightWrite('Log/WholeWeight.txt',WholeWeight)
    a=np.array(WholeWeight)
    Index=np.argsort(a)
    WeightName=[u"平均电价", u"电费成本占总成本比例", u"年均总用电量", u"用电量是增长/降低趋势", u"峰/谷/平用电量比例",
                   u"合作基础", u"合同期限", u"增值服务", u"多联供需求",
                   u"企业性质", u"所在行业", u"企业类型", u"年利润"]
    sorted_whole=[]
    sorted_WeightName=[]
    for i in range(0,13):
        b=Index[i]
        sorted_whole.append(WholeWeight[b])
        sorted_WeightName.append(WeightName[b])      
    WholeWeightFig(sorted_whole,sorted_WeightName)
#综合指标权重图示    
def WholeWeightFig(sorted_whole,sorted_WeightName):
    fig3 = plt.figure(1,figsize=(25,18)) 
    myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=20)
    title_myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=38)
    plt.title(u'综合权重展示图',fontproperties=title_myfont)
    plt.barh(range(len(sorted_whole)), sorted_whole,align='center',alpha=1,color='teal')
    for b,a in zip(range(len(sorted_whole)),sorted_whole):    
        plt.text(a+0.004, b, '%.3f' % a, ha='center', va= 'center',size=20)
    plt.xticks(size=25)    
    plt.yticks(range(len(sorted_whole)), sorted_WeightName,fontproperties=myfont)
    plt.grid(linestyle = "--",axis= 'x')
    #ax = plt.gca()
    #ax.spines['top'].set_visible(False)  #去掉上边框
    #ax.spines['right'].set_visible(False) #去掉右边框
    plt.xlim(0,max(sorted_whole)+0.01)
    plt.savefig("Img/综合权重展示图.png") #保存图                    
    plt.cla()
    plt.close()
#ITOPSIS排序计算    
def ITOPSISCal():
    W=Read2('Log/WholeWeight.txt')
    X=np.loadtxt("Log/客户原始信息矩阵X.txt")
    CusName= Read3('Log/CusName.txt')
    #标准化
    for column in range(len(X[0])):
        total=0
        for i in range(len(X)):
            total += (X[i][column]**2)
        for i in range(len(X)):
            if total!=0:
                X[i][column] = X[i][column]/(total**0.5)       
    #构造加权矩阵
    for column in range(len(X[0])):
        for i in range(len(X)):
            X[i][column] = X[i][column]*W[column]
    #确定理想解和负理想解
    Z_Pos=[]
    Z_Neg=[]
    for column in range(len(X[0])):
        Zimax=X[0][column]
        Zimin=X[0][column]
        for i in range(len(X)):
            if Zimax<X[i][column]:
                Zimax=X[i][column]
            if Zimin>X[i][column]:
                Zimin=X[i][column]
        Z_Pos.append(Zimax)
        Z_Neg.append(Zimin)
    #确定每个方案到理想点的距离和到负理想点的距离
    S_Pos=[]
    S_Neg=[]
    for i in range(len(X)):
        total=0
        for column in range(len(X[0])):
             total += ((X[i][column]-Z_Pos[column])**2)
        S_Pos.append(total**0.5)
        total=0
        for column in range(len(X[0])):
             total += ((X[i][column]-Z_Neg[column])**2)        
        S_Neg.append(total**0.5)
    #计算对于理想解的相对接近度
    C=[]
    for i in range(len(X)):
        Ci_val=S_Neg[i]/(S_Neg[i]+S_Pos[i])
        C.append(Ci_val)
    #根据Ci大小进行排序
    Ci=np.array(C)
    Index=np.argsort(Ci)
    sorted_Ci=[]
    sorted_CusName=[]
    for i in range(len(C)):
        b=Index[i]
        sorted_Ci.append(Ci[b])
        sorted_CusName.append(CusName[b])
    return sorted_Ci,sorted_CusName
#画出排序曲线，方便分析客户结构的优劣    
def PlotCurve(sorted_Ci):
    x = [e+1 for e in range(len(sorted_Ci))]
    plt.figure(figsize=(20,15)) #创建绘图对象
    plt.plot(x,sorted_Ci,"g",linewidth=4,marker='o',markersize=12)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）  
    myfont = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=30)
    plt.xlabel(u"电力客户",fontproperties=myfont) #X轴标签  
    plt.ylabel(u"距离正理想解测度",fontproperties=myfont)  #Y轴标签 
    plt.yticks(size=30)
    plt.xticks(size=30)
    plt.grid(linestyle = "--")
    myfont2 = matplotlib.font_manager.FontProperties(fname='Fonts\simsun.ttc',size=40)
    plt.title(u'电力客户评估结果图',fontproperties=myfont2) #图标题 
    plt.savefig("Img/电力客户评估结果图.png") #保存图
    plt.cla()
    plt.close()        
#读取文件，注意此处将读取数据float化       
def Read2(FileAdr):
    FileObject = open(FileAdr)
    ListOfLine = FileObject.readlines()
    List = []
    for i in range(len(ListOfLine)):
        List.append(float(ListOfLine[i].replace('\n','')))
    FileObject.close()
    return List
    
def Read3(FileAdr):
    FileObject = open(FileAdr)
    ListOfLine = FileObject.readlines()
    List = []
    for i in range(len(ListOfLine)):
        List.append(ListOfLine[i].replace('\n',''))
    FileObject.close()
    return List
    
def WeightWrite(FileAdr,List):
    ListOfStr=[]
    for i in List:
        ListOfStr.append(str(i))
        ListOfStr.append('\n')
    file_object = open(FileAdr,'w')
    file_object.writelines(ListOfStr)
    file_object.close()    

