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
        print('Let\'s gather details about your task.')
        task_name = input('Enter a Task name (e.g., Resolve script error): ')
        task_details = input('Task description (e.g., Use pysnooper on pesky function): ')
        start_date = input('Task start date (e.g., MM/DD/YYYY): ')
        due_date = input('Task due date (e.g., MM/DD/YYYY): ')
        if not t.add_task(task_name, task_details, start_date, due_date):
            print("An error occurred while trying to add a new task.")
        else:
            print("Task added successfully.")
    except ValueError:
        print("The date(s) cannot resemble the chaos you entered.")


def update_task():
    """
    Modifies the details of an existing task
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
    """
    Marks a task in the database as completed
    """
    task_name = input('Task name: ')
    if not t.complete_task(task_name):
        print("An error occurred while trying to mark task, 'Complete'.")
    else:
        print("Task completed!")


def list_task_options():
    """
    Basic menu for a user to select various list format options
    """
    submenu_options = {
        'a': task_id_list,
        'b': priority_task_list,
        'c': due_date_list,
        'd': closed_tasks_date_query,
        'e': overdue_tasks,
    }

    while True:
        user_choice = input("""
        Select a List view of your Tasks:
                            a) Tasks by Task ID
                            b) Tasks by Priority
                            c) Open Tasks by Date
                            d) Closed Tasks in Date Range
                            e) Overdue Tasks
                            f) Return to Main Menu
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
    while True:
        try:
            choice = input('Enter 1 or 2: ').strip()
            if not tl.task_list_id_sort(choice):
                print("An error occurred while trying to compile this list.")
            else:
                print('List generated!')
        except Exception as e:
            logger.info(e)


def priority_task_list():
    print("Tasks sort by Priority:")
    if not tl.task_list_priority_sort():
        print("An error occurred while trying to compile list")
    else:
        print('Priority list generated!')


# List all open tasks sorted by due date
def due_date_list():
    """
    Outputs a simple menu and table of open tasks sorted in ascending or descending order
    """
    print("Open Tasks sorted by Due Date")
    print("""
                        1 -- Oldest to Newest
                        2 -- Newest to Oldest
    """)
    while True:
        try:
            choice = input('Enter 1 or 2: ').strip()
            if not tl.task_list_open_sort(choice):
                print("An error occurred while trying to compile this list.")
            else:
                print('List generated!')
        except Exception as e:
            logger.info(e)


def closed_tasks_date_query():
    """
    Gets user input for dates and passes them to a function that filters tasks within that date range
    """
    try:
        date_1 = input("Enter first (oldest) date in range: ")
        date_2 = input("Enter second (newest) date in range: ")
        tl.task_list_completed_sort(date_1, date_2)
    except Exception as e:
        logger.info(e)


def overdue_tasks():
    """
    Outputs a table containing overdue tasks.
    """
    print("Here are the Overdue Tasks:")
    try:
        if not tl.task_list_overdue_sort():
            print("An error occurred while trying to compile this list.")
        else:
            print('List generated!')
    except Exception as e:
        logger.info(e)


def generate_task_report():
    """
    Outputs a table containing all database contents, including those marked as 'Deleted.'
    """
    print("Here is the record of All your AccompList Tasks:")
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
        'C': complete_task,
        'D': delete_task,
        'E': list_task_options,
        'F': generate_task_report,
        'Q': quit_program
    }

    # print menu of options to user
    print("Welcome to AccompList!"
          "\nLet us curate a List of tasks you will to Accomplish. ")
    while True:
        user_selection = input("""
                                A: Add a task
                                B: Update a task
                                C: Complete a task
                                D: Delete a task
                                E: List tasks
                                F: Generate a task report
                                Q: Quit
                                Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option. Try again.")
