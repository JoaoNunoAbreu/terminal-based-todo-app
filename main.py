import sys
import json
import os
from sys import argv
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + "/data.json"


def readTasks():
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def writeTasks(info):
    with open(file_path, 'w') as outfile:
        json.dump(info, outfile, indent=4, ensure_ascii=False)


def newTask(info, section, task, date):
    next_id = len(info[section]) + 1
    info[section].append({
        "id": next_id,
        "task": task,
        "date": date
    })
    writeTasks(info)


def normalize(info):
    for i in info:
        count = 1
        for elem in info[i]:
            elem['id'] = count
            count += 1
    return info

def are_there_tasks(data):
    for i in data:
        if data[i] != []:
            return True
    return False

def prettyprint(data):

    if(are_there_tasks(data) == False):
        print("No data. Try adding some tasks! Use \"todo help\" for more info.")
        return

    table = []
    section_width = 8
    task_width = 5
    for x, y in data.items():
        identifier = 1
        for i in y:
            table.append([x, f"{identifier} - {i['task']}", i["date"]])
            if len(x) > section_width:
                section_width = len(x)
            if len(i["task"]) + 4 > task_width:
                task_width = len(i["task"]) + 4
            identifier += 1

    print()
    print(f" {'Section':<{section_width}} | {'Task':<{task_width}} | {'Date':<6}")

    last_section = ""
    for i in table:
        if i[0] != last_section:
            print("-" * (section_width+2) + "+" + "-" * (task_width+2) + "+" + "-" * 9)
            print(f" {i[0]:<{section_width}} | {i[1]:<{task_width}} | {i[2]:<7}")
            last_section = i[0]
        else:
            print(f" {' ':<{section_width}} | {i[1]:<{task_width}} | {i[2]:<7}")

    print()


def main():
    if((len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5) and sys.argv[1] == "add"):

        info = readTasks()

        # Cria a seccção, caso não exista
        if(len(sys.argv) == 3 or (len(sys.argv) == 4 and "/" in sys.argv[3])):
            if("GENERAL" not in info):
                info["GENERAL"] = []
        else:
            if(argv[2] not in info and "/" not in sys.argv[3]):
                info[sys.argv[2]] = []

        # Adiciona nova task ao ficheiro
        if(len(sys.argv) == 3):
            newTask(info, "GENERAL", sys.argv[2], "-----")

        elif(len(sys.argv) == 4):
            # Caso tenha data sem seção
            if("/" in sys.argv[3]):
                newTask(info, "GENERAL", sys.argv[2], sys.argv[3])
            # Caso tenha secção sem data
            else:
                newTask(info, sys.argv[2], sys.argv[3], "-----")

        elif(len(sys.argv) == 5):
            if("/" not in sys.argv[4]):
                print("Invalid date...")
                sys.exit()
            newTask(info, sys.argv[2], sys.argv[3], sys.argv[4])

        prettyprint(readTasks())

    elif(len(sys.argv) == 1):
        prettyprint(readTasks())
    elif(len(sys.argv) == 3 and sys.argv[1] == "rs"):
        info = readTasks()
        seccao = sys.argv[2]
        if(seccao not in info):
            print("Section doesn't exist...")
            sys.exit(0)
        del info[seccao]
        writeTasks(info)
    elif(len(sys.argv) == 4 and sys.argv[1] == "rm"):
        info = readTasks()
        seccao = sys.argv[2]
        if(seccao not in info):
            print("Section doesn't exist...")
            sys.exit(0)
        if(int(sys.argv[3]) > len(info[seccao]) or int(sys.argv[3]) <= 0):
            print("Invalid id...")
            sys.exit(0)

        found = False
        for i in range(len(info[seccao])):
            if(info[seccao][i]['id'] == int(sys.argv[3])):
                del info[seccao][i]
                found = True
                break

        if(found == False):
            print("Invalid id...")
        else:
            info = normalize(info)
            writeTasks(info)
    elif(len(sys.argv) == 2 and sys.argv[1] == "dates"):
        info = readTasks()
        info_with_dates = {}

        for sec in info:
            for i in info[sec]:
                if(i["date"] != "-----"):
                    if(sec not in info_with_dates):
                        info_with_dates[sec] = []
                    info_with_dates[sec].append(i)
        prettyprint(info_with_dates)

    elif(len(sys.argv) == 2 and sys.argv[1] == "today"):
        info = readTasks()
        info_with_dates = {}
        todays_date = datetime.now().strftime("%d/%m")
        for sec in info:
            for i in info[sec]:
                if(i["date"] == todays_date):
                    if(sec not in info_with_dates):
                        info_with_dates[sec] = []
                    info_with_dates[sec].append(i)
        prettyprint(info_with_dates)
    elif(len(sys.argv) == 2 and sys.argv[1] == "help"):
        print("$ todo                                       -> Show the tasks for each section")
        print("$ todo add \"task\" [\"date\"]                   -> New task to the \"GENERAL\" section")
        print("$ todo add \"section_name\" \"task\" [\"date\"]    -> New task to a section")
        print("$ todo rm \"section_name\" \"id-task\"           -> Removes task from a section")
        print("$ todo rs \"section_name\"                     -> Removes a section")
        print("$ todo dates                                 -> Shows the tasks with deadline dates")
        print("$ todo today                                 -> Shows the tasks with today's deadline date")
    else:
        print(sys.argv)
        print("Invalid arguments!")


if __name__ == '__main__':
    main()
