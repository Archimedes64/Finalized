import logic as l

def get_due_date() -> str:
    date = input(' Due Date YYYY/MM/DD: ')
    list(date)
    while True:    
        date = input(' Due Date YYYY/MM/DD: ')
        list(date)
        print(int(date[5:7]))
        print(int(date[:4]))

        if len(date) != 10:
            continue

        if date[4] == '/' and date[7] == '/':
            continue

        if int(date[5:7]) < 12:
            continue
        
        if int(date[:4] >= 2024):
            break
    return "".join(date)
def main():
    l.has_saves()
    goal = 'all'
    while True:
        saves = l.load_todos()
        l.tasks_screen(goal)
        user_input = input("\n:")
        if user_input == 'exit':
            print('Goodbye')
            break
        elif user_input == 'add':
            l.clear_screen()
            l.console.print("[bold red]Add[/bold red]")
            while True:    
                user_input_add = input("What do you want to add?\n  Goal = 1\n  Task = 2\n  subtask = 3\n\n: ")
                if user_input_add not in ['1','2','3']:
                    print("Not a valid input please enter a number 1-3")
                break
            if user_input_add == "1":
                l.add_goal()
            elif user_input_add == "2":
                l.write_todo(get_due_date())
        elif user_input == 'finish':
            l.clear_screen()
            l.console.print('[bold red]Finish[/bold red]\n [green]Tasks:[/green]')
            l.Finish_Mode(goal)
            l.finish_task(input('Task Tile:'))
        elif any(task['title'] == user_input for task in saves['goals'][goal]['tasks']['todo']):
                l.clear_screen()
        elif user_input.lower() in list(saves['goals']):
            goal = user_input.lower()
        else:
            
            print("Invalid input")
main()