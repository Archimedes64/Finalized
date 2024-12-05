import topylist as tpl


def main():
    tpl.has_saves()

    while True:
        saves = tpl.load_todos()
        tpl.tasks_screen()
        user_input = input(":")
        if user_input == 'exit':
            print('Goodbye')
            break
        elif user_input == 'add':
            tpl.clear_screen()
            tpl.console.print("[bold red]Add[/bold red]")
            tpl.write_todo(input(" Title: "),input(" Description: "),input(' Due Date MM/DD: '))
        elif user_input == 'finish':
            tpl.clear_screen()
            tpl.console.print('[bold red]Finish[/bold red]\n [green]Tasks:[/green]')
            tpl.Finish_Mode()
            tpl.finish_task(input('Task Tile:'))
        else:
            print("Invalid input")
main()