# -*- coding: utf-8 -*-
"""
Created Mon Dec 25 12:24:13 2017

@author: JRCHAN
Discription: Define the login windows and preset the accounts/passwords
"""

from PyQt5 import QtWidgets, uic

class LoginDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(u'登录')
        self.resize(300,150)

        self.leName =QtWidgets.QLineEdit(self)
        self.leName.setPlaceholderText(u'用户名')

        self.lePassword =QtWidgets.QLineEdit(self)
        self.lePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lePassword.setPlaceholderText(u'密码')

        self.pbLogin =QtWidgets.QPushButton(u'登录',self)
        self.pbCancel =QtWidgets.QPushButton(u'取消',self)

        self.pbLogin.clicked.connect(self.login)
        self.pbCancel.clicked.connect(self.reject)
        
        # 设置窗口布局方式
        layout =QtWidgets.QVBoxLayout()
        layout.addWidget(self.leName)
        layout.addWidget(self.lePassword)
            
        spacerItem =QtWidgets.QSpacerItem(20,48,QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacerItem)
        
        # 设置按钮布局方式
        buttonLayout =QtWidgets.QHBoxLayout() 
        spancerItem2 =QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)
        buttonLayout.addItem(spancerItem2)
        buttonLayout.addWidget(self.pbLogin)
        buttonLayout.addWidget(self.pbCancel)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
    
    # Table for username and code. Passwords presetted.
    def login(self):      
        Table = [['JIE','RUN'],
                 ['DING','YI'],
                 ['QING','SHAN'],
                 ['6','6']]

        flag = False
        for i in range(0,len(Table)):
            if self.leName.text()== Table[i][0]:
                if self.lePassword.text()== Table[i][1]:
                    self.accept()
                    flag = True
        if not flag:
            QtWidgets.QMessageBox.critical(self, u'错误', u'账户名或密码不对，区分大小写')
def login_first():
    dialog = LoginDialog()
    if dialog.exec_():
        return True
    else:
        return False
