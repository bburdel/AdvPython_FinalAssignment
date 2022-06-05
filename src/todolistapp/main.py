"""
Main driver for a to-do list platform
"""

# import task_model as tm
import task as t


def add_task(task_name, task_description, start_date, due_date):
    """
    Creates a new user database entry
    """

    new_task = t.Task.add_task(task_name, task_description, start_date, due_date)
    return new_task


def update_task(task_name, task_description, start_date, due_date):
    """
    Modifies an existing task with edited information
    """

    mod_task = t.Task.update_task(task_name, task_description, start_date, due_date)
    return mod_task


def delete_task(task_name):
    # TODO is this actually deleted a task or shifting it to another table?
    pass