# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 10:34:23 2017
@author: JRCHAN
Description: 

The codes was developed based on paper:
CAO Qingshan, " Multi-Attribute Decision Making Model for Customer Evaluation and Selection in Electricity Market", Power System Technology
曹清山, 新电改背景下基于多属性决策的电力客户评估和选择研究,电网技术
The paper presents a customer evaluation model based on multi-attribute decision method. 
The model proceeds as follows. Firstly, an evaluation index system for prioritizing power
customers is developed based on customer characteristics and electricity retailer interests. 
Secondly, index weights are obtained with analytic hierarchy process along with improved 
entropy weight method, to reflect opinions of experts and objective quality of different 
types of data and enable a combined utilization of different types of data. Then, to avoid
shortage of technique for order preference by similarity to ideal solution, an improved 
sorting strategy using absolute ideal solution and vertical projection distance is proposed. 
Finally, a case study is conducted for different development stages of electricity market. 
Results show distinct customer prioritizing strategies at different market development stages, 
and verify effectiveness of the proposed evaluation model.

"""

import sys
import login
import MainWindow
from PyQt5 import QtWidgets
                  
if __name__ == "__main__":
    app = 0 # if not the core will die
    app = QtWidgets.QApplication(sys.argv)
    if login.login_first():
        window = MainWindow.MainWindow()
        window.show()
        sys.exit(app.exec_())