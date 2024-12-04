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
    for task in saves['tasks']['todo']:
        if task['title'] == title:
            print("Already a task with title: " + title)
            return
    save['tasks']['todo'].append({'title':title, 'details':task,'date':datetime.date.today()})
    with open(PATH + '/save.txt','w') as f:
        f.write(str(saves))
def print_off_tasks_todo(saves):
    for task in saves['tasks']['todo']:
        #sorry future me for how unreadable. makes date obj a str then spliting to seperate the ymds takes away year
        print(f'{task['title']}: {"-".join(str(task['date']).split('-')[1:3])}\n   {task['details']}')
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
        f.write(str(saves))
def clear_finished_tasks(saves):
    save =saves
    save['tasks_done'] = 0
    save['tasks']['done'] = []
    with open(PATH + '/save.txt','w') as f:
        f.write(str(saves))
def main():
    if not os.path.exists('topylist/saves/save.txt'):  
        init_saves()
    saves = load_todos()

    #write_todo(saves,'just live another day','live')
    write_todo(saves,'eat dinner today','eat')
    saves = load_todos()
    finish_task(saves,'live')
    print_off_tasks_todo(saves)
    clear_finished_tasks(saves)
if __name__ == '__main__':
    main()
