import logic as l
import argparse

def main():

    parser = argparse.ArgumentParser(prog='Finalized',description='Todo list')

    parser.add_argument('-at',action='store_true')
    parser.add_argument('-ag',action='store_true')
    parser.add_argument('-f',action='store_true')
    parser.add_argument('-l',action='store_true')
    parser.add_argument('-g',action='store_true')

    args = parser.parse_args()

    if args.at:
        l.write_todo()
    elif args.ag:
        l.add_goal()
    elif args.f:
        l.finish_mode_no_info('all')
    elif args.l:
        l.list_up_tasks('all')
    elif args.g:
        l.get_amount_of_tasks_todo('all')
    else:
        tui()
    
def tui():
    l.has_saves()
    goal = 'all'
    sort_type = ('due_date',True)
    while True:
        saves = l.load_save()
        mode = 'compact'
        l.update_pending_tasks()
        l.tasks_screen(goal=goal,sort_type=sort_type,mode= mode)
        user_input = input("\n:")
        
        if user_input == 'exit':
            print('Goodbye')
            break
        
        elif user_input == 'add':
            l.clear_screen()
            l.console.print("[bold red]Add[/bold red]")
            
            while True:    
                user_input_add = input("What do you want to add?\n  Goal = 1\n  Task = 2\n  Subtask = 3\n\n: ")
                if user_input_add not in ['1','2','3']:
                    print("Not a valid input please enter a number 1-3")
                break
            if user_input_add == "1":
                l.add_goal()
            
            elif user_input_add == "2":
                l.write_todo()
        
        elif user_input == 'finish':
            l.Finish_Mode(goal)
                    
        elif any(task['title'] == user_input for task in saves['goals'][goal]['tasks']):
                l.clear_screen()
        elif user_input == "sort":
            
            while True:    
                user_input_sort = input("sort type:\n1 = Due Date\n2 = Priority\n:")
                if user_input_sort not in ['1','2']:
                    print("Not a valid input please enter a number 1-2")
                break

            if user_input_sort == '1':
                sorter = 'due_date'
            elif user_input_sort == '2':
                sorter = 'priority'
            reverse = l.get_user_confirmation("Low to High?")
            sort_type = (sorter,reverse)
        elif user_input == "compact":
            mode = 'compact'
        elif user_input == 'expand':
            mode = 'expand'
        elif user_input.lower() in list(saves['goals']): 

            goal = user_input.lower()
        else:
            
            print("Invalid input")
if __name__ == "__main__":
    main()
