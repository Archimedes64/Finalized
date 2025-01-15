import os
import datetime
import json
import toml
from rich.console import Console
from dateutil.rrule import rrule, DAILY, WEEKLY,MONTHLY

console = Console()
DESCRIPTION_NEWLINE_INTERVAL = 7
PATH = 'saves'
CLOCK_SYMBOL = "🕒"
PRIORITY_ORDER = {"high": 1, "mid": 2, "low": 3}
CURRENT_DATE = datetime.datetime.now()
#CURRENT_DATE = datetime.datetime.strptime("2025/02/13","%Y/%m/%d")
#==========================
# Config Loading
#==========================
with open('config.toml', 'r') as f:
    config = toml.load(f)
# this might be the worse thing ive ever writen completly unreadabel
 # function takes a dictionary of default values for the settings and checks if new ones were writen in the config
# if they are it replaces the default with the new value 
# returns new settings 
#ps: as of 10 mins after writing originally this was re writen so it does not need this documentation to under stand

def replace_defaults(defaults, config_settings):
    new_settings = defaults
    for default in defaults:
        if default.lower() in config_settings:
            new_settings[default] = config_settings[default.lower()]
    return new_settings

COLORS_DEFAULT = {
    'TOP_BAR':'red',
    'GOAL_INDICATOR':'yellow',
    'MODE_INDICATOR':'red',
    'SORT_INDICATOR':'grey',
    'TASK': 'white',
    'TASK_DETAILS':'grey',
    'TASK_PRIORITY_TAG': 'yellow',
    'TASK_TIME_TAG': 'green'
}
DISPLAY_DEFAULT = {
    'DEFAULT_SORT':'due_date',
    'IS_DEFAULT_SORT_REVERSED':True
}
colors = replace_defaults(COLORS_DEFAULT, config['colors'])
display_settings = replace_defaults(DISPLAY_DEFAULT,config['display'])
#===========================
# Date Functions
#===========================

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

def get_current_date():
    current_date = datetime.now()
    return current_date.strftime('%Y/%m/%d')

#all this was ai 
def get_next_monthly_occurrence(start_date, count=2):
    # Convert string date to datetime object
    start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
    # Create a recurrence rule for monthly occurrences
    rule = rrule(MONTHLY, dtstart=start_date, count=count)
    # Get the next occurrences
    occurrences = list(rule)
    return occurrences[1]

def get_next_daily_occurrence(start_date, count=2):
    start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
    rule = rrule(DAILY, dtstart=start_date, count=count)
    return list(rule)[1]

def get_next_weekly_occurrence(start_date, count=2):
    start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
    rule = rrule(WEEKLY, dtstart=start_date, count=count)
    return list(rule)[1]

def check_occurrences(occurrence):
    return CURRENT_DATE >= occurrence
#ai end
    
# ===========================
# Input Functions
# ===========================


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
        
def get_recurring_interval():
    valid_intervals = ['monthly','weekly','daily','every time']
    while True:
        user_input = input("what interval for this task (Monthly, Weekly, Daily, Every Time): ").lower()
        if user_input not in valid_intervals:
            print('Not a valid interval')
            continue
        return user_input
        
def get_tasks_goal():
    save = load_save()
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
    return goal
    
def get_tasks_title():
    title = input("Task title: ")
    check = validate_task(title)
    while not check[0]:
        print(check[1])
        title = input("Task title: ")
        check = validate_task(title)
    return title
# ===========================
# Validation Functions
# ===========================

def check_length(checked_type, the_checked, length):
    if len(the_checked) < length:
        return [False, f'{checked_type} must be longer than {length} characters']
    return [True]

def validate_goal(goal):
    save = load_save()
    if not check_length("Goals", goal, 4)[0]:
        return check_length['goals']['all']("goals", goal, 4)
    elif goal in save['goals']:
        return [False, "Goal already exists"]
    return [True]

def validate_task(task_title):
    save = load_save()
    if not check_length("Task", task_title, 4)[0]:
        return check_length("tasks", task_title, 4)
    if any(task['title'] == task_title for task in save['tasks']):
        return [False, "Task already exists"]
    return [True]

