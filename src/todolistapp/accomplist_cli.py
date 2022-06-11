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


@app.command(short_help="Adds a task to the task database")
def create(task_name: str, task_description: str, start_date: str, due_date: str):
    t.add_task(task_name, task_description, start_date, due_date)
    typer.secho(f"Adding, '{task_name}'to the list.", fg=typer.colors.BRIGHT_CYAN)


@app.command(short_help="Updates a task in the task database")
def update(task_name: str, task_details: str, start_date: str, due_date: str):
    t.update_task(task_name, task_details, start_date, due_date)
    typer.secho(f"Updating {task_name}...")


@app.command(help="Marks as task in the database as, 'Deleted'")
def delete(task_name: str = typer.Option("Task name to delete: ",
                                         help="Exact name of the task to be deleted")):
    t.delete_task(task_name)
    typer.echo(f"Deleting {task_name}...")


@app.command(short_help="Creates a table of all existing database contents")
def print_all_tasks():
    tl.database_report()
    # return True


@app.command(short_help="List of the tasks sorted by Task ID")
def list_ids(choice: str = typer.Option(default="1", prompt="Enter 1 for Ascending or 2 for Descending: ", prompt_required=True)):
    tl.task_list_id_sort(choice)


if __name__ == '__main__':
    # connect to database
    task_model.main_task_database()

    app()
