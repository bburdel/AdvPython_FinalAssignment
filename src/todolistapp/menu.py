'''
menu for options presented to user
'''

import sys
from loguru import logger
import task_model
# import main
from task import Task as t
from task import TaskLists as tl

logger.info("Logging activity from menu.py")
logger.add("out.log", backtrace=True, diagnose=True)


def load_task():
    pass


def add_task():
    """
    Adds a new task to the database

    Task status defaults to 'Not Started'
    """
    try:
        task_name = input('Task name: ')
        task_details = input('Task description: ')
        start_date = input('Task start date: ')
        due_date = input('Task due date: ')
        if not t.add_task(task_name, task_details, start_date, due_date):
            print("An error occurred while trying to add a new task.")
        else:
            print("Task added successfully.")
    except ValueError:
        print("The date cannot resemble the chaos you entered.")


def update_task():
    """

    :return:
    """
    # TODO perhaps give options for which to alter
    task_name = input('Task name: ')
    task_details = input('Task details: ')
    start_date = input('Altered task start date: ')
    due_date = input('Altered task due date: ')
    if not t.update_task(task_name, task_details, start_date, due_date):
        print(f"An error occurred while trying to update the task, '{task_name}.'")
    else:
        print(f"Task name -- {task_name} -- was successfully updated.")


def delete_task():
    """
    Marks a task in the database as task_status = deleted
    """
    task_name = input('Task name: ')
    if not t.delete_task(task_name):
        print("An error occurred while trying to delete this task.")
    else:
        print("Task deleted.")


def complete_task():
    task_name = input('Task name: ')
    if not t.complete_task(task_name):
        print("An error occurred while trying to mark task, 'Complete'.")
    else:
        print("Task completed!")


def list_task_options():
    # List all tasks sorted by task number
    # List all tasks sorted by priority
    # List all open tasks sorted by due date
    # List all closed tasks between specified dates
    # List all overdue tasks
    submenu_options = {
        'a': task_id_list,
        'b': priority_task_list,
        'c': due_date_list,
        'd': closed_tasks_date_query,
        'e': overdue_tasks,
    }

    while True:
        user_choice = input("""
                                a: Tasks by Task ID
                                b: Tasks by Priority
                                c: Open Tasks by Date
                                d: Closed Tasks in Date Range
                                e: Overdue Tasks
                                f: Return to Main Menu
                                Please enter your choice: """)
        if user_choice.lower() in submenu_options:
            submenu_options[user_choice.lower()]()
        elif user_choice.lower() == 'f':
            break
        else:
            print("Invalid option. Try again.")


def task_id_list():
    print("""
                See Task ID List Sorted in:
                1 -- Ascending order
                2 -- Descending order
    """)
    choice = input('Choice: ').strip()
    if not tl.task_list_id_sort(choice):
        print("An error occurred while trying to compile this list.")
    else:
        print('List generated!')


def priority_task_list():
    print("Tasks sort by Priority:")
    if not tl.task_list_priority_sort():
        print("An error occurred while trying to compile list")
    else:
        print('Priority list generated!')


def due_date_list():
    pass


def closed_tasks_date_query():
    pass


def overdue_tasks():
    pass


def generate_task_report():
    print("Here is the current state of your AccompList Tasks:")
    return tl.database_report()


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == '__main__':
    # connect to database
    task_model.main_task_database()

    # list of function that does the work
    menu_options = {
        'A': add_task,
        'B': update_task,
        'C': delete_task,
        'D': complete_task,
        'E': list_task_options,
        'F': generate_task_report,
        'Q': quit_program
    }

    # print menu of options to user
    while True:
        user_selection = input("""
                                A: Add a task
                                B: Update a task
                                C: Delete a task
                                D: Complete a task
                                E: List tasks
                                F: Generate a task report
                                Q: Quit
                                Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option. Try again.")
