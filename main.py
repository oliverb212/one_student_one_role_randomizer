from PySide6.QtWidgets import *
from PySide6.QtCore import *
from os import path,mkdir

import sys
import json

stu_list:dict
role_list:dict


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
    def __init__(self):
        super().__init__()
        global stu_list
        global role_list
        
        self.grid = QGridLayout(self)

        self.tableGroup = QGroupBox("학생 리스트",self)
        self.box_2 = QGroupBox("box",self)
        self.box_3 = QGroupBox("box",self)
        self.box_4 = QGroupBox("box",self)
        
        #######학생 리스트 구성#############
        self.tableLayout = QVBoxLayout(self)   
        self.tableGroup.setLayout(self.tableLayout)

        self.table = QTableWidget(len(stu_list),3,self)
        
        student = tuple(stu_list.keys())        
        for i in range(len(stu_list)):
            self.table.setItem(i,0,QTableWidgetItem(student[i]))
            self.table.setItem(i,1,QTableWidgetItem(stu_list[student[i]]['role']))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[student[i]]['comment']))
            self.table.setItem(i,3,QTableWidgetItem(stu_list[student[i]]['rate']))
        del student
        
        self.tableLayout.addWidget(self.table)
        ###################################

        #그리드에 그룹박스 위젯 추가
        self.grid.addWidget(self.tableGroup,0,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_2,0,1,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_3,1,0,Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.box_4,1,1,Qt.AlignmentFlag.AlignLeft)





class main():
    def __init__(self) -> None:
        check_load_file()

        app = QApplication([])
        app.setApplicationDisplayName("main")
        widget = gui()
        widget.resize(1920,1080)
        widget.show()
        
        sys.exit(app.exec())
main()