# ===========================
# Data Management Functions
# ===========================


def load_save():
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

    goals = {  
        'all': {
                    'details': "every task"
                },

        'misc': {
            'details': "tasks that have no goal"
        }
    }
    for goal in user_goals:
        details = get_goal_details(goal)
        goals[goal] = {
            'details': details
        }

    data = {
        'tasks': [],
        'goals': goals,
        'user_goal_names': user_goals,
        'name': name,
        'tasks_done': 0
    }
    save_data(data)
    
def save_new_task(tasks_details,goal):
    save = load_save()
    tasks_details['goal'] = goal
    save['tasks'].append(tasks_details)
    save_data(save)

def format_details(detail):
    details = detail
    details = details.split()
    length = len(details)
    for i in range(0, length - 4, DESCRIPTION_NEWLINE_INTERVAL):
        if i == 0:
            continue
        details.insert(i + i // DESCRIPTION_NEWLINE_INTERVAL, '\n')
    details = " ".join(details)
    return details
    
def get_time_tag(task):
    if task['due_date'] == None:
        return f'(Interval: {task['interval']['interval'].upper()})'
    return f'(DUE: {task['due_date'][5:-1] at {task['']}})'

def update_pending_tasks():
    save = load_save()
    for task in get_tasks_todo('all'):
        
        next_occurrence = None
        if task['interval']['interval'] == 'daily':
            next_occurrence = get_next_daily_occurrence(start_date=task['interval']['prev_date'])
        elif task['interval']['interval'] == 'weekly':
            next_occurrence = get_next_weekly_occurrence(start_date=task['interval']['prev_date'])
        elif task['interval']['interval'] == 'monthly':
            next_occurrence = get_next_monthly_occurrence(start_date=task['interval']['prev_date'])
        if next_occurrence and check_occurrences(next_occurrence):
            task['interval']['status'] = 'up'  
            task['interval']['prev_date'] = CURRENT_DATE.strftime('%Y/%m/%d')
    save_data(save)
                
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
    save = load_save()
    save['goals'][goal_name] = {
        'tasks': {'todo': [], 'done': []},
        'details': details
    }
    save['user _goal_names'].append(goal_name)
    save_data(save)

def write_todo():

    title = get_tasks_title()
    details = input(f"{title} details: ")
    priority = get_priority()
    is_recurring = get_user_confirmation("Do you want this task to be recurring\n")
    
    if is_recurring:
        recurring_interval = get_recurring_interval()
        due_date = None
    else:
        due_date = get_due_date()
        recurring_interval = None
    
    goal = get_tasks_goal()

    tasks_details = {
        'title': title, 
        'details': details,
        'due_date': due_date,
        'priority': priority,
        'interval': {
                    'interval':recurring_interval,
                    'prev_date': datetime.datetime.strftime(CURRENT_DATE,"%Y/%m/%d"),
                    'status': 'up'
        }
}

    save_new_task(tasks_details, goal)
    
def get_task_ids(task_title):
    save = load_save()
    
    for i, tasks in enumerate(save['tasks']):
        if tasks['title'] == task_title:
            return i 
            

def finish_task(task_title):
    save = load_save()
    
    task_id  = get_task_ids(task_title)
    task = save['tasks'][task_id]
    
    while True:
        if task['interval']['interval'] == "Every Time":
            save['tasks_done'] += 1 
            save_data(save)
            return
            
        if task['due_date'] == None:
            task['interval']['status'] = 'pending'
            break
        
        repeat_task = get_user_confirmation("Do you want to repeat this task?")
        if repeat_task:
            new_due_date = get_due_date()
            task['due_date'] = new_due_date
            break
             
        del(save['tasks'][task_id])

        save['tasks_done'] += 1 
        save_data(save)
        return
        
    save['tasks_done'] += 1 
    save_data(save)

def clear_finished_tasks():

    save = load_save()
    save['tasks_done'] = 0
    save_data(save)

# ===========================
# Display Functions
# ===========================


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def get_sort_symbol(sort_type):
    if sort_type[0] == 'due_date':
        symbol = f'{CLOCK_SYMBOL}'
    elif sort_type[0] == 'priority':
        symbol = f'❗'
    if sort_type[1]:
        symbol += "🡅 :sort"
    else:
        symbol += '⬇ :sort'
    return symbol

def tasks_screen(goal, sort_type,mode):
    clear_screen()
    save = load_save()
    goals = "     ".join((list(save['goals']))).upper()
    symbol = get_sort_symbol(sort_type)

    console.print(f"[bold {colors['TOP_BAR']}] \t{goals} [/bold {colors['TOP_BAR']}]"
                  f"\n\t{(' '*len(goals)) + '\t'}[{colors['SORT_INDICATOR']}] {symbol}[/{colors['SORT_INDICATOR']}]")
    console.print(f"[bold {colors['GOAL_INDICATOR']}] {goal.upper()}: [/bold {colors['GOAL_INDICATOR']}]")
    
    for task in sort_list(sort_type, get_tasks_todo(goal)):
    
        details = format_details(task['details'])
        priority = task['priority']
        time_tag = get_time_tag(task) # i know this name sucks but idk

        console.print(f"\n[bold] [{colors['TASK']}]-{task['title']} [/{colors['TASK']}]"
            f"[{colors['TASK_PRIORITY_TAG']}](Priority: {priority.upper()})[/{colors['TASK_PRIORITY_TAG']}][/bold] \n"
            f"[{colors['TASK_DETAILS']}]{details}[/{colors['TASK_DETAILS']}]"
            f"[{colors['TASK_TIME_TAG']}] {time_tag}[/{colors['TASK_TIME_TAG']}]"
            )

def list_up_tasks(goal):
    tasks = get_tasks_todo(goal)
    for indx, task in enumerate(tasks):
        console.print(f'[bold]{indx+1}:\n   {task["title"]}[bold]')

def get_amount_of_tasks_todo(goal):
    print(len(get_tasks_todo(goal)))
    
def Finish_Mode(goal):
    save = load_save()
    clear_screen()
    console.print(f'[bold {colors['MODE_INDICATOR']}]Finish[/bold {colors['MODE_INDICATOR']}]\n')
    list_up_tasks(goal)
    finish_mode_no_info(goal)

def Add_Mode():
    clear_screen()
    console.print(f"[bold {colors['MODE_INDICATOR']}]Add [/bold {colors['MODE_INDICATOR']}]")

    while True:
        user_input_add = input("What do you want to add?\n  Goal = 1\n  Task = 2\n  Subtask = 3\n\n: ")
        if user_input_add not in ['1','2','3']:
            print("Not a valid input please enter a number 1-3")
        break
    if user_input_add == "1":
        add_goal()

    elif user_input_add == "2":
        write_todo()
        
def get_tasks_todo(goal):
    save = load_save()
    unfiltered_tasks = save['tasks']
    return [task for task in unfiltered_tasks if task['interval']['status'] == 'up']
    
def finish_mode_no_info(goal):
    tasks = get_tasks_todo(goal)
    while True:
            task_input = input('\nTask Index:')
    
            if task_input.isdigit() is False:
                print('Make sure the index you put in is a digit')
                continue
    
            task_index = int(task_input) - 1 
            if len(tasks) <= task_index or task_index < 0:
                print('\nInvalid Index')
                continue
    
            task_name = tasks[task_index]["title"]     
            break
    finish_task(task_name)
def has_saves():
    if not os.path.exists('saves/saves.json'):  
        init_saves()

def sort_list(sort_type, task_list):
    tasks_with_due_dates = [task for task in task_list if task['due_date'] is not None]
    tasks_with_intervals = [task for task in task_list if task['due_date'] is None]
    
    if sort_type[0] == 'due_date':
        sorted_list = tasks_with_intervals + sorted(tasks_with_due_dates, key=lambda x: datetime.datetime.strptime(x['due_date'], '%Y/%m/%d'))
    elif sort_type[0] == 'priority':
        sorted_list = sorted(task_list, key=lambda x: (PRIORITY_ORDER.get(x['priority'], 4)))
    
    if sort_type[1]:
        return sorted_list[::-1]
    return sorted_list
