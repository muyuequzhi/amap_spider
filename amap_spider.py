# -*- coding: utf-8 -*-

"""
高德地图爬虫小程序
"""

import os
import sys
import requests
from openpyxl import Workbook
from PyQt5.QtWidgets import QLineEdit, QApplication, QDialog, QLabel, QMessageBox, QPushButton, QFileDialog

mykey = "" #需要申请搞得地图的api
start_url = "https://restapi.amap.com/v3/place/text?&citylimit=true&&output=json&offset=20&page={}"
# 使用工作簿
wb = Workbook()
ws = wb.active
ws.append(['name', 'address', 'tel'])
urls = [start_url.format(p) for p in range(1,100)]


class Line(QDialog):
    '''
    掩码输入
    '''
    def __init__(self):
        '''
        一些初始设置
        '''
        super().__init__()
        self.Ui()

    def amap_spider(self,city,keyword):
        '''
        高德地图爬虫主程序
        '''
        kv = {'key': mykey, 'keywords': keyword,'city':city}
        for url in urls:
            r = requests.get(url, params=kv)
            data = r.json()
            pois = data.get('pois')
            ''' 在返回的数据中找到pois，pois列表中含有目标数据'''
            for num in range(20):
                poi = pois[num]
                name = poi.get('name')
                address = poi.get('address')
                tel = poi.get('tel')
                target = [name, address, tel]
                ''' 去除不完整的数据（可能没有电话或地址） '''
                if [] == target[2]:
                    target[2] = 0
                if [] == target[1]:
                    continue
                else:
                    ws.append(target)
                #print(target)

    def Ui(self):
        '''
        界面初始设置
        '''
        self.resize(900, 500)
        self.setWindowTitle('高德地图爬虫')
        self.line = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line3 = QLineEdit(self)
        self.line4 = QLineEdit(self)

        lb = QLabel('城市', self)
        lb2 = QLabel('关键字', self)
        lb3 = QLabel('保存路径', self)
        lb4 = QLabel('进度', self)
        
        lb.move(30, 50)
        lb2.move(30, 150)
        lb3.move(30, 250)
        lb4.move(30, 350)

        self.line.move(240, 50)
        self.line2.move(240, 150)
        self.line3.move(240, 250)
        self.line4.move(240, 350)

        self.line.setText('')# 空白，等待输入城市
        self.line2.setText('')# 空白，等待输入关键字
        self.line3.setText('')# 空白，等待选择文件夹
        self.line4.setText('0')# 进度显示

        self.bt2 = QPushButton('选择文件夹', self)
        self.bt2.move(460, 250)
        self.bt2.clicked.connect(self.get_dir)

        self.bt1 = QPushButton('开始执行', self)
        self.bt1.move(460, 350)
        self.bt1.clicked.connect(self.Action)

        self.show()

    def get_dir(self):
        '''
        选择文件夹
        '''
        home = os.getcwd()
        self.filename = QFileDialog.getExistingDirectory(self, 'Open file', home)
        self.line3.setText(self.filename)# 保存路径

    def Action(self):
        '''
        开始执行时调用主程序
        '''
        self.city = self.line.text()
        self.keyword = self.line2.text()
        file = self.filename + "/" + self.city + self.keyword + ".xlsx"
        if self.bt1.isEnabled():
            self.line4.setText('执行中,请稍等几分钟')
            QMessageBox.information(self, '提示信息', '正在执行')
            try:
                self.amap_spider(self.city,self.keyword)
                wb.save(file)
            except IndexError:
                wb.save(file)
            #wb.save(file)
            QMessageBox.information(self, '提示信息', "文件已保存在: {}".format(file))
            self.line4.setText('已完成')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    line = Line()
    sys.exit(app.exec_())