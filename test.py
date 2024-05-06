import json
from PySide6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
ls:dict

import time
import random
import datetime

if __name__ == "__main__":
    class Ui_Form(object):
        def setupUi(self, Form):
            Form.setObjectName("Form")
            Form.resize(400, 300)
            self.label = QLabel(Form)
            self.label.setGeometry(QRect(165, 125, 61, 16))
            self.label.setObjectName("label")

            self.retranslateUi(Form)
            QMetaObject.connectSlotsByName(Form)

    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    def update_label():
        current_time = str(datetime.datetime.now().time())
        ui.label.setText(current_time)

    timer = QTimer()
    timer.timeout.connect(update_label)
    timer.start(10000)  # every 10,000 milliseconds

    sys.exit(app.exec_())

'''
names = ['name1', 'name2', 'name3', 'name4', 'name5']
random.seed(time.process_time_ns()<<2)
random.shuffle(names)
print(names)

class stu_directory():   
    def __init__(self,stu:str,comment:str,rate:int):
        global ls
        ls['student'][0][stu] = {"comment":comment,"rate":rate}


with open("data\\data.json",'r+',encoding='utf-8') as f:

    ls = json.loads(f.read())
    
ls=ls['student'][0]
print(ls)
ls_key = list(ls.keys())
print(ls_key[0])

with open("data\\stu_data.json",'w',encoding='utf-8') as f:
    stu_directory("대충 뭐시기","어쩌구저쩌구",3)
    print(ls)
    json.dump(ls,f,indent=4,ensure_ascii=False)
'''
