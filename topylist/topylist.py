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
    user_goals = input('What goals do you have that you want to do\nthink of goals like long term tasks that you do tasks to complete\nEnter your goals ex:goal1 goal2 goal3: ')
    user_goals = user_goals.lower().split()
    tasks = {
        'todo':[],
        'done':[]
    }
    goals = {  
    'all':{
        'tasks': tasks,
        'details':"every task"
    },
    'misc':{
        'tasks': tasks,
        'details':"tasks that have no goal"
    },
    }
    for goal in user_goals:
        details = f"Tasks related to {goal}"
        while True:    

            user_input = input(f'Do you want to write your own description for goal:  {goal}?(y,n): ')
            if user_input.lower() == 'y':
                details = input(f'Enter your description for {goal}: ')
                break
            elif user_input.lower() == 'n':
                print('Ok using default description')
                break
        goals[goal] = {
        'tasks': tasks,
        'details': details
    }
    print(goals)
    data = {
        'goals': goals,
        'name': name,
        'tasks_done': 0,
        
    }
    print(data)
    with open(PATH +'/saves.json','w') as f:
        json.dump(data,f,indent=5)

def write_todo(title,task,due_date):
    save = load_todos()
    while True:
        goal = input("Goal this is under [leave blank if no goal]: ")
        if goal == '':
            goal = "misc"
        elif goal not in list(save['goals']):
            print('not a goal you have made')
            continue
        break
    print(type(save))
    if any(task['title'] == title for task in save['goals'][goal]['tasks']['todo']):
        clear_screen()
        print('Already a task with that title')
        useless = input(": ")
        return

    save['goals'][goal]['tasks']['todo'].append({'title':title, 'details':task,'due_date':due_date})
    save['goals']['all']['tasks']['todo'].append({'title':title, 'details':task,'due_date':due_date})

    with open(PATH + '/saves.json','w') as f:
        json.dump(save,f,indent=5)


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
        json.dump(save,f,indent=5)
def clear_finished_tasks():
    save = load_todos()
    save['tasks_done'] = 0
    save['tasks']['done'] = []
    with open(PATH + '/saves.json','w') as f:
        json.dump(save,f,indent=5)
def tasks_screen(goal):
    clear_screen()
    save = load_todos()
    console.print(f"[bold red] \t{"\t".join((list(save['goals']))).upper()} [/bold red]")
    console.print(f"[bold yellow] {goal.upper()}: [/bold yellow]")
    
    for task in save['goals'][goal]['tasks']['todo']:
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
