import os
import datetime
import argparse
import json
from colorama import Fore, Style
PATH = 'topylist/saves'

argparser= argparse.ArgumentParser(description='A simple todo list program')

def load_todos():
    with open(PATH + '/saves.json','r') as f:
        return json.load(f)

def init_saves():
    os.makedirs(PATH,exist_ok=True)
    name = input('whats your name?: ')
    data = {
        'tasks': {'todo': [], 'done': []},
        'name': name,
        'tasks_done': 0
    }
    with open(PATH +'/saves.json','w') as f:
        json.dump(data,f)

def write_todo(task,title):
    save = load_todos()
    print(type(save))
    if any(task['title'] == title for task in save['tasks']['todo']):
        print('Already a task with that title')
        return
    save['tasks']['todo'].append({'title':title, 'details':task,'date':datetime.date.today().strftime('%Y-%m-%d')})
    print(save)
    with open(PATH + '/saves.json','w') as f:
        json.dump(save,f)


def finish_task(task_title):
    save = load_todos()
    for task_id, tasks in enumerate(save['tasks']['todo']):
        if tasks['title'] == task_title:
            task = save['tasks']['todo'][task_id]
            del(save['tasks']['todo'][task_id])
            break
    else:
        print('No task with title: '+task_title)
        return
    save['tasks']['done'].append(task)
    save['tasks_done'] += 1 
    with open(PATH + '/saves.json','w') as f:
        json.dump(save,f)
def clear_finished_tasks():
    save = load_todos()
    save['tasks_done'] = 0
    save['tasks']['done'] = []
    with open(PATH + '/saves.json','w') as f:
        json.dump(save,f)
def tasks_screen():
    save = load_todos()
    for task in save['tasks']['todo']:
        print(task['title'])
def main():
    if not os.path.exists('topylist/saves/saves.json'):  
        init_saves()
    saves = load_todos()








    argparser.add_argument('-a','--add',action='store_true')
    argparser.add_argument('-l','--list',action='store_true')
    argparser.add_argument('-f','--finish',action='store_true')
    argparser.add_argument('-lf','--list_finished',action='store_true')
    argparser.add_argument('--reset',action='store_true')
    
    args  = argparser.parse_args()
    if args.add:
        title = input("Enter task title: ")
        description = input("Task Description: ")
        write_todo(description,title)
    elif args.list:
        tasks_screen()
    elif args.list_finished:
        pass
    elif args.finish:
        finish_task(task_title=input("Task title you finished: "))
    elif args.reset:
        init_saves()

if __name__ == '__main__':
    main()
