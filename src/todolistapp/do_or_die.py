"""
Title: Do or Die
Description: A script that uses Typer to make a CLI To Do List app
Helpful Resources: Typer Documentation and https://youtu.be/ynd67UwG_cI
Author: BBurdelsky
"""

# pylint: disable=E0401

import typer
from rich.console import Console
import requests
import todolistapp.task_model as tm
from task import Task as t
from task import TaskLists as tl

console = Console()

app = typer.Typer(help=("--Do Or Die--" + "\nYour Tasks Are Nigh"))


@app.command(short_help="Adds a task to the task database")
def create(task_name: str = typer.Option(default=None, prompt="Enter Task Name", prompt_required=True),
           task_description: str = typer.Option(default=None, prompt="Enter Task details", prompt_required=True),
           start_date: str = typer.Option(default=None, prompt="Enter Start Date", prompt_required=True),
           due_date: str = typer.Option(default=None, prompt="Enter Due Date", prompt_required=True)):
    """
    Adds a task to a database
    :param task_name: (string)
    :param task_description: (string)
    :param start_date: (string)
    :param due_date: (string)
    :return:
    """
    t.add_task(task_name, task_description, start_date, due_date)
    typer.secho(f"Added, '{task_name},' to the list.", fg=typer.colors.BRIGHT_CYAN)


@app.command(help="Mark a task, 'Completed'")
def complete(task_name: str = typer.Option(default=None,
                                           prompt="Enter exact Task Name to mark, 'Complete'",
                                           prompt_required=True)):
    """
    Completes a task in a database by using the function 'complete_task' from file task.py
    :param task_name: (string) name of task
    :return:
    """
    t.complete_task(task_name)
    typer.secho(f"{task_name} -- LAID TO REST", fg=typer.colors.BRIGHT_GREEN)
    typer.secho("""                                                                                                                     
                                                  .;*+?##S%%%SS##?+;                                                    
                                              *?#S%%%@@@@@@@@@@@@@@@%S#+.                                               
                                           *?S%%%%%@@@@@@@@@@@@@@@@@@@@@%S?.                                            
                                         +#%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@%#;                                          
                                       ,?SS%%%%%%%@%@@@@@@@@@@@@@@@@@@@@@@@@@%#.                                        
                                      .?#?S%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@S.                                       
                                      *#S??SSS##S#S##############SS%%%%@@@@@@@%%+                                       
                                      +#S#?#%####S%%%%SS##??#?##S%%%%%@@@@@@@%%%?                                       
                                     .?#S#??%%%%%%S##SSSSS####SSS%%%%%@@@@@@%%%%#                                       
                                     .?####%%%%S#+*.,;;*+???????++,,**?S%@@@%%%%#                                       
                                      +???##+;.      .,;*;;++**?+,       ,*?%%%%+                                       
                                      +++??            ,**+S%#++,           +%%S,                                       
                                      *++??*           ;??S%%%S?*          ;%%%#                                        
                                      .???##+;.....,*+??#?+;*S%%S??+*,.;*,+#%%%?.                                       
                                      .?####?+++++*+++??+.   ,?S#????????##S%%%S*                                       
                                       ,?#?+*;,,,..;*++.       ,??+*. .,*++#SS#,                                        
                                        .*+;,,,*+*;*?#?*,.;;. ,*#%#?**;;+;,+?#,                                         
                                         .,     *###%%?#?#?######@%S#?,,+. .;;                                          
                                                ,?##SS#S?#??#%#%S%%%S?                                                  
                                                .*++?##%##%?S%?%#S?##+                                                  
                                                  ,,,*++**+**++++*;;  

                                                          RIP
                                                  """, fg=typer.colors.BRIGHT_BLACK)


@app.command(help="Marks task in the database as, 'Deleted'")
def delete(task_name: str = typer.Option(default=None,
                                         prompt="Task name to delete",
                                         help="Exact name of the task to be deleted"),
           force: bool = typer.Option(default=True,
                                      prompt="Are you sure you want to delete this task? [y/n]")):
    """
    Changes the status of a task in the database from 'In Progress' (the default) to Deleted'.
    :param force: a CLI option, if not provided, is prompted (see Typer documentation)
    :param task_name: (string) exact string of the task name
    :return:
    """
    if force:
        t.delete_task(task_name)
        typer.secho(f"Sent -- {task_name} -- to OBLIVION.", fg=typer.colors.RED)
    else:
        typer.secho("Operation canceled.", fg=typer.colors.RED)


@app.command(short_help="Updates a task in the task database")
def update(task_name: str = typer.Option(default=None,
                                         prompt="Enter Updated Task Name",
                                         prompt_required=True),
           task_details: str = typer.Option(default=None,
                                            prompt="Enter Updated Task details",
                                            prompt_required=True),
           start_date: str = typer.Option(default=None,
                                          prompt="Enter Same Start Date or Update it",
                                          prompt_required=True),
           due_date: str = typer.Option(default=None,
                                        prompt="Enter Same Due Date or Update it",
                                        prompt_required=True)):
    """
    Updates a task in the database with new value (if the user wishes) for each parameter.
    :param task_name: (string)
    :param task_details: (string)
    :param start_date: (string)
    :param due_date: (string)
    :return:
    """
    t.update_task(task_name, task_details, start_date, due_date)
    typer.secho(f"Updated Original Task Name: {task_name}...", fg=typer.colors.YELLOW)


