import json
from PySide6.QtWidgets import *
from PyQt6.QtCore import *
import sys
ls:dict

import time
import random

names = ['name1', 'name2', 'name3', 'name4', 'name5']
random.seed(time.process_time_ns()<<2)
random.shuffle(names)
print(names)
'''
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
    stu_directory("이택경","병신이다",3)
    print(ls)
    json.dump(ls,f,indent=4,ensure_ascii=False)
'''
