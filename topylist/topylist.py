import os
import datetime
import argparse
import json
from rich.console import Console
console = Console()
DESCRIPTION_NEWLINE_INTERVAL = 7
PATH = 'topylist/saves'
def check_length(checked_type,the_checked,length):
    if len(the_checked) > length:
        return [False,f'{checked_type} must be longer than {length} charecters']
    return [True]
def validate_goal(goal):
    save = load_todos()
    if not check_length("Goals",goal,4)[0]:
        return check_length("goals",goal,4)
    elif goal in save['goals']:
        return [False,"Goal already exsists"]
    return [True]
def validate_task(task):
    save = load_todos()
    if not check_length("Task",task,4)[0]:
        return check_length("tasks",task,4)
    elif any(task['title'] == task for task in save['goals']['all']['tasks']['todo']):
        return [False,"Task already exsists"]
    return [True]
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
def save_data(data):
    with open(PATH + '/saves.json','w') as f:
        return json.dump(data, f,indent=5)
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
    save_data(data)
def user_authenication(prompt):
    while True:
        user_input =input(prompt+'(y/n): ')
        if user_input.lower() in ['y','n']:
            if user_input.lower() == 'n':
                return False
            return True
        print('Not valid input')
def add_goal():
    goal_name = input("Name of goal: ").lower()
    check = validate_goal(goal_name)
    while not  check[0]:
        print(check[1])
        goal_name = input("Name of goal: ").lower()
        check = validate_goal(goal_name)
    save = load_todos()
    save['goals'][goal_name] = {'todo':[],'done':[]}
    save_data(save)
    
def write_todo(due_date):
    title = input("Task title: ")
    check = validate_task(title)
    while not check[0]:
        print(check[1])
        title = input("Task title: ")
        check = validate_task(title)
    task = input(f"{title} details: ")
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
    save['goals']['all']['tasks']['todo'].append({'title':title, 'details':task,'due_date':due_date,'goal':goal})

    save_data(save)
    


def finish_task(task_title):
    
    save = load_todos()
    for task_id, tasks in enumerate(save['goals']['all']['tasks']['todo']):
        if tasks['title'] == task_title:
            task = save['goals']['all']['tasks']['todo'][task_id]
            del(save['goals']['all']['tasks']['todo'][task_id])
            del(save['goals'][task['goal']]['tasks']['todo'][task_id])
            break
    else:
        print('No task with title: '+ task_title)
        return
    
    save['goals']['all']['tasks']['done'].append(task)
    save['goals'][task['goal']]['tasks']['done'].append(task)
    print(save)
    save['tasks_done'] += 1 
    save_data(save)
def clear_finished_tasks():
    save = load_todos()
    save['tasks_done'] = 0
    save['tasks']['done'] = []
    save_data(save)
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
def Finish_Mode(goal):
    save = load_todos()
    for task in save['goals'][goal]['tasks']['todo']:
        console.print(f'[bold]   {task['title']}[bold]')
def has_saves():
    if not os.path.exists('topylist/saves/saves.json'):  
        init_saves()

