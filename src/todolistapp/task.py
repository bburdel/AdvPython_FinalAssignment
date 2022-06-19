"""
Title: task.py
Description: Code containing classes that organize task details like dates and lists,
as well as manipulate those task in a SQLite3 database.
Author: BBurdelsky
Version: Python 3.10
"""

# pylint: disable=R1710

# TODO write the data to the database as all lowercase? Then string format in the tables?

import datetime as d
from datetime import datetime
from loguru import logger
import peewee as pw
from tabulate import tabulate
import typer
import pysnooper
import todolistapp.task_model as tm


class DateHelper:
    """
    A class containing functions that work with datetime objects and date strings.
    """

    @staticmethod
    def check_for_past_date(date):
        """
        This function checks a date and ensures that it is valid, i.e., it is not in the past.
        :param date: (string) date
        :return: Nothing
        """
        today = datetime.now()  # No timezone is specified but could be passed as an argument.
        past_check = datetime.strptime(date, '%m/%d/%Y')
        if past_check.date() < today.date():
            print("Invalid date. Cannot assign a task to the past.")
            return False
        else:
            # logger.info("\tDate accepted.")
            return True

    @staticmethod
    def date_conversion(date):
        """
        Gets a date and converts it to a datetime object
        :param date: 'string formatted date'
        :return: (object) datetime representation of the date with the time stripped away
        """
        if DateHelper.check_for_past_date(date):
            date_converted = d.datetime.strptime(date, '%m/%d/%Y')
            return date_converted


class Task:
    """
    Contains functions that use the peewee library to manipulate data in a sqlite database
    """

    @staticmethod
    def get_priority(start_date, due_date):
        """
        Calculates the difference between two dates.
        :param start_date: (string) a date
        :param due_date: (string) a date
        :return: (string) priority classification
        """
        start_date_converted = DateHelper.date_conversion(start_date)
        due_date_converted = DateHelper.date_conversion(due_date)

        date_delta = (due_date_converted - start_date_converted).days

        if date_delta > 7:
            priority = 'Low'
            return priority
        if 3 <= date_delta <= 7:
            priority = 'Medium'
            return priority
        if date_delta < 3:
            priority = 'High'
            return priority

    @staticmethod
    # @pysnooper.snoop(depth=1)
    def add_task(task_name, task_description, start_date, due_date):
        """
        Adds a task to a SQLite database table called Tasks
        :param task_name: (string) of task name
        :param task_description: (string) task details/description
        :param start_date: (string) date the task starts
        :param due_date: (string) date the task is due
        :return: (bool) True if a task is successfully added, False otherwise
        """
        # create a task_id automatically
        task_id = datetime.now().strftime('%Y%m%d%H%M%S')

        try:
            new_task = tm.Tasks.create(task_id=task_id, task_name=task_name,
                                       task_details=task_description,
                                       task_start_date=start_date, task_due_date=due_date,
                                       task_priority=Task.get_priority(start_date, due_date))
            new_task.save()
            return True
        except pw.IntegrityError:
            print("Peewee Integrity Error -- Cannot add this task to the database.")
            return False

    @staticmethod
    def update_task(task_name, task_details, start_date, due_date):
        """
        Modifies each parameter
        :param task_name: (string) of task name
        :param task_details: (string) task details/description
        :param start_date: (string) date the task starts
        :param due_date: (string) date the task is due
        :return: (bool) True if a task is successfully updated, False otherwise
        """
        try:
            row = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row.task_details = task_details
            row.task_start_date = start_date
            row.task_due_date = due_date
            # row.task_status = task_status
            row.save()
            return True
        except pw.DoesNotExist:
            typer.secho("Peewee Error: pw.DoesNotExist", fg=typer.colors.BRIGHT_YELLOW)
            # logger.info("")
            return False

    @staticmethod
    def delete_task(task_name):
        """
        Marks the status column of a task as 'Deleted.'
        :param task_name: (string) name of task
        :return: (bool)
        """
        try:
            row_query = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Deleted'
            row_query.save()
            # logger.info(f'Task name: {task_name} -- marked as deleted.')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not modify task with name, "{task_name}," as it was not found.')
            return False

    @staticmethod
    def complete_task(task_name):
        """
        Marks the status column of a task as 'Completed.'
        :param task_name: (string) name of task
        :return: (bool)
        """
        try:
            row_query = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Completed'
            row_query.task_complete_date = datetime.now().strftime('%m/%d/%Y')
            row_query.save()
            logger.info(f'Task name: {task_name} -- is Complete!')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not modify task with name, "{task_name}," as it was not found.')
            return False


