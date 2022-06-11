"""new file to experiment with creating a CLI app with typer, rich, and sqlite3
created with the help of the youtube video: https://youtu.be/ynd67UwG_cI"""

import typer
from rich.console import Console
# from rich.table import Table
import task_model
from task import Task as t
from task import TaskLists as tl

console = Console()

app = typer.Typer()


@app.command(short_help="Adds a task to the task database.")
# def add(task_name, task_details, task_start_date,
# task_due_date, task_complete_date, task_priority):
#     typer.echo(f"Adding {task_name} with {task_priority} priority to the list.")
def add_task(task_name: str, task_description: str, start_date: str, due_date: str):
    typer.echo(f"Adding, '{task_name}'to the list.")
    t.add_task(task_name, task_description, start_date, due_date)



@app.command(short_help="Updates a task to the task database.")
def update(task_name, task_details, task_start_date, task_due_date, task_complete_date, task_priority):
    typer.echo(f"Updating {task_name}...")


@app.command(help="Deletes a task to the task database.")
def delete(task_name, task_details, task_start_date, task_due_date, task_complete_date, task_priority):
    typer.echo(f"Deleting {task_name}...")


@app.command(short_help="Creates a table of the task database contents.")
def print_all_tasks():
    tl.database_report()
    # return True


if __name__ == '__main__':
    # connect to database
    task_model.main_task_database()

    app()
