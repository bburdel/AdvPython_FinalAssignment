'''
task related functions
'''

import datetime as d
from datetime import datetime
from loguru import logger
import peewee as pw
import task_model as tm
from tabulate import tabulate


class DateHelper:

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
            print("\tDate accepted.")
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
    Placeholder text about the task class
    """

    @staticmethod
    def get_priority(start_date, due_date):
        """
        Calculates the difference between two dates.
        :param start_date:
        :param due_date:
        :return:
        """
        start_date_converted = DateHelper.date_conversion(start_date)
        due_date_converted = DateHelper.date_conversion(due_date)

        date_delta = (due_date_converted - start_date_converted).days

        if date_delta > 7:
            priority = 'Low'
        if 7 <= date_delta >= 3:
            priority = 'Medium'
        if date_delta <= 2:
            priority = 'High'
        return priority

    @staticmethod
    def add_task(task_name, task_description, start_date, due_date):
        # create a task_id automatically
        task_id = datetime.now().strftime('%Y%m%d%H%M%S')

        try:
            new_task = tm.Tasks.create(task_id=task_id, task_name=task_name, task_details=task_description,
                                       task_start_date=start_date, task_due_date=due_date,
                                       task_priority=Task.get_priority(start_date, due_date))
            new_task.save()
            return True
        except pw.IntegrityError:
            print("An identical task already exists. Cannot add this task to the database.")
            return False

    @staticmethod
    def update_task(task_name, task_details, start_date, due_date):
        try:
            row = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row.task_details = task_details
            row.task_start_date = start_date
            row.task_due_date = due_date
            # row.task_status = task_status
            row.save()
            return True
        except pw.DoesNotExist:
            logger.info("")

    @staticmethod
    def delete_task(task_name):
        """
        Marks the status column of a task as 'Deleted.'
        """
        try:
            row_query = tm.Tasks.select().where(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Deleted'
            logger.info(f'Task name: {task_name} -- marked as deleted.')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not modify task with name, "{task_name}," as it was not found.')
            return False

    @staticmethod
    def complete_task(task_name):
        """
        Marks the status column of a task as 'Completed.'
        """
        try:
            row_query = tm.Tasks.select().where(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Completed'
            logger.info(f'Task name: {task_name} -- is Complete!')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not modify task with name, "{task_name}," as it was not found.')
            return False


class TaskLists:
    """
    Curates functions relating to organizing tasks into lists
    """

    def task_list_id_sort(self):
        query = tm.Tasks.select().where(tm.Tasks.task_status != 'Deleted')


    def database_report(self):
        query = tm.Tasks.select().dicts()
        formatted_list = []
        for row in query:
            task_id = row['task_id']
            task_name = row['task_name']
            task_details = row['task_details']
            task_start_date = row['task_start_date']
            task_due_date = row['task_due_date']
            task_priority = row['task_priority']
            task_status = row['task_status']
            formatted_content = [task_id, task_name, task_details, task_start_date,
                                 task_due_date, task_priority, task_status]
            formatted_list.append(formatted_content)
            print("----------------------------------------------------------------------------------")
            print(tabulate(formatted_list, headers=['Task ID', 'Name', 'Details','Start Date', 'Due Date'
                                                    'Priority', 'Status'], tablefmt='github'))
            print("----------------------------------------------------------------------------------")
