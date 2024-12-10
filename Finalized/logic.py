import os
import datetime
import json
from rich.console import Console

console = Console()
DESCRIPTION_NEWLINE_INTERVAL = 7
PATH = 'Finalized/saves'
CLOCK_SYMBOL = "🕒"

# ===========================
# Input Functions
# ===========================

def get_due_date() -> str:
    while True:    
        date = input(' Due Date YYYY/MM/DD: ')
        list(date)
        if len(date) != 10:
            continue

        if date[4] != '/' and date[7] != '/':
            continue

        if int(date[5:7]) > 12:
            continue

        if int(date[:4]) >= 2024:
            break
    return "".join(date)

def get_priority():
    while True:
        priority = input("Task priority(High, Mid, Low): ").lower()
        if priority not in ('high','mid','low'):
            print("Not a valid priority")
            continue
        return priority

def get_goal_details(goal_title):
    user_input = get_user_confirmation(f'Do you want to write your own description for goal:  {goal_title}: ')
    if user_input:
        return input(f'Enter your description for {goal_title}: ')
    else:
        print('Ok using default description')
        return f'Tasks related to {goal_title}'

def get_user_confirmation(prompt):
    while True:
        user_input = input(prompt + '(y/n): ')
        if user_input.lower() in ['y', 'n']:
            return user_input.lower() == 'y'
        print('Not valid input')

# ===========================
# Validation Functions
# ===========================

def check_length(checked_type, the_checked, length):
    if len(the_checked) < length:
        return [False, f'{checked_type} must be longer than {length} characters']
    return [True]

def validate_goal(goal):
    save = load_todos()
    if not check_length("Goals", goal, 4)[0]:
        return check_length("goals", goal, 4)
    elif goal in save['goals']:
        return [False, "Goal already exists"]
    return [True]

def validate_task(task_title):
    save = load_todos()
    if not check_length("Task", task_title, 4)[0]:
        return check_length("tasks", task_title, 4)
    if any(task['title'] == task_title for task in save['goals']['all']['tasks']['todo']):
        return [False, "Task already exists"]
    return [True]

# ===========================
# Data Management Functions
# ===========================

def load_todos():
    with open(PATH + '/saves.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open(PATH + '/saves.json', 'w') as f:
        return json.dump(data, f, indent=5)

def init_saves():
    os.makedirs(PATH, exist_ok=True)
    name = input('whats your name?: ')
    user_goals = input('What goals do you have that you want to do\nthink of goals like long term tasks that you do tasks to complete\nEnter your goals ex:goal1 goal2 goal3: ')
    user_goals = user_goals.lower().split()
    tasks = {
        'todo': [],
        'done': []
    }
    goals = {  
        'all': {
            'tasks': tasks,
            'details': "every task"
        },
        'misc': {
            'tasks': tasks,
            'details': "tasks that have no goal"
        },
    }
    for goal in user_goals:
        details = get_goal_details(goal)
        goals[goal] = {
            'tasks': tasks,
            'details': details
        }
    print(goals)
    data = {
        'goals': goals,
        'user_goal_names': user_goals,
        'name': name,
        'tasks_done': 0,
    }
    save_data(data)

# ===========================
# Task Management Functions
# ===========================

def add_goal():
    goal_name = input("Name of goal: ").lower()
    check = validate_goal(goal_name)
    details = get_goal_details(goal_name)
    while not check[0]:
        print(check[1])
        goal_name = input("Name of goal: ").lower()
        check = validate_goal(goal_name)
    save = load_todos()
    save['goals'][goal_name] = {
        'tasks': {'todo': [], 'done': []},
        'details': details
    }
    save['user _goal_names'].append(goal_name)
    save_data(save)

def write_todo():
    title = input("Task title: ")
    check = validate_task(title)
    
    while not check[0]:
        print(check[1])
        title = input("Task title: ")
        check = validate_task(title)

    details = input(f"{title} details: ")
    priority = get_priority()
    due_date = get_due_date()
    save = load_todos()
    print("Available goals:")
    
    for goal in save['user_goal_names']:
        console.print(f"-[bold red] {goal.upper()}[/bold red]")

    while True:
        goal = input("Goal this is under [leave blank if no goal]: ")
        if goal == '':
            goal = "misc"
        elif goal not in list(save['goals']):
            print('not a goal you have made')
            continue
        break
    tasks_details = {
        'title': title, 
        'details': details,
        'due_date': due_date,
        'priority': priority
    }
    save['goals'][goal]['tasks']['todo'].append(tasks_details)
    tasks_details['goal'] = goal
    save['goals']['all']['tasks']['todo'].append(tasks_details)

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
        print('No task with title: ' + task_title)
        return
    
    save['goals']['all']['tasks']['done'].append(task)
    save['goals'][task['goal']]['tasks']['done'].append(task)
    print(save)
    save['tasks_done'] += 1 
    save_data(save)

def clear_finished_tasks():
    save = load_todos()
    save['tasks_done'] = 0
    save['goals']['all']['tasks']['done'] = []
    save_data(save)

# ===========================
# Display Functions
# ===========================

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def tasks_screen(goal, sort_type):
    clear_screen()
    save = load_todos()
    goals = "     ".join((list(save['goals']))).upper()
    if sort_type[0] == 'due_date':
        symbol = f'{CLOCK_SYMBOL}'
    elif sort_type[0] == 'priority':
        symbol = f'❗'
    if sort_type[1]:
        symbol += "🡅 :sort"
    else:
        symbol += '⬇ :sort'
    console.print(f"[bold red] \t{goals} [/bold red]\n\t{(' '*len(goals)) + '\t'} {symbol}")
    console.print(f"[bold yellow] {goal.upper()}: [/bold yellow]")
    
    for task in sort_list(sort_type, save['goals'][goal]['tasks']['todo']):
        details = task['details']
        
        details = details.split()
        length = len(details)
        for i in range(0, length - 4, DESCRIPTION_NEWLINE_INTERVAL):
            if i == 0:
                continue
            details.insert(i + i // DESCRIPTION_NEWLINE_INTERVAL, '\n    ')
        details = " ".join(details)
        console.print(f"\n[bold]Title: {task['title']}\n  Description:\n [/bold]    {details}\n[bold]  due-date: [/bold][green]{task['due_date']}[/green]")

def Finish_Mode(goal):
    save = load_todos()
    for task in save['goals'][goal]['tasks']['todo']:
        console.print(f'[bold]   {task["title"]}[bold]')

def has_saves():
    if not os.path.exists('Finalized/saves/saves.json'):  
        init_saves()

def sort_list(sort_type, task_list):
    priority_order = {"high": 1, "mid": 2, "low": 3}
    if sort_type[0] == 'due_date':
        sorted_list = sorted(task_list, key=lambda x: datetime.datetime.strptime(x['due_date'], '%Y/%m/%d'))
    elif sort_type[0] == 'priority':
        sorted_list = sorted(task_list, key=lambda x: (priority_order.get(x['priority'], 4)))
    
    if sort_type[1]:
        return sorted_list[::-1]
    return sorted_list

def get_sort_type():
    pass