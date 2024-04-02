from PySide6.QtWidgets import *
from PySide6.QtCore import *
from os import path,mkdir

import sys
import json

stu_list:dict #자료 구조: {이름, 역할, 코멘트},{...}
role_list:dict #자료구조: {역할, 역할,...}

width,height = 1600,900


#TODO: CVS 파일 임포트, UI 개발, 역할 수정, 추가 칸

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
    def make_preset(self,stu:str,role:str,comment:str,rate:float):
        global stu_list
        stu_list[stu] = {"role":role, "comment":comment, "rate":rate}
    
    def shuffel(self) -> None:
        global stu_list
        import time
        import random
        random.seed((time.process_time_ns()*136%255+7)<<2)
        students = gui().student
        random.shuffle(students)
        for i in range(len(students)):
            stu_list[gui().student[i]]['role'] = stu_list[students]['role']
        
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
        self.setLayout(self.grid)

        self.tableGroup = QGroupBox("학생 리스트",self)
        self.tableGroup.setMinimumSize(QSize(width/2,height/2.5))

        self.setting_box = QGroupBox("설정",self)
        self.detail_box = QGroupBox("세부사항",self)
        self.comment_box = QGroupBox(self)

        self.comment_box.setMinimumSize(QSize(width/2,height/1.5))
        self.detail_box.setMinimumSize(width-self.comment_box.size().width(),height-self.comment_box.size().height())
        
        #그리드에 그룹박스 위젯 추가    
        self.grid.addWidget(self.tableGroup,0,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.detail_box,0,1,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.setting_box,1,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.comment_box,1,1,Qt.AlignmentFlag.AlignLeft)
        
        self.table_init()
        self.comment_init()
        self.detail_init()
        self.setting_init()
    
    def setting_init(self):
        self.setting_layout = QHBoxLayout(self)
        self.setting_button = QPushButton('test',self)

        self.setting_box.setLayout(self.setting_layout)
        self.setting_layout.addWidget(self.setting_button)

    def table_init(self):
        self.table_layout = QVBoxLayout(self)
        self.table = QTableWidget(len(stu_list),3,self)

        for i in range(len(stu_list)):
            self.table.setItem(i,0,QTableWidgetItem(stu_list[self.student[i]]['role']))
            self.table.setItem(i,1,QTableWidgetItem(self.student[i]))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[self.student[i]]['comment']))
            self.table.setItem(i,3,QTableWidgetItem(stu_list[self.student[i]]['rate']))
        
        self.tableGroup.setLayout(self.table_layout)
        self.table_layout.addWidget(self.table)

    def comment_init(self): #TODO: 글자수, 바이트수 표시
        self.comment_layer = QVBoxLayout(self)
        self.comment_line = QTextEdit()
        self.comment_line.setPlainText(stu_list[self.student[self.stu_num]]['comment'])

        self.comment_box.setLayout(self.comment_layer)
        self.comment_layer.addWidget(self.comment_line)
    
    def detail_init(self):#TODO: 폴 레이아웃 고치기!
        self.detail_layout = QFormLayout(self)
        self.detail_layout.addRow("이름")
        
        self.name_text = QLabel("이름",self)
        self.role_text = QLabel("역할",self)

        self.detail_name = QTextEdit(self)
        self.detail_name.setText(self.student[self.stu_num])
        self.detail_role_exp = QTextEdit(self)
        self.detail_role_exp.setText(stu_list[self.student[self.stu_num]]['role'])

        self.detail_layout.addWidget(self.detail_name,0,0)
        self.detail_layout.addWidget(self.detail_name,1,0)

        self.detail_layout.addWidget(self.detail_name,0,1)
        self.detail_layout.addWidget(self.detail_role_exp,1,1)
        self.detail_box.setLayout(self.detail_layout)
       





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