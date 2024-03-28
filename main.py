from PySide6.QtWidgets import *
from PySide6.QtCore import *
from os import path,mkdir

import sys
import json

stu_list:dict
role_list:dict

width,height = 1600,900


#TODO: CVS 파일 임포트, UI 개발

class check_load_file():
    def __init__(self) -> None:
        global stu_list
        global role_list

        self.check_file()
        with open("data\\data.json",'r',encoding='utf-8') as f:
            raw = json.loads(f.read())
            stu_list = raw["student"][0]
            role_list = raw["role"][0]




    def check_file(self): #data 안에 학생, 역할, 코멘트, 평점 다 있음, 정규화 필요
        if path.isdir('data') == False:
            mkdir('data')

        if path.isfile('data\data.json') == False:
            with open("data\data.json", 'w') as f:
                pass

class stu_directory():
    def __init__(self,stu:str,role:str,comment:str,rate:float):
        global stu_list
        stu_list[stu] = {"role":role, "comment":comment, "rate":rate}

class gui(QWidget):
    stu_num = 0
    student = []
    
    def __init__(self):
        super().__init__()
        global stu_list
        global width
        global height
        self.student = list(stu_list.keys())

        self.grid = QGridLayout(self)

        self.tableGroup = QGroupBox("학생 리스트",self)
        self.tableGroup.setMinimumSize(QSize(width/2,height/2.5))

        self.setting_box = QGroupBox("설정",self)
        self.box_2 = QGroupBox("box",self)
        self.comment_box = QGroupBox(self)

        self.comment_box.setMinimumSize(QSize(width/2,height/1.5))
        self.box_2.setMinimumSize(width-self.comment_box.size().width(),height-self.comment_box.size().height())
        
        self.table_init()
        self.comment_init()
        
       
        #그리드에 그룹박스 위젯 추가    
        self.grid.addWidget(self.tableGroup,0,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_2,0,1,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.setting_box,1,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.comment_box,1,1,Qt.AlignmentFlag.AlignLeft)
    
    def setting_init(self):
        self.setting_layout = QLayout(self)
        self.button_1 = QPushButton('test',self)
        
        self.comment_box.setLayout(self.setting_layout)
        self.setting_layout.addItem(self.button_1)

    def table_init(self):
        self.tableLayout = QVBoxLayout(self)
        self.table = QTableWidget(len(stu_list),3,self)

        for i in range(len(stu_list)):
            self.table.setItem(i,0,QTableWidgetItem(self.student[i]))
            self.table.setItem(i,1,QTableWidgetItem(stu_list[self.student[i]]['role']))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[self.student[i]]['comment']))
            self.table.setItem(i,3,QTableWidgetItem(stu_list[self.student[i]]['rate']))
        
        self.tableGroup.setLayout(self.tableLayout)
        self.tableLayout.addWidget(self.table)

    def comment_init(self): #TODO: 글자수, 바이트수 표시
        self.comment_layer = QVBoxLayout(self)
        self.comment_line = QTextEdit(self)
        self.comment_line.setText(stu_list[self.student[self.stu_num]]['comment'])

        self.comment_box.setLayout(self.comment_layer)
        self.comment_layer.addWidget(self.comment_line)
       





class main():
    def __init__(self) -> None:
        check_load_file()

        app = QApplication([])
        app.setApplicationDisplayName("main")
        widget = gui()
        widget.resize(width,height)        
        widget.show()
        
        sys.exit(app.exec())
main()