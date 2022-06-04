'''
menu for options presented to user
'''


import sys
from loguru import logger


logger.info("Logging activity from menu.py")
logger.add("out.log", backtrace=True, diagnose=True)

def load_task():
    pass

def add_task():
    pass

def update_task():
    pass

def delete_task():
    pass

def complete_task():
    pass

def list_task_options():
    pass

def generate_task_report():
    pass

def quit_program():
    """
    Quits program
    """
    sys.exit()

if __name__ == '__main__':
    # connect to database
    # snm.main_social_network()

    # list of function that does the work
    menu_options = {
        'A': add_task,
        'B': update_task
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