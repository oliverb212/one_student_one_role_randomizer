from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from os import path,mkdir

import sys
import json


stu_list:dict #자료 구조: 이름:{역할, 코멘트},{...}
role_list:dict #자료구조: {역할, 역할,...}
release_hash = ""


width,height = 1600,900


#TODO: CVS 파일 임포트 익스포트, UI 개발(ui 디자이너 사용), 테이블 수정 및 추가 기능,릴리즈 해시로 업데이트 확인,테이블 수정시 데이터 리스트 수정 

class check_load_file():
    def __init__(self) -> None:
        global stu_list
        global role_list
        global release_hash

        self.check_file()
        with open("data\\data.json",'r',encoding='utf-8') as f:
            raw = json.loads(f.read())
            stu_list = raw["student"]
            role_list = raw["role"]
            release_hash = raw['release_hash']




    def check_file(self): #data 안에 학생, 역할, 코멘트, 평점 다 있음, 정규화 필요
        if path.isdir('data') == False:
            mkdir('data')

        if path.isfile('data\data.json') == False:
            with open("data\data.json", 'w') as f:
                pass

class stu_directory():
    def make_json_preset(self):
        global stu_list,role_list,release_hash
        return {"student":stu_list, "role":role_list, "release_hash":release_hash}

        
class gui(QWidget):
    stu_num = 0
    student = []
    comment_byte=0
    comment_length=0
    cell_row = 0
    cell_column = 0
    
    def __init__(self):
        super().__init__()
        global stu_list
        global width
        global height
        
        self.student = list(stu_list.keys())

        grid = QGridLayout(self)
        self.setLayout(grid)

        self.tableGroup = QGroupBox("학생 리스트",self)
        self.tableGroup.setMinimumSize(QSize(width/2,height/2.5))

        self.setting_box = QGroupBox("학생 추가",self)
        self.detail_box = QGroupBox("세부사항",self)
        self.comment_box = QGroupBox(self)

        self.comment_box.setMinimumSize(QSize(width/2,height/1.5))
        self.detail_box.setMinimumSize(width-self.comment_box.size().width(),height-self.comment_box.size().height())
        
        #그리드에 그룹박스 위젯 추가    
        grid.addWidget(self.tableGroup,0,0,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.detail_box,0,1,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.setting_box,1,0,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.comment_box,1,1,Qt.AlignmentFlag.AlignLeft)
        
        self.table_init()
        self.comment_init()
        self.detail_init()
        self.setting_init()
        self.update_text()
    
    #--------------slots----------------
    @Slot()
    def stu_select_event(self):
        action:QAction = self.sender()
        self.stu_num = action.data()
        #이닛을 부른다 해도 택스트 업데이트 X
        self.update_text()

    @Slot()
    def randomize_stu(self):
        global stu_list
        import random
        import time
        role = []
        random.seed(time.process_time_ns()*time.time_ns())
        for i in range(len(self.student)): #학생의 리스트 구해오고, 섞기
            role.append(stu_list[self.student[i]]['role'])
        random.shuffle(role)
        for i in range(len(self.student)): #섞은 리스트를 다시 원래 리스트에 붙여넣는 작업
            stu_list[self.student[i]]['role'] = role[i]
        self.update_text()

    
    @Slot()
    def comment_text_changed(self):
        sender = self.sender()
        stu_list[self.student[self.stu_num]]['comment'] = sender.toPlainText()
        self.comment_text_byte_len()
    
    @Slot()
    def rate_text_changed(self):
        sender = self.sender()
        stu_list[self.student[self.stu_num]]['rate'] = sender.toPlainText()
        

    @Slot()
    def cell_select(self,row,column):
        sender = self.sender()
        self.cell_row = row
        self.cell_column = column
    
    @Slot()
    def delete_cell(self):
        self.table.removeRow(self.cell_row)
    
    @Slot()
    def test(self):
        sender:QTableWidget = self.sender()
        print(sender.currentItem().text())
    #------------------------------------
        
    def update_text(self):
        for i in range(len(stu_list)):
            self.table.setItem(i,0,QTableWidgetItem(stu_list[self.student[i]]['role']))
            self.table.setItem(i,1,QTableWidgetItem(self.student[i]))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[self.student[i]]['comment']))
            self.table.setItem(i,3,QTableWidgetItem(stu_list[self.student[i]]['rate']))
        self.comment_line.setText(stu_list[self.student[self.stu_num]]['comment'])
        self.detail_name.setText(self.student[self.stu_num])
        self.detail_role.setText(stu_list[self.student[self.stu_num]]['role'])
        self.detail_role_explain.setText(role_list[stu_list[self.student[self.stu_num]]['role']])
        self.detail_rate.setText(str(stu_list[self.student[self.stu_num]]['rate']))
        self.length_text.setText(str(self.comment_length))
        self.byte_text.setText(str(self.comment_byte))
    
    def comment_text_byte_len(self):
        sender = self.sender()
        self.comment_byte = len(sender.toPlainText().encode('utf-8'))
        self.comment_length = str(len(sender.toPlainText()))
        self.length_text.setText(str(self.comment_length))
        self.byte_text.setText(str(self.comment_byte))
        
    #---------------------inits-----------------------
    def setting_init(self):
        setting_grid = QGridLayout

        setting_layout = QHBoxLayout(self)
        add_stu_button = QPushButton('추가',self)
        del_selected_row_button = QPushButton('선택된 열 삭제',self)
        del_selected_row_button.pressed.connect(self.delete_cell)
        randomize_role_button = QPushButton("역할 랜덤 부여",self)
        randomize_role_button.pressed.connect(self.randomize_stu)

        setting_layout.addWidget(add_stu_button)
        setting_layout.addWidget(del_selected_row_button)
        setting_layout.addWidget(randomize_role_button)
        self.setting_box.setLayout(setting_layout)

    def table_init(self):
        table_layout = QVBoxLayout(self)
        self.table = QTableWidget(len(stu_list),3,self)
        self.table.cellClicked.connect(self.cell_select)
        self.table.itemSelectionChanged.connect(self.test)

        self.tableGroup.setLayout(table_layout)
        table_layout.addWidget(self.table)

    def comment_init(self):
        comment_layer = QVBoxLayout(self)
        self.comment_line = QTextEdit()
        
        self.comment_line.textChanged.connect(self.comment_text_changed)
        self.comment_box.setLayout(comment_layer)
        comment_layer.addWidget(self.comment_line)
    
    def detail_init(self):
        detail_layout = QFormLayout(self)
        
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
        
        #nameline--------

        #role line
        self.detail_role = QLabel(self)
        self.detail_role_explain = QLabel(self)

        #rate line
        self.detail_rate = QTextEdit(self)
        self.detail_rate.setFixedSize(30,30)
        self.detail_rate.textChanged.connect(self.rate_text_changed)
        
        #non-editalbe text line
        self.length_text = QLabel(text=str(self.comment_length))
        self.byte_text = QLabel(text=str(self.comment_byte))

        detail_layout.addRow("이름:",self.detail_name)
        detail_layout.addRow("역할:",self.detail_role)
        detail_layout.addRow("역할 설명:",self.detail_role_explain)
        detail_layout.addRow("평점",self.detail_rate)
        detail_layout.addRow("글자수:",self.length_text)
        detail_layout.addRow("바이트 수:",self.byte_text)
               
        self.detail_box.setLayout(detail_layout)
       





class main():
    def __init__(self) -> None:
        check_load_file()

        app = QApplication([])
        app.setApplicationDisplayName("main")
        self.widget = gui()
        widget = self.widget
        widget.resize(width,height)        
        widget.show()
        app.exec()
        temp:dict
        #save_part
        with open('data\\data.json','w+',encoding='utf8') as f:
            json.dump(stu_directory().make_json_preset(),f,ensure_ascii=False)
        sys.exit(0)
main()