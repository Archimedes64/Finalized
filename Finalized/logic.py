import os
import datetime
import json
from rich.console import Console
from dateutil.rrule import rrule, DAILY, WEEKLY,MONTHLY
import pytermgui as ptg

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

OUTPUT = {'task':{}}








console = Console()
DESCRIPTION_NEWLINE_INTERVAL = 7
PATH = 'Finalized/saves'
CLOCK_SYMBOL = "🕒"
PRIORITY_ORDER = {"high": 1, "mid": 2, "low": 3}
CURRENT_DATE = datetime.datetime.now()
#===========================
# Date Functions
#===========================
def is_valid_due_date(date) -> str:
    list(date)
    if len(date) != 10:
        return False
    return date[4] == '/' and date[7] == '/'


def get_current_date():
    current_date = datetime.now()
    return current_date.strftime('%Y/%m/%d')

#all this was ai im to lazy to deal with a  random module
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
    return CURRENT_DATE >= occurrence.date()
        
    
# ===========================
# Input Functions
# ===========================


def is_valid_priority(priority):
    return priority  in ('high','mid','low')


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
    return len(the_checked) < length
        

def validate_goal(goal):
    save = load_save()
    if not check_length("Goals", goal, 4)[0]:
        return check_length("goals", goal, 4)
    elif goal in save['goals']:
        return False
    return True

def validate_task(task_title):
    save = load_save()
    if not check_length("Task", task_title, 4)[0]:
        return check_length("tasks", task_title, 4)
    if any(task['title'] == task_title for task in save['goals']['all']['tasks']):
        return False 
    return True

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
            'tasks': [],
            'details': "every task"
        },
        'misc': {
            'tasks': [],
            'details': "tasks that have no goal"
        },
    }
    for goal in user_goals:
        details = get_goal_details(goal)
        goals[goal] = {
            'tasks': [],
            'details': details
        }

    data = {
        'goals': goals,
        'user_goal_names': user_goals,
        'name': name,
        'upcoming_tasks': [],
        'tasks_done': 0,
    }
    save_data(data)
def save_new_task(tasks_details,goal):
    save = load_save()
    save['goals'][goal]['tasks'].append(tasks_details)
    tasks_details['goal'] = goal
    save['goals']['all']['tasks'].append(tasks_details)
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
    return f'(DUE: {task['due_date']})'

def update_pending_tasks():
    save = load_save()
    for task in save['goals']['all']['tasks']:
        if task['interval']['status'] == 'up':
            continue
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



def finish_task(task_title):
    save = load_save()
    task = None
    for i, tasks in enumerate(save['goals']['all']['tasks']):
        if tasks['title'] == task_title:
            task_id = i
            task = save['goals']['all']['tasks'][task_id]
            break
    if task == None:
        return 
    for i, tasks in enumerate(save['goals'][task['goal']]['tasks']):
        if tasks['title'] == task_title:    
            task_id1 = i
            break
    if save['goals'][task['goal']]['tasks'][task_id1]['due_date'] == None:
        print('debug message')
        save['goals'][task['goal']]['tasks'][task_id1]['interval']['status'] = 'pending'
        save['goals']['all']['tasks'][task_id]['interval']['status'] = 'pending'
        save_data(save)
        return
    repeat_task = get_user_confirmation("Do you want to repeat this task?")
    if repeat_task:
        new_due_date = get_due_date()
        save['goals'][task['goal']]['tasks'][task_id1]['due_date'] = new_due_date
        save['goals']['all']['tasks'][task_id]['due_date'] = new_due_date
    else:
        del(save['goals'][task['goal']]['tasks'][task_id1])
        del(save['goals']['all']['tasks'][task_id])
    save['tasks_done'] += 1 
    save_data(save)

def clear_finished_tasks():
    save = load_save()
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

    console.print(f"[bold red] \t{goals} [/bold red]\n\t{(' '*len(goals)) + '\t'} {symbol}")
    console.print(f"[bold yellow] {goal.upper()}: [/bold yellow]")
    
    for task in sort_list(sort_type, save['goals'][goal]['tasks']):
        if task['interval']['status'] == 'pending':
            continue
        details = format_details(task['details'])
        priority = task['priority']
        time_tag = get_time_tag(task) # i know this name sucks but idk

        console.print(f"\n[bold]-{task['title']} [yellow](Priority: {priority.upper()})[/yellow] \n [/bold]{details}[green] {time_tag}[/green]")

def has_saves():
    if not os.path.exists('Finalized/saves/saves.json'):  
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
def submit_task(manager: ptg.WindowManager, window: ptg.Window) -> None:

    goal = window[1].value 
    title = window[2].value  
    details = window[3].value  
    due_date = window[4].value  
    priority = window[5].value.lower()
    interval = window[6].value.lower()
    task = {
        'title':title,
        'details':details,
        'due_date':due_date,
        'priority':priority,
        'interval':
        {
            'interval':interval,
            'prev_date':CURRENT_DATE,
            'status': 'up'
        }
    }
    # Validate inputs
    if title:
        print("Task title cannot be empty.")
        return

    if not is_valid_priority(priority):
        print("Priority must be 'High', 'Mid', or 'Low'.")
        return
    
    if not is_valid_due_date(due_date) and due_date:
        print("Due date must be in YYYY/MM/DD format.")
        return
    
    if not due_date:
        task['due_date'] = None

    if not interval:
        task['interval']['interval'] = None

    save_new_task(task,goal)

    manager.stop()

def new_task():
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(
                "",

                ptg.InputField(prompt="Goal:", label="Goal"),
                ptg.InputField(prompt="Title:", label="Title"),
                ptg.InputField(prompt="Description:", label="Description"),
                ptg.InputField(prompt="Due Date(leave empty for recurring tasks):", label="Due Date"),
                ptg.InputField(prompt="Priority(High, Mid, Low):", label="Priority"),
                ptg.InputField(prompt="Interval(leave empty for normal tasks):", label="Interval"),
                "" ,
                ["Submit", lambda *_: submit_task(manager, window)],
                    width=60,
                    box="DOUBLE",
                )
            .set_title("[210 bold]New Task")
            .center()
        )
        manager.add(window)
        display_task_list(manager)
        manager.bind("<Up>", lambda *_: manager.focus_previous())
        manager.bind("<Down>", lambda *_: manager.focus_next())



def display_task_list(manager: ptg.WindowManager):
    save = load_save()
    tasks = save['goals']['all']['tasks']
    
    # Create a display string for the tasks
    if tasks:
        task_display = "\n".join([f"- {task['title']} (Priority: {task['priority']})" for task in tasks])
    else:
        task_display = "No tasks available."

    # Create the task list window
    task_list_window = ptg.Window(
        "Task List",
        ptg.Label(task_display),  
        box="DOUBLE",
        width=60,
    )
    
    manager.add(task_list_window)

    
new_task()