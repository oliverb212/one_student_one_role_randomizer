from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from os import path,mkdir

import sys
import json
import screeninfo

from PySide6.QtWidgets import QWidget


stu_list:dict #자료 구조: 이름:{역할, 코멘트},{...}
role_list:dict #자료구조: {역할, 역할,...}


height,width = int(screeninfo.get_monitors()[0].height/1.5), int(screeninfo.get_monitors()[0].width/1.5)

class check_load_file():
    def __init__(self) -> None:
        global stu_list
        global role_list

        self.check_file()
        try:
            with open("data\\data.json",'r',encoding='utf-8') as f:
                raw = json.loads(f.read())
                stu_list = raw["student"]
                role_list = raw["role"]
                if (stu_list == {}) or (role_list == {}):
                    raise ValueError()
        except:
            with open("data\\data.json",'w+',encoding='utf-8') as f:
                temp = {"student": {"예시": {"role": "예시", "comment": "예시", "rate": "5"}}, "role": {"예시":"예시입니다."}}
                json.dump(temp,f,ensure_ascii=False)
                
            with open("data\\data.json",'r',encoding='utf-8') as f:
                raw = json.loads(f.read())
                stu_list = raw["student"]
                role_list = raw["role"]

    def check_file(self): #data 안에 학생, 역할, 코멘트, 평점 다 있음, 정규화 필요
        if path.isdir('data') == False:
            mkdir('data')


        if path.isfile('data\data.json') == False:
            with open("data\data.json", 'w') as f:
                pass
class save_data():
    def __init__(self) -> None:
        #save_part
        with open('data\\data.json','w+',encoding='utf8') as f:
            json.dump(stu_directory().make_json_preset(),f,ensure_ascii=False)

class load_csv(): #자료구조: 이름,역할,학생 코멘트,점수, 역할 설명
    def __init__(self,path) -> None:
        import csv
        try:
            data = {"student":{},"role":{}}

            with open(path,"r",encoding="cp949") as f:
                reader = csv.reader(f)

                stu_name = []
                stu_role = []
                stu_rate = []
                stu_comment =[]
                role_comment = []
                data_temp = {}

                for line in reader:
                    stu_name.append(line[0])
                    stu_role.append(line[1])
                    stu_comment.append(line[2])
                    stu_rate.append(line[3])
                    role_comment.append(line[4])

                for i in range(len(stu_name)):
                    data["student"][stu_name[i]] = {"role":stu_role[i],"comment":stu_comment[i],"rate":stu_rate[i]}              
                    data_temp[stu_role[i]] = role_comment[i]

                data["role"] = data_temp
            
            with open(".\\data\\data.json",'w',encoding='utf-8') as f:
                json.dump(data,f,ensure_ascii=False)
            
            check_load_file()
        
        except Exception as e:
            errmsg = QErrorMessage()
            errmsg.showMessage("에러, 파일이 손상되었거나, 코드의 버그입니다. 예외 로그:{}: {}".format(type(e).__name__,e))
            errmsg.exec()

class export_csv():
    def __init__(self,path) -> None:
        import csv
        save_data()
        try:
            raw = None
            data = []
            with open(".\\data\\data.json",'r',encoding='utf-8') as f:
                raw = json.loads(f.read())

            export_stu = raw["student"]
            stu_keys = list(export_stu.keys())
            export_role = raw["role"]

            for i in range(len(stu_keys)):
                data.append([stu_keys[i], export_stu[stu_keys[i]]["role"], export_stu[stu_keys[i]]["comment"], export_stu[stu_keys[i]]["rate"], export_role[export_stu[stu_keys[i]]["role"]] ])

            with open(path,'w+',encoding='utf-8',newline="\n") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print("done!")
        except Exception as e:
            msg = QErrorMessage()
            msg.showMessage("에러, 예외 로그: {}: {}".format(type(e).__name__,e))
            msg.exec()




        

class stu_directory():
    def make_json_preset(self):
        global stu_list,role_list
        return {"student":stu_list, "role":role_list}
    

