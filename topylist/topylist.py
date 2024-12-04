import os
import datetime
import argparse
import json
PATH = 'topylist/saves'

argparser= argparse.ArgumentParser(description='A simple todo list program')

def load_todos():
    with open(PATH + '/save.txt','r') as f:
        return json.load(f)

def init_saves():
    os.makedirs(PATH,exist_ok=True)
    data = {
        'tasks': {'todo': [], 'done': []},
        'name': input('whats your name?'),
        'tasks_done': 0
    }
    with open(PATH +'/saves.json','w') as f:
        json.dump(data,f)

def write_todo(saves,task,title):
    save =saves
    if any(task['title'] == title for task in saves['tasks']['todo']):
        print('Already a task with that title')
        return
    save['tasks']['todo'].append({'title':title, 'details':task,'date':datetime.date.today()})
    with open(PATH + '/save.txt','w') as f:
        json.dump(save,f)


def finish_task(saves,task_title):
    save =saves
    for task_id, tasks in enumerate(saves['tasks']['todo']):
        if tasks['title'] == task_title:
            task = save['tasks']['todo'][task_id]
            del(save['tasks']['todo'][task_id])
            break
    else:
        print('No task with title: '+task_title)
        return
    save['tasks']['done'].append(task)
    save['tasks_done'] += 1 
    with open(PATH + '/save.txt','w') as f:
        json.dump(save,f)
def clear_finished_tasks(saves):
    save =saves
    save['tasks_done'] = 0
    save['tasks']['done'] = []
    with open(PATH + '/save.txt','w') as f:
        json.dump(save,f)
def main():
    if not os.path.exists('topylist/saves/save.txt'):  
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
        write_todo(saves,description,title)
    elif args.list:
        print_off_tasks_todo(saves)
    elif args.list_finished:
        print_off_tasks_done(saves)
    elif args.finish:
        finish_task(saves,task_title=input("Task title you finished: "))
    elif args.reset:
        init_saves()
if __name__ == '__main__':
    main()
