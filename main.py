import sys
import json
import os
from sys import argv
from tabulate import tabulate

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + "/data.json"

def readTasks():
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

def writeTasks(info):
    with open(file_path, 'w') as outfile:
        json.dump(info, outfile,indent=4,ensure_ascii=False)

def newTask(info,section,task,date):
    next_id = len(info[section]) + 1
    info[section].append({
        "id":next_id,
        "task":task,
        "date":date
    })
    writeTasks(info)

def prettyprint(data):
    
    headers = ["Secção","Tarefa","Data"]
    table = []
    for x in data:
        s = ""
        datas = ""
        for y in data[x]:
            s += str(y["id"]) + " - " + y["task"] + "\n"
            datas += y["date"] + "\n"
        table.append([x,s,datas])

    print(tabulate(table, headers, tablefmt='fancy_grid'))


def main():
    if((len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5) and sys.argv[1] == "add"):

        info = readTasks()

        # Cria a seccção, caso não exista
        if(len(sys.argv) == 3):
            if("GERAL" not in info):
                info["GERAL"] = []
        else:
            if(argv[2] not in info and "/" not in sys.argv[3]):
                info[sys.argv[2]] = []

        # Adiciona nova tarefa ao ficheiro
        if(len(sys.argv) == 3):
            newTask(info,"GERAL",sys.argv[2],"-----")

        elif(len(sys.argv) == 4):
            # Caso tenha data sem seção
            if("/" in sys.argv[3]):
                newTask(info,"GERAL",sys.argv[2],sys.argv[3])
            # Caso tenha secção sem data
            else:
                newTask(info,sys.argv[2],sys.argv[3],"-----")

        elif(len(sys.argv) == 5):
            newTask(info,sys.argv[2],sys.argv[3],sys.argv[4])

        prettyprint(readTasks())

    elif(len(sys.argv) == 1):
        prettyprint(readTasks())
    elif(len(sys.argv) == 3 and sys.argv[1] == "rs"):
        info = readTasks()
        seccao = sys.argv[2]
        if(seccao not in info):
            print("Secção não existe...")
            sys.exit(0)
        del info[seccao]
        writeTasks(info)
        prettyprint(info)
    elif(len(sys.argv) == 4 and sys.argv[1] == "rm"):
        info = readTasks()
        seccao = sys.argv[2]
        if(seccao not in info):
            print("Secção não existe...")
            sys.exit(0)
        if(int(sys.argv[3]) > len(info[seccao]) or int(sys.argv[3]) <= 0):
            print("Id inválido...")
            sys.exit(0)
        del info[seccao][int(sys.argv[3])-1]
        writeTasks(info)
        prettyprint(info)
    elif(len(sys.argv) == 2 and sys.argv[1] == "datas"):
        info = readTasks()
        info_with_dates = {}

        for sec in info:
            for i in info[sec]:
                if(i["date"] != "-----"):
                    if(sec not in info_with_dates):
                        info_with_dates[sec] = []    
                    info_with_dates[sec].append(i)
        prettyprint(info_with_dates)

    elif(len(sys.argv) == 2 and sys.argv[1] == "help"):
        print("╒═══════════════════════════════════════════════════════════════════════════════════════╕")
        print("│ $ todo                                         -> Mostra os to-dos de cada secção     │")
        print("│ $ todo add \"tarefa\" [\"data\"]                   -> Novo to-do na secção \"GERAL\"        │")
        print("│ $ todo add \"nome_secção\" \"tarefa\" [\"data\"]     -> Novo to-do numa secção à escolha    │")
        print("│ $ todo rm \"nome_secção\" \"id-tarefa\"            -> Remove um to-do de uma secção       │")
        print("│ $ todo rs \"nome_secção\"                        -> Remove uma secção                   │")
        print("│ $ todo datas                                   -> Mostra os to-dos com data por ordem │")
        print("╘═══════════════════════════════════════════════════════════════════════════════════════╛")
    else:
        print(sys.argv)
        print("Argumento inválido!")

if __name__ == '__main__':
    main()