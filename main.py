from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
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
    comment_byte=0
    comment_length=0
    
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

    @Slot()
    def stu_select_event(self):
        action:QAction = self.sender()
        self.stu_num = action.data()
        self.refrash()

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

    def comment_init(self):
        self.comment_layer = QVBoxLayout(self)
        self.comment_line = QTextEdit()
        self.comment_line.setText(stu_list[self.student[self.stu_num]]['comment'])
        self.comment_box.setLayout(self.comment_layer)
        self.comment_layer.addWidget(self.comment_line)
    
    def detail_init(self):
        self.detail_layout = QFormLayout(self)
        
        #name line
        self.detail_name = QPushButton(self)
        self.detail_name.setMaximumWidth(90)
        
        menu = QMenu(self)
        for i in range(len(self.student)):
            act = QAction(self.student[i],self)
            act.setData(i)
            act.triggered.connect(self.stu_select_event)
            menu.addAction(act)

        self.detail_name.setMenu(menu)
        self.detail_name.setText(self.student[self.stu_num])
        
        d_button_menu = self.detail_name.menu()
        button_list = d_button_menu.actions()
        
        #nameline

        #role line
        self.detail_role = QLabel(self)
        self.detail_role.setText(stu_list[self.student[self.stu_num]]['role'])
        
        self.detail_role_explain = QLabel(self)
        self.detail_role_explain.setText(role_list[stu_list[self.student[self.stu_num]]['role']])
        #roleline

        self.length_text = QLabel(text=str(self.comment_length))
        self.byte_text = QLabel(text=str(self.comment_byte))

        self.detail_layout.addRow("이름:",self.detail_name)
        self.detail_layout.addRow("역할:",self.detail_role)
        self.detail_layout.addRow("역할 설명:",self.detail_role_explain)
        self.detail_layout.addRow("글자수:",self.length_text)
        self.detail_layout.addRow("바이트 수:",self.byte_text)
       
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