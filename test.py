import json

ls:dict

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

'''with open("data\\stu_data.json",'w',encoding='utf-8') as f:
    stu_directory("이택경","병신이다",3)
    print(ls)
    json.dump(ls,f,indent=4,ensure_ascii=False)
'''
