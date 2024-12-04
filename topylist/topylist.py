import os
import datetime
PATH = 'topylist/saves'



def load_todos():
    
    with open(PATH + '/save.txt','r') as f:
        info = f.read()
        data = eval(info)
    return data
    pass

def init_saves():
    os.makedirs(PATH,exist_ok=True)
    f = open(PATH+'/save.txt','w')
    name = input("What is your name: ")
    f.write(str({ 'tasks' : {'todo':[],'done':[]} ,'name':name,'tasks_done':0}))
    f.close()

def write_todo(saves,task,title):
    save =saves
    save['tasks']['todo'].append({'title':title, 'details':task,'date':datetime.date.today()})
    with open(PATH + '/save.txt','w') as f:
        f.write(str(saves))
def print_off_tasks_todo(saves):
    for task in saves['tasks']['todo']:
        print(task['details'])
def finish_task(saves,task_title):
    save =saves
    for task_id, tasks in enumerate(saves['tasks']['todo']):
        if tasks['title'] == task_title:
            task = save['tasks']['todo'][task_id]
            del(save['tasks']['todo'][task_id])
            break
    else:
        print('No task with that name')
        return
    save['tasks']['done'].append(task)
    save['tasks_done'] += 1 
    with open(PATH + '/save.txt','w') as f:
        f.write(str(saves))

def main():
    if not os.path.exists('topylist/saves/save.txt'):  
        init_saves()
    saves = load_todos()
    print(saves)
    
    #write_todo(saves,'this is a task','task')
    saves = load_todos()
    #finish_task(saves,'task')
    print_off_tasks_todo(saves)
if __name__ == '__main__':
    main()