@app.command(short_help="Creates a table of all existing database contents")
def see_all_tasks():
    """
    Outputs all tasks in the database to the user. This includes deleted tasks as well.
    :return:
    """
    typer.secho("""                                                                                                                     
                                                  .;*+?##S%%%SS##?+;                                                    
                                              *?#S%%%@@@@@@@@@@@@@@@%S#+.                                               
                                           *?S%%%%%@@@@@@@@@@@@@@@@@@@@@%S?.                                            
                                         +#%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@%#;                                          
                                       ,?SS%%%%%%%@%@@@@@@@@@@@@@@@@@@@@@@@@@%#.                                        
                                      .?#?S%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@S.                                       
                                      *#S??SSS##S#S##############SS%%%%@@@@@@@%%+                                       
                                      +#S#?#%####S%%%%SS##??#?##S%%%%%@@@@@@@%%%?                                       
                                     .?#S#??%%%%%%S##SSSSS####SSS%%%%%@@@@@@%%%%#                                       
                                     .?####%%%%S#+*.,;;*+???????++,,**?S%@@@%%%%#                                       
                                      +???##+;.      .,;*;;++**?+,       ,*?%%%%+                                       
                                      +++??            ,**+S%#++,           +%%S,                                       
                                      *++??*           ;??S%%%S?*          ;%%%#                                        
                                      .???##+;.....,*+??#?+;*S%%S??+*,.;*,+#%%%?.                                       
                                      .?####?+++++*+++??+.   ,?S#????????##S%%%S*                                       
                                       ,?#?+*;,,,..;*++.       ,??+*. .,*++#SS#,                                        
                                        .*+;,,,*+*;*?#?*,.;;. ,*#%#?**;;+;,+?#,                                         
                                         .,     *###%%?#?#?######@%S#?,,+. .;;                                          
                                                ,?##SS#S?#??#%#%S%%%S?                                                  
                                                .*++?##%##%?S%?%#S?##+                                                  
                                                  ,,,*++**+**++++*;;  
                                                  
                                                  TIME TO DO! ...OR DIE
                                                  """, fg=typer.colors.BRIGHT_BLACK)
    tl.database_report()
    typer.secho(f"Report complete!", fg=typer.colors.BRIGHT_BLUE)
    # return True


@app.command(short_help="List tasks sorted by Task ID")
def list_ids(choice: str = typer.Option(default=None,
                                        prompt="Enter 1 for Ascending or 2 for Descending",
                                        prompt_required=True)):
    """
    Outputs a table to the user showing all tasks sorted by task idea. User has the option to see the table
    sorted by ascending or descending task id order.
    :param choice: (string) of a number representing a choice
    :return:
    """
    tl.task_list_id_sort(choice)


@app.command(short_help="List tasks by priority")
def list_priority():
    """
    Placeholder text
    :return:
    """
    tl.task_list_priority_sort()


@app.command(short_help="List incomplete tasks")
def list_open(choice: str =
              typer.Option(default=None,
                           prompt="Enter 1 for Oldest to Newest or 2 for Newest to Oldest",
                           prompt_required=True)):
    """
    Placeholder text
    :param choice:
    :return:
    """
    tl.task_list_open_sort(choice)


@app.command(short_help="List completed tasks in a date range")
def list_between(date_1: str = typer.Option(default=None,
                                            prompt="Enter older date",
                                            prompt_required=True),
                 date_2: str = typer.Option(default=None,
                                            prompt="Enter newer date",
                                            prompt_required=True)):
    """
    Placeholder text
    :param date_1:
    :param date_2:
    :return:
    """
    tl.task_list_completed_sort(date_1, date_2)


@app.command(short_help="List all overdue tasks.")
def list_overdue():
    """
    Presents a list of overdue tasks to the user
    :return:
    """
    tl.task_list_overdue_sort()
    typer.secho("""                                                                                                                     
                                                  .;*+?##S%%%SS##?+;                                                    
                                              *?#S%%%@@@@@@@@@@@@@@@%S#+.                                               
                                           *?S%%%%%@@@@@@@@@@@@@@@@@@@@@%S?.                                            
                                         +#%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@%#;                                          
                                       ,?SS%%%%%%%@%@@@@@@@@@@@@@@@@@@@@@@@@@%#.                                        
                                      .?#?S%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@S.                                       
                                      *#S??SSS##S#S##############SS%%%%@@@@@@@%%+                                       
                                      +#S#?#%####S%%%%SS##??#?##S%%%%%@@@@@@@%%%?                                       
                                     .?#S#??%%%%%%S##SSSSS####SSS%%%%%@@@@@@%%%%#                                       
                                     .?####%%%%S#+*.,;;*+???????++,,**?S%@@@%%%%#                                       
                                      +???##+;.      .,;*;;++**?+,       ,*?%%%%+                                       
                                      +++??            ,**+S%#++,           +%%S,                                       
                                      *++??*           ;??S%%%S?*          ;%%%#                                        
                                      .???##+;.....,*+??#?+;*S%%S??+*,.;*,+#%%%?.                                       
                                      .?####?+++++*+++??+.   ,?S#????????##S%%%S*                                       
                                       ,?#?+*;,,,..;*++.       ,??+*. .,*++#SS#,                                        
                                        .*+;,,,*+*;*?#?*,.;;. ,*#%#?**;;+;,+?#,                                         
                                         .,     *###%%?#?#?######@%S#?,,+. .;;                                          
                                                ,?##SS#S?#??#%#%S%%%S?                                                  
                                                .*++?##%##%?S%?%#S?##+                                                  
                                                  ,,,*++**+**++++*;;  

                                                  TIME TO DO OR DIE
                                                  """, fg=typer.colors.BRIGHT_RED)


@app.command(short_help="get jsonified data from URL")
def get_data(enpoint: str = typer.Option(default=None, prompt="Enter /<url end>")):
    url = f"http://127.0.0.1:5000/{enpoint}"
    response = requests.get(url)
    typer.secho(f"{response.content}", fg=typer.colors.BRIGHT_CYAN)


if __name__ == '__main__':
    # connect to database
    tm.main_task_database()

    app()
