import logic as l
import argparse
import toml

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
            l.Add_Mode()
        
        elif user_input == 'finish':
            l.Finish_Mode(goal)
                    
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
