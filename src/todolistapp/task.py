'''
task related functions
'''

import datetime as d
from datetime import datetime
from loguru import logger
import peewee as pw
import task_model as tm
from tabulate import tabulate
import pysnooper


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
            return priority
        if 3 <= date_delta <= 7:
            priority = 'Medium'
            return priority
        if date_delta < 3:
            priority = 'High'
            return priority

    @staticmethod
    @pysnooper.snoop(depth=1)
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
            print("Peewee Integrity Error -- Cannot add this task to the database.")
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
            row_query = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Deleted'
            row_query.save()
            logger.info(f'Task name: {task_name} -- marked as deleted.')
            return True
        except pw.DoesNotExist:
            logger.info(f'Could not modify task with name, "{task_name}," as it was not found.')
            return False

    @staticmethod
    @pysnooper.snoop(depth=1)
    def complete_task(task_name):
        """
        Marks the status column of a task as 'Completed.'
        """
        try:
            row_query = tm.Tasks.get(tm.Tasks.task_name == task_name)
            row_query.task_status = 'Completed'
            row_query.task_complete_date = datetime.now()
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

    # List all tasks sorted by task number
    # List all tasks sorted by priority
    # List all open tasks sorted by due date
    # List all closed tasks between specified dates
    # List all overdue tasks

    @staticmethod
    def print_any_list_choice(query_results):
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
        print("----------------------------------------------------------------------------------")
        print(tabulate(formatted_list, headers=['Task ID', 'Name', 'Details', 'Start Date', 'Due Date',
                                                'Completed On', 'Priority', 'Status'], tablefmt='github'))
        print("----------------------------------------------------------------------------------")

    @staticmethod
    def database_report():
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
                                 task_due_date, task_priority, task_status]
            formatted_list.append(formatted_content)
        print("----------------------------------------------------------------------------------")
        print(tabulate(formatted_list, headers=['Task ID', 'Name', 'Details', 'Start Date', 'Due Date',
                                                'Completed On', 'Priority', 'Status'], tablefmt='github'))
        print("----------------------------------------------------------------------------------")

    @staticmethod
    def task_list_id_sort(choice):
        # filtered_options = ['In Progress', 'Complete']
        list_of_dicts = []
        try:
            if choice.strip() == '1':
                print('Task IDs in Ascending order:')
                query = tm.Tasks.select().where(tm.Tasks.task_status.in_(['In Progress', 'Complete']))\
                    .order_by(+tm.Tasks.task_id)
                for result in query.dicts():
                    list_of_dicts.append(result)
                print(list_of_dicts)
                TaskLists.print_any_list_choice(list_of_dicts)
                # string formatting instead?
            elif choice.strip() == '2':
                print('Task IDs in Descending order:')
                query = tm.Tasks.select().where(tm.Tasks.task_status.in_(['In Progress', 'Complete']))\
                    .order_by(-tm.Tasks.task_id)
                query_dict = query.dicts()
                TaskLists.print_any_list_choice(query_dict)
            else:
                print('That is not a valid option.')
        except Exception as e:
            print("Something went wrong, please try again.")
            logger.info(e)

    @staticmethod
    def task_list_priority_sort():
        try:
            query = tm.Tasks.select().where(tm.Tasks.task_status != 'Deleted')\
                .order_by(tm.Tasks.task_due_date, tm.Tasks.task_priority)
            for row in query:
                print(f"{row.task_priority}, {row.task_due_date}, {row.task_name}, {row.task_details} ")
        except Exception as e:
            logger.info(e)
