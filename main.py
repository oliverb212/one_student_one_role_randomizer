from PySide6.QtWidgets import *
from PySide6.QtCore import *
from os import path,mkdir

import sys
import json

stu_list:dict
role_list:dict

width,height = 1920,1080


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
        self.student = list(stu_list.keys())

        self.grid = QGridLayout(self)

        self.tableGroup = QGroupBox("학생 리스트",self)
        self.box_2 = QGroupBox("box",self)
        self.box_3 = QGroupBox("box",self)
        self.comment_box = QGroupBox(self)

        self.tab_init()

        #코멘트 작성 라인###########
        self.comment_layer = QVBoxLayout(self)
        self.comment_line = QTextEdit(self)
        self.comment_line.setText(stu_list[self.student[self.stu_num]]['comment'])

        self.comment_box.setLayout(self.comment_layer)
        self.comment_layer.addWidget(self.comment_line)
        ##########################
       
        #그리드에 그룹박스 위젯 추가    
        self.grid.addWidget(self.tableGroup,0,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_2,0,1,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_3,1,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.comment_box,1,1,Qt.AlignmentFlag.AlignLeft)
    
    def tab_init(self):
         #######학생 리스트 구성#############
        self.tableLayout = QVBoxLayout(self)
        self.table = QTableWidget(len(stu_list),3,self)
        #self.table.setFixedSize(width,height)

        for i in range(len(stu_list)):
            self.table.setItem(i,0,QTableWidgetItem(self.student[i]))
            self.table.setItem(i,1,QTableWidgetItem(stu_list[self.student[i]]['role']))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[self.student[i]]['comment']))
            self.table.setItem(i,3,QTableWidgetItem(stu_list[self.student[i]]['rate']))
        
        self.tableGroup.setLayout(self.tableLayout)
        self.tableLayout.addWidget(self.table)
        ###################################
       





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