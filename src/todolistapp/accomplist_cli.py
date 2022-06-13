"""new file to experiment with creating a CLI app with typer, rich, and sqlite3
created with the help of the YouTube video: https://youtu.be/ynd67UwG_cI"""

# pylint: disable=E0401

import typer
from rich.console import Console
import task_model
from task import Task as t
from task import TaskLists as tl

console = Console()

app = typer.Typer()


@app.command(short_help="Adds a task to the task database")
def create(task_name: str = typer.Option(default=None, prompt="Enter Task Name", prompt_required=True),
           task_description: str = typer.Option(default=None, prompt="Enter Task details", prompt_required=True),
           start_date: str = typer.Option(default=None, prompt="Enter Start Date", prompt_required=True),
           due_date: str = typer.Option(default=None, prompt="Enter Due Date", prompt_required=True)):
    """
    Placeholder text
    :param task_name:
    :param task_description:
    :param start_date:
    :param due_date:
    :return:
    """
    t.add_task(task_name, task_description, start_date, due_date)
    typer.secho(f"Added, '{task_name},' to the list.", fg=typer.colors.BRIGHT_CYAN)


@app.command(help="Mark a task, 'Completed'")
def complete(task_name: str = typer.Option(default=None,
                                           prompt="Enter exact Task Name to mark, 'Complete'",
                                           prompt_required=True)):
    """
    Placeholder text
    :param task_name:
    :return:
    """
    t.complete_task(task_name)
    typer.secho(f"Congrats on completing: {task_name}", fg=typer.colors.BRIGHT_GREEN)


@app.command(help="Marks task in the database as, 'Deleted'")
def delete(task_name: str = typer.Option(default=None,
                                         prompt="Task name to delete",
                                         help="Exact name of the task to be deleted")):
    """
    Placeholder text
    :param task_name:
    :return:
    """
    t.delete_task(task_name)
    typer.secho(f"Deleted {task_name}.", fg=typer.colors.RED)


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
    Placeholder text
    :param task_name:
    :param task_details:
    :param start_date:
    :param due_date:
    :return:
    """
    t.update_task(task_name, task_details, start_date, due_date)
    typer.secho(f"Updated Original Task Name: {task_name}...", fg=typer.colors.YELLOW)


@app.command(short_help="Creates a table of all existing database contents")
def print_all_tasks():
    """
    Placeholder text
    :return:
    """
    tl.database_report()
    typer.secho(f"Report complete!", fg=typer.colors.BRIGHT_BLUE)
    # return True


@app.command(short_help="List tasks sorted by Task ID")
def list_ids(choice: str = typer.Option(default=None,
                                        prompt="Enter 1 for Ascending or 2 for Descending",
                                        prompt_required=True)):
    """
    Placeholder text
    :param choice:
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
    Placeholder text
    :return:
    """
    tl.task_list_overdue_sort()


if __name__ == '__main__':
    # connect to database
    task_model.main_task_database()

    app()
