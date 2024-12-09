import topylist as tpl

def get_due_date() -> str:
    while True:    
        date = input(' Due Date YYYY/MM/DD: ')
        list(date)
        print(len(date))
        if len(date) == 10:
            if date[4] == '/' and date[7] == '/':
                if int(date[5:7]) < 12:
                    if int(date[:4] >= 2024):
                        break
            

        print('Not a valid date')
    return "".join(date)
def main():
    tpl.has_saves()
    goal = 'all'
    while True:
        saves = tpl.load_todos()
        tpl.tasks_screen(goal)
        user_input = input("\n:")
        if user_input == 'exit':
            print('Goodbye')
            break
        elif user_input == 'add':
            tpl.clear_screen()
            tpl.console.print("[bold red]Add[/bold red]")
            while True:    
                user_input_add = input("What do you want to add?\n  Goal = 1\n  Task = 2\n  subtask = 3\n\n: ")
                if user_input_add not in ['1','2','3']:
                    print("Not a valid input please enter a number 1-3")
                break
            if user_input_add == "1":
                tpl.add_goal()
            elif user_input_add == "2":
                tpl.write_todo(get_due_date())
        elif user_input == 'finish':
            tpl.clear_screen()
            tpl.console.print('[bold red]Finish[/bold red]\n [green]Tasks:[/green]')
            tpl.Finish_Mode(goal)
            tpl.finish_task(input('Task Tile:'))
        elif any(task['title'] == user_input for task in saves['goals'][goal]['tasks']['todo']):
                tpl.clear_screen()
        elif user_input.lower() in list(saves['goals']):
            goal = user_input.lower()
        else:
            
            print("Invalid input")
main()