# -*- coding: utf-8 -*-
"""
Created on Sun Jan 7 15:52:13 2018
@author: JRCHAN
Description: 读写本地存储的计算参数和上一次计算结果，数据存储在txt文件中
"""

def Read(FileAdr):
    FileObject = open(FileAdr)
    ListOfLine = FileObject.readlines()
    List = []
    for i in range(len(ListOfLine)):
        List.append(ListOfLine[i].replace('\n',''))
    FileObject.close()
    return List

def Write(FileAdr,ListOfStr):
    file_object = open(FileAdr,'w')
    file_object.writelines(ListOfStr)
    file_object.close()