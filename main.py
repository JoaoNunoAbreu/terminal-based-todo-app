import sys
import os 
from os import path
from sys import argv
from tabulate import tabulate

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + "/data.txt"

if(path.exists(file_path) == False):
    file = open(file_path,"w")

def line_remover(nicknames_to_delete):
    with open(file_path, "r") as f:
        lines = f.readlines()
    with open(file_path, "w") as f:
        for line in lines:
            if line.strip("\n") not in nicknames_to_delete:
                f.write(line)

def prettyprint(printable):
    file = open(file_path,"r")
    lines = file.readlines() 
    info = {}
    for l in lines:
        data = l.split()
        
        if(data[0] == "*"):
            info[data[1]] = []
        else:
            info[data[0]].append((data[1],data[2]))

    if(printable):
        
        headers = ["Secção","Tarefa","Data"]
        table = []
        for x in info:
            s = "\n"
            datas = "\n"
            num = 1
            for y in info[x]:
                s += str(num) + " - " + y[0] + "\n"
                datas += y[1] + "\n"
                num += 1
            table.append([x,s.replace("~"," "),datas])

        print(tabulate(table, headers, tablefmt='fancy_grid'))

    file.close()
    return info

if((len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5) and sys.argv[1] == "add"):

    info = prettyprint(False)
    file = open(file_path,"a")

    if(len(sys.argv) == 3):
        if("GERAl" not in info):
            file.write("* GERAl\n")
    else:
        if(argv[2] not in info and "/" not in sys.argv[3]):
            file.write("* "+sys.argv[2]+"\n")
            

    if(len(sys.argv) == 3):
        file.write("GERAl" + " " + sys.argv[2].replace(" ","~") + " " + "-----" + "\n")
    elif(len(sys.argv) == 4):
        # Caso tenha data sem seção
        if("/" in sys.argv[3]):
            file.write("GERAl" + " " + sys.argv[2].replace(" ","~") + " " + sys.argv[3] + "\n")
        # Caso tenha secção sem data
        else:
            file.write(sys.argv[2] + " " + sys.argv[3].replace(" ","~") + " " + "-----" + "\n")

    elif(len(sys.argv) == 5):
        file.write(sys.argv[2] + " " + sys.argv[3].replace(" ","~") + " " + sys.argv[4] + "\n")
    file.close()
    prettyprint(True)
elif(len(sys.argv) == 1):
    prettyprint(True)
elif(len(sys.argv) == 3 and sys.argv[1] == "rs"):
    info = prettyprint(False)
    seccao = sys.argv[2]
    if(seccao not in info):
        print("Secção não existe...")
        sys.exit(0)
    line_remover(["* " + seccao])
    l = [seccao + " " + x[0] + " " + x[1] for x in info[seccao]]
    line_remover(l)
    prettyprint(True)
elif(len(sys.argv) == 4 and sys.argv[1] == "rm"):
    info = prettyprint(False)
    seccao = sys.argv[2]
    if(seccao not in info):
        print("Secção não existe...")
        sys.exit(0)
    if(int(sys.argv[3]) > len(info[seccao]) or int(sys.argv[3]) <= 0):
        print("Id inválido...")
        sys.exit(0)
    line_remover([seccao + " " + info[seccao][int(sys.argv[3])-1][0] + " " + info[seccao][int(sys.argv[3])-1][1]])
    prettyprint(True)
elif(len(sys.argv) == 2 and sys.argv[1] == "datas"):
    file = open(file_path,"r")
    lines = file.readlines() 
    info = {}

    for l in lines:
        data = l.split()
        if(data[0] == "*"):
            info[data[1]] = []
        elif(data[2] != "-----"):
            info[data[0]].append((data[1],data[2]))

    headers = ["Secção","Tarefa","Data"]
    table = []
    for x in info:
        s = "\n"
        datas = "\n"
        num = 1
        for y in info[x]:
            s += str(num) + " - " + y[0] + "\n"
            datas += y[1] + "\n"
            num += 1
        
        # Para não aparecerem secções sem secções
        if(s != "\n" and datas != "\n"):
            table.append([x,s.replace("~"," "),datas])

    print(tabulate(table, headers, tablefmt='fancy_grid'))
    file.close()

    
elif(len(sys.argv) == 2 and sys.argv[1] == "help"):
    print("╒═══════════════════════════════════════════════════════════════════════════════════════╕")
    print("│ $ todo                                         -> Mostra os to-dos de cada secção     │")
    print("│ $ todo add \"tarefa\" [\"data\"]                   -> Novo to-do na secção \"GERAl\"        │")
    print("│ $ todo add \"nome_secção\" \"tarefa\" [\"data\"]     -> Novo to-do numa secção à escolha    │")
    print("│ $ todo rm \"nome_secção\" \"id-tarefa\"            -> Remove um to-do de uma secção       │")
    print("│ $ todo rs \"nome_secção\"                        -> Remove uma secção                   │")
    print("│ $ todo datas                                   -> Mostra os to-dos com data por ordem │")
    print("╘═══════════════════════════════════════════════════════════════════════════════════════╛")
else:
    print(sys.argv)
    print("Argumento inválido!")
