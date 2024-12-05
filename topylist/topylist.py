import os
import datetime
import argparse
import json
from rich.console import Console
console = Console()
DESCRIPTION_NEWLINE_INTERVAL = 7
PATH = 'topylist/saves'
def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
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

def write_todo(title,task,due_date):
    save = load_todos()
    print(type(save))
    if any(task['title'] == title for task in save['tasks']['todo']):
        clear_screen()
        print('Already a task with that title')
        useless = input(": ")
        return

    save['tasks']['todo'].append({'title':title, 'details':task,'due_date':due_date})
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
    clear_screen()
    save = load_todos()
    console.print("[bold red]Tasks: [/bold red]")
    
    for task in save['tasks']['todo']:
        details = task['details']
        
        details = details.split()
        length = len(details)
        for i in range(0,length-4,DESCRIPTION_NEWLINE_INTERVAL):
            if i ==0:
                continue
            details.insert(i+i//DESCRIPTION_NEWLINE_INTERVAL,'\n    ')
        details = " ".join(details)
        console.print(f"\n[bold]Title: {task['title']}\n  Description:\n [/bold]    {details}\n[bold]  due-date: [/bold][green]{task['due_date']}[/green]")
def Finish_Mode():
    
    save = load_todos()
    for task in save['tasks']['todo']:
        console.print(f'[bold]   {task['title']}[bold]')
def has_saves():
    if not os.path.exists('topylist/saves/saves.json'):  
        init_saves()
def main():
    








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