class TaskLists:
    """
    Curates functions relating to organizing tasks into lists
    """

    @staticmethod
    def print_any_list_choice(query_results):
        """
        Organizes data in a dictionary into a table using the 'tabulate' module
        :param query_results:
        :return:
        """
        formatted_list = []
        for row in query_results:
            task_id = row['task_id']
            task_name = row['task_name']
            task_details = row['task_details']
            task_start_date = row['task_start_date']
            task_due_date = row['task_due_date']
            task_complete_date = row['task_complete_date']
            task_priority = row['task_priority']
            task_status = row['task_status']
            formatted_content = [task_id, task_name, task_details, task_start_date,
                                 task_due_date, task_complete_date, task_priority, task_status]
            formatted_list.append(formatted_content)
        colored_table = tabulate(formatted_list, headers=['Task ID', 'Name', 'Details',
                                                          'Start Date', 'Due Date',
                                                          'Completed On', 'Priority', 'Status'],
                                 tablefmt='fancy_grid')
        typer.secho(f"{colored_table}", fg=typer.colors.BRIGHT_BLACK)

    @staticmethod
    def database_report():
        """

        :return:
        """
        query = tm.Tasks.select().dicts()
        formatted_list = []
        for row in query:
            task_id = row['task_id']
            task_name = row['task_name']
            task_details = row['task_details']
            task_start_date = row['task_start_date']
            task_due_date = row['task_due_date']
            task_complete_date = row['task_complete_date']
            task_priority = row['task_priority']
            task_status = row['task_status']
            formatted_content = [task_id, task_name, task_details, task_start_date,
                                 task_due_date, task_complete_date, task_priority, task_status]
            formatted_list.append(formatted_content)
        print(tabulate(formatted_list, headers=['Task ID', 'Name', 'Details',
                                                'Start Date', 'Due Date',
                                                'Completed On', 'Priority', 'Status'],
                       tablefmt='fancy_grid'))  # 'github' --> for markdown

    # List all tasks sorted by task number
    @staticmethod
    def task_list_id_sort(choice):
        """

        :param choice:
        :return:
        """
        list_of_dicts = []
        try:
            if choice.strip() == '1':
                print('Task IDs in Ascending order:')
                query = tm.Tasks.select().where(tm.Tasks.task_status != 'Deleted') \
                    .order_by(+tm.Tasks.task_id)
                for result in query.dicts():
                    list_of_dicts.append(result)
                # print(list_of_dicts)
                TaskLists.print_any_list_choice(list_of_dicts)
                # string formatting instead?
            elif choice.strip() == '2':
                print('Task IDs in Descending order:')
                query = tm.Tasks.select().where(tm.Tasks.task_status != 'Deleted') \
                    .order_by(-tm.Tasks.task_id)
                query_dict = query.dicts()
                TaskLists.print_any_list_choice(query_dict)
            else:
                print('That is not a valid option.')
        except Exception as e:
            print("Something went wrong, please try again.")
            logger.info(e)

    # List all tasks sorted by priority
    @staticmethod
    def task_list_priority_sort():
        """
        Uses peewee to query SQLite database for all (non-deleted) tasks
        """
        # underline = '\033[4m'
        bullet = '\u2022'
        try:
            query = tm.Tasks.select().where(tm.Tasks.task_status != 'Deleted') \
                .order_by(tm.Tasks.task_due_date)
            # print("Prioritized Task List")
            typer.secho("Prioritized Task List", fg=typer.colors.BRIGHT_BLUE)
            for row in query:
                # print("\t" + bullet + f"Task: {row.task_name}" + f"\n\t Priority: {row.task_priority}")
                if row.task_priority == "High":
                    typer.secho("\t" + bullet + f"Task: {row.task_name}" + f"\n\t Priority: {row.task_priority}",
                                fg=typer.colors.BRIGHT_RED)
                if row.task_priority == "Medium":
                    typer.secho("\t" + bullet + f"Task: {row.task_name}" + f"\n\t Priority: {row.task_priority}",
                                fg=typer.colors.BRIGHT_YELLOW)
                if row.task_priority == "Low":
                    typer.secho("\t" + bullet + f"Task: {row.task_name}" + f"\n\t Priority: {row.task_priority}",
                                fg=typer.colors.BRIGHT_GREEN)
        except Exception as e:
            logger.info(e)

    # List all open tasks sorted by due date
    @staticmethod
    def task_list_open_sort(choice):
        """
        Uses peewee to query SQLite database for all (non-deleted tasks, incomplete) and sorts them by date.
        """
        list_of_dicts = []
        try:
            if choice.strip() == '1':
                print('Oldest to Newest Tasks:')
                query = tm.Tasks.select().where(tm.Tasks.task_status == 'In Progress') \
                    .order_by(+tm.Tasks.task_due_date)
                for result in query.dicts():
                    list_of_dicts.append(result)
                # print(list_of_dicts)
                TaskLists.print_any_list_choice(list_of_dicts)
                # string formatting instead?
            elif choice.strip() == '2':
                print('Newest to Oldest Tasks:')
                query = tm.Tasks.select().where(tm.Tasks.task_status == 'In Progress') \
                    .order_by(-tm.Tasks.task_due_date)
                query_dict = query.dicts()
                TaskLists.print_any_list_choice(query_dict)
            else:
                print('That is not a valid option.')
        except Exception as e:
            print("Something went wrong, please try again.")
            logger.info(e)

    # List all closed tasks between specified dates
    @staticmethod
    def task_list_completed_sort(date_1: str, date_2: str):
        """
        Uses peewee to query SQLite database for completed tasks that fall within a given date range
        :param date_1:
        :param date_2:
        """
        list_of_dicts = []
        query = tm.Tasks.select().where((tm.Tasks.task_status == 'Completed')
                                        & (tm.Tasks.task_due_date.between(date_1, date_2))) \
            .order_by(tm.Tasks.task_complete_date)
        for result in query.dicts():
            list_of_dicts.append(result)
        TaskLists.print_any_list_choice(list_of_dicts)

    # List all overdue tasks
    @staticmethod
    # @pysnooper.snoop(depth=2)
    def task_list_overdue_sort():
        """
        Uses peewee to query SQLite database for overdue tasks
        """
        list_of_dicts = []
        today = datetime.now().date().strftime('%m/%d/%Y')
        query = tm.Tasks.select().where((tm.Tasks.task_status == 'In Progress')
                                        & (tm.Tasks.task_due_date <= today))\
            .order_by(+tm.Tasks.task_due_date)
        try:
            for result in query.dicts():
                list_of_dicts.append(result)
        except StopIteration:
            logger.info("StopIteration triggered.")
        TaskLists.print_any_list_choice(list_of_dicts)