class role_setting_window(QWidget):
    def __init__(self,main_gui_instance):
        global role_list
        super().__init__()
        self.main_gui = main_gui_instance
        
        self.role = list(role_list.keys())
        self.role_desc = list(role_list.values())

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        
        self.table = QTableWidget(self)
        self.table.setRowCount(len(self.role))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['역할', '설명'])
        self.table.setEditTriggers(QTableWidget().EditTrigger(0))
        
        self.update()
        
        # 디자인
        pannel_grid = QGridLayout()
        self.pannel_role = QLineEdit()
        self.pannel_role_desc = QLineEdit()
        pannel_role_add = QPushButton()
        pannel_role_del = QPushButton()

        pannel_role_add.setText("추가")
        pannel_role_del.setText("선택한 역할 삭제")
        self.pannel_role.setPlaceholderText("여기에 역할 입력 (중복되는 역할 이름 불가)")
        self.pannel_role_desc.setPlaceholderText("여기에 역할 설명 입력")

        pannel_grid.addWidget(self.pannel_role,0,0)
        pannel_grid.addWidget(pannel_role_add,0,1)
        pannel_grid.addWidget(self.pannel_role_desc,1,0)
        pannel_grid.addWidget(pannel_role_del,1,1)

        # 디자인 끝

        pannel_role_add.clicked.connect(self.add_button_func)
        pannel_role_del.clicked.connect(self.del_button_func)
        
        main_layout.addWidget(self.table)
        main_layout.addLayout(pannel_grid)

    def update(self):
        self.table.setRowCount(len(self.role)) #우라질 그놈의 함수, 이거 추가하니깐 또 멀정하게 작동함
        for i in range(len(self.role)):
            self.table.setItem(i,0,QTableWidgetItem(self.role[i]))
            self.table.setItem(i,1,QTableWidgetItem(self.role_desc[i]))
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        main_update = QAction(self)
        main_update.triggered.connect(main_gui().update_all)



    @Slot()
    def add_button_func(self):
        text_role = self.pannel_role.text().strip()
        text_desc = self.pannel_role_desc.text().strip()
        if text_role not in role_list:
            self.role.append(text_role)
            self.role_desc.append(text_desc)
            role_list[text_role] = text_desc
            self.main_gui.update_preset_role() #이부분은 GPT 생성, 객체 인자 불러와서 가능했다는데 이부분은 나중에 물어보기
            self.update()
        else:
            msg = QErrorMessage()
            msg.showMessage("역할 이름 중복입니다, 다시 지어주세요.")
            msg.exec()

    @Slot()
    def del_button_func(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            selected_row = self.table.row(selected_items[0])
            role_to_delete = self.role[selected_row]
            del role_list[role_to_delete]
            del self.role[selected_row]
            del self.role_desc[selected_row]
            self.update()
        
class main_gui(QWidget):
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

        self.maker_window = None
        self.role_window = None

        menubar = QMenuBar(self)
        menubar_file =QMenu("파일",self)
        menubar_info =QMenu("정보",self)
        
        file_load = QAction("CSV로 로드하기",self)
        file_export =QAction("CSV로 내보내기",self)
        info_maker = QAction("깃허브로 이동",self)
        
        menubar_add_role =QAction("역할 추가",self)
        menubar_file.addAction(file_load)
        menubar_file.addAction(file_export)
        menubar_info.addAction(info_maker)

        info_maker.triggered.connect(self.call_maker_window)
        menubar_add_role.triggered.connect(self.call_role_window)
        file_load.triggered.connect(self.call_load_window)
        file_export.triggered.connect(self.call_export_window)
        
        menubar.addMenu(menubar_file)
        menubar.addAction(menubar_add_role)
        menubar.addMenu(menubar_info)



        self.student = list(stu_list.keys())
    
        grid = QGridLayout(self)
        grid.setRowStretch(0,height)
        grid.setMenuBar(menubar)
        self.setLayout(grid)

        self.table_group = QGroupBox("학생 리스트",self)
        self.setting_box = QGroupBox("학생 추가",self)
        self.detail_box = QGroupBox("세부사항",self)
        self.comment_box = QGroupBox("코멘트(쓰이는 즉시 자동저장)",self)

        self.setting_box.setMinimumSize(width/2,height/5)
        self.detail_box.setMinimumSize(width/2,height/5)

        self.table_group.setMinimumSize(width/2,height-self.setting_box.size().height())
        self.comment_box.setMinimumSize(width/2,height-self.setting_box.size().height())

        self.table_group.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.comment_box.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        
        #그리드에 그룹박스 위젯 추가    
        grid.addWidget(self.table_group,0,0)
        grid.addWidget(self.detail_box,1,1)
        grid.addWidget(self.setting_box,1,0)
        grid.addWidget(self.comment_box,0,1)
        
        self.table_init()
        self.comment_init()
        self.detail_init()
        self.setting_init()
        self.update_all()
        
    
    #--------------slots----------------
    @Slot()
    def call_load_window(self):
        dbox = QFileDialog(self)
        fpath = dbox.getOpenFileName(self,filter="*.csv")[0]
        if fpath != "":
            load_csv(fpath)
            self.update_all()
    
    @Slot()
    def call_export_window(self):
        dbox = QFileDialog(self)
        fpath = dbox.getSaveFileName(self,filter="*.csv")[0]
        if fpath != "":
            export_csv(fpath)
    
    @Slot()
    def call_role_window(self):
        if self.role_window == None:
            self.role_window = role_setting_window(self)
        self.role_window.resize(640,640)
        self.role_window.show()

    def update_preset_role(self):
        self.preset_role.clear()
        for role in role_list.keys():
            self.preset_role.addItem(role)
        

    @Slot()
    def call_maker_window(self):
        url = QUrl("https://github.com/oliverb212/one_student_one_role_randomizer")
        QDesktopServices().openUrl(url)
        
    @Slot()
    def stu_select_event(self):
        action:QAction = self.sender()
        self.stu_num = action.data()

        self.update_all()

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
        self.update_all()
        
    
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
        self.stu_num = row
        self.update_all()
    
    @Slot()
    def delete_cell(self):
        item_name = self.table.item(self.cell_row,1).text()
        del stu_list[item_name]
        if self.stu_num >= 0: self.stu_num -= 1
        else: pass
    
        self.table.removeRow(self.cell_row)
        if self.table.rowCount() >= self.cell_row:
            self.table.setRangeSelected(QTableWidgetSelectionRange(self.cell_row,0,self.cell_row,2),True)
        self.update_all()
    

    @Slot()
    def add_item(self):
        input_stu = self.preset_name.text()
        input_role = self.preset_role.currentText()
        input_rate = self.preset_rate.text()

        if input_stu not in self.student:
        
            preset = {'role':'','comment':'','rate':''}
            preset['role'] = input_role
            preset['comment'] = ""
            preset['rate'] = input_rate

            stu_list[input_stu] = preset

            self.preset_name.setText("")
            self.preset_rate.setText("")

            self.update_all()
        else:
            msgbox = QErrorMessage()
            msgbox.showMessage("이름이 중복됩니다, 다시 지어주세요.")
            msgbox.exec()

    @Slot()
    def update_table(self):
        stu_num = len(self.student)
        self.table.setRowCount(stu_num) #이 부분 때문에 테이블 업데이트가 안된거였음;;; 고마워요 GPT4, 고마워요 스택 오버플로우
        for i in range(stu_num):
            self.table.setItem(i,0,QTableWidgetItem(stu_list[self.student[i]]['role']))
            self.table.setItem(i,1,QTableWidgetItem(self.student[i]))
            self.table.setItem(i,2,QTableWidgetItem(stu_list[self.student[i]]['comment']))
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        
        
    @Slot()
    def update_all(self):
        self.student = list(stu_list.keys())

        self.update_table()
        self.update_detail()
    
    #------------------------------------

    def update_detail(self):
        self.comment_line.setText(stu_list[self.student[self.stu_num]]['comment'])
        self.detail_name.setText(self.student[self.stu_num])
        self.detail_role.setText(stu_list[self.student[self.stu_num]]['role'])
        try:
            self.detail_role_explain.setText(role_list[stu_list[self.student[self.stu_num]]['role']])
        except:
            role_list[stu_list[self.student[self.stu_num]]['role']] = "NULL"
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
        global role_list

        setting_grid = QGridLayout(self)

        setting_button_layout = QHBoxLayout(self)
        add_stu_button = QPushButton('추가',self)
        add_stu_button.pressed.connect(self.add_item)

        del_selected_row_button = QPushButton('선택된 열 삭제',self)
        del_selected_row_button.pressed.connect(self.delete_cell)
        
        randomize_role_button = QPushButton("역할 랜덤 부여",self)
        randomize_role_button.pressed.connect(self.randomize_stu)

        setting_preset_layout = QHBoxLayout(self)
        
        self.preset_role = QComboBox(self)
        self.preset_role.setBaseSize(500,100)
        role = list(role_list.keys())
        
        for i in range(len(role)):
            self.preset_role.addItem(role[i])
        
        self.preset_name = QLineEdit(self)
        self.preset_name.setPlaceholderText("여기에 이름 입력")
        
        self.preset_rate = QLineEdit(self)
        self.preset_rate.setMaximumWidth(100)
        self.preset_rate.setPlaceholderText("여기에 점수 입력")

        setting_preset_layout.addWidget(self.preset_role)
        setting_preset_layout.addWidget(self.preset_name)
        setting_preset_layout.addWidget(self.preset_rate)
        
        setting_button_layout.addWidget(add_stu_button)
        setting_button_layout.addWidget(del_selected_row_button)
        setting_button_layout.addWidget(randomize_role_button)
        
        setting_grid.addLayout(setting_preset_layout,0,0)
        setting_grid.addLayout(setting_button_layout,1,0)
        
        self.setting_box.setLayout(setting_grid)
        

    def table_init(self):
        table_layout = QVBoxLayout(self)
        self.table = QTableWidget(len(stu_list),3,self)
        self.table.setEditTriggers(QTableWidget().EditTrigger(0))
        self.table.setHorizontalHeaderLabels(["역할","이름","코멘트"])

        self.table.cellClicked.connect(self.cell_select)

        self.table_group.setLayout(table_layout)
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
        self.detail_name = QLabel(self)
        self.detail_name.setMaximumWidth(90)
        
        
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
        app.setApplicationDisplayName("1인1역 기록장")
        self.widget = main_gui()
        widget = self.widget
        widget.resize(width,height)
        widget.show()
        app.exec()
        save_data()
        sys.exit(0)
main()