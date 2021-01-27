from MainUI import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import requests
import json
import threading
import time
from datetime import date, timedelta
from urllib3 import PoolManager
import random

class My_window(QtWidgets.QMainWindow, Ui_MainWindow):
    count = 0
    isMmonitoring = False
    monitor = threading.Thread(target=threadMonitor)

    def __init__(self):
        super(My_window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.sendMessageTest)
        self.ui.pushButton_2.clicked.connect(self.connectTest)
        self.ui.pushButton_3.clicked.connect(self.monitorSwitch)
        
    def monitorSwitch(self):
        self.monitor.start()

    def sendMessageTest(self):
        httpstr = 'https://sc.ftqq.com/SCU147608Tafc64fe9bc86bdd6d6d6d55e07819fb65ff7eca9522be.send?text=开始监控' + str(random.randint(0,999))
        http = PoolManager()
        http.request('GET', httpstr)
        self.ui.label.setText("已发送，请查看方糖公众号消息。")
 
    def connectTest(self):
        url = 'http://100000552840.yuyue.n.weimob.com/api3/interactive/advance/microbook/mobile/getAvailableCalendar'
        headers = {'Connection': 'keep-alive','Content-Length': '74','Cache-Control': 'max-age=0','Origin': 'http://100000552840.yuyue.n.weimob.com','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat','Content-Type': 'application/json','Accept': '*/*','Referer': 'http://100000552840.yuyue.n.weimob.com/saas/yuyue/100000552840/12556/calendar?pno=','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4','Cookie': 'saas.express.session=s%3AXq20KEg7TA1E3aHYCxLgjzMn4uRfVyK7.uVJcuk6tP60RwLpiqZF94qZJkKrJVSxMfsA0EAk%2F33Q; rprm_cuid=649987730c9j1qdm8mag','Host': '100000552840.yuyue.n.weimob.com'}
        data = {"sno":"12556","pid":"100000552840","pno":"","calendarDate":1609489988168}
        r = requests.post(url,data=json.dumps(data),headers=headers)
        result = json.loads(r.text)
        if result['errmsg'] == 'ok':
            self.ui.label_2.setText("网站连接成功")
            self.ui.label_2.setStyleSheet("background-color: rgb(0, 255, 0);")
        else:
            self.ui.label_2.setText("网站连接失败，请更新cookies。")
            self.ui.label_2.setStyleSheet("background-color: rgb(255, 0, 0);")

    def threadMonitor(self):
        http = PoolManager()
        while(True):
            self.count+=1
            if self.count >= 3600:
                issend =True
                self.count=0
            tomorrow = (date.today() + timedelta(days= 1)).strftime("%Y-%m-%d")
            url = 'http://100000552840.yuyue.n.weimob.com/api3/interactive/advance/microbook/mobile/getAvailableCalendar'
            headers = {'Connection': 'keep-alive','Content-Length': '74','Cache-Control': 'max-age=0','Origin': 'http://100000552840.yuyue.n.weimob.com','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat','Content-Type': 'application/json','Accept': '*/*','Referer': 'http://100000552840.yuyue.n.weimob.com/saas/yuyue/100000552840/12556/calendar?pno=','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4','Cookie': 'saas.express.session=s%3AXq20KEg7TA1E3aHYCxLgjzMn4uRfVyK7.uVJcuk6tP60RwLpiqZF94qZJkKrJVSxMfsA0EAk%2F33Q; rprm_cuid=649987730c9j1qdm8mag','Host': '100000552840.yuyue.n.weimob.com'}
            data = {"sno":"12556","pid":"100000552840","pno":"","calendarDate":1609489988168}

            r = requests.post(url,data=json.dumps(data),headers=headers)
            result = json.loads(r.text)
            
            data = result['data']
            list = data['items']
            
            for item in list:
                if item['bookDivideTimes'] == tomorrow: 
                    if item['stockNum'] > 0 and issend == False:
                        http.request('GET', 'https://sc.ftqq.com/SCU147608Tafc64fe9bc86bdd6d6d6d55e07819fb65ff7eca9522be.send?text=京丰可以约.')
                        issend = True
                    print("监控日期:  " + tomorrow+ "    当前库存    "+ str(item['stockNum']))
            time.sleep(1)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_app = My_window()
    my_app.show()
    sys.exit(app.exec_())