import sys
from sys import argv
import os.path
from os import path
from tabulate import tabulate

file_path = "/Users/joaonunoabreu/Desktop/Util/Python/todo-app/data.txt"

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
            info[data[1]] = [];
        else:
            info[data[0]].append(data[1])

    if(printable):
        
        headers = ["Secção","Tarefa"]
        table = []
        for x in info:
            s = "\n"
            num = 1
            for y in info[x]:
                s += str(num) + " - " + y + "\n"
                num += 1
            table.append([x,s.replace("~"," ")])

        print(tabulate(table, headers, tablefmt='fancy_grid'))

    file.close()
    return info

if(len(sys.argv) == 4 and sys.argv[1] == "add"):

    info = prettyprint(False)
    file = open(file_path,"a")
    if(argv[2] not in info):
        file.write("* "+sys.argv[2]+"\n")

    file.write(sys.argv[2] + " " + sys.argv[3].replace(" ","~") + "\n")
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
    l = [seccao + " " + x for x in info[seccao]]
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
    #line_remover([seccao + " " + info[seccao][int(sys.argv[3])-1]])
    prettyprint(True)
else:
    print(sys.argv)
    print("Argumento inválido!")
