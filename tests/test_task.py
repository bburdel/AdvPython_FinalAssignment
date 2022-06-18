"""
Will contain tests for the tasks.py file
"""

from unittest import TestCase
import peewee as pw
from todolistapp.task_model import Tasks
import todolistapp.task as t
import todolistapp

MODELS = Tasks

test_db = pw.SqliteDatabase(':memory:')


def use_test_database(fn):
    """
    Sets up a test database for unit tests below
    """
    @pw.wraps(fn)
    def inner(self):
        with test_db.bind_ctx(MODELS):
            test_db.create_tables(MODELS)
            try:
                fn(self)
            finally:
                test_db.drop_tables(MODELS)

    return inner


# class TestDateHelper(TestCase):
#     """
#     Collection of unit tests for class 'DateHelper' in tasks.py
#     """
#     def test_check_date(self, date):
#         pass
#
#     def test_date_conversion(self, date):
#         pass
#

class TestTaskModel(TestCase):
    """
    Collection of unit tests for tasks.py
    """
    @use_test_database
    def test_add_task_true(self):
        """
        Tests adding a task
        :return:
        """
        new_task = t.Task.add_task("New task", "Placeholder", "6/18/2022", "6/20/2022")
        self.assertTrue(new_task)

    def test_add_task(self):
        """
        Tests adding a duplicate task
        :return:
        """
        t.Task.add_task("New task", "Placeholder", "6/18/2022", "6/20/2022")
        dup_task = t.Task.add_task("New task", "Placeholder", "6/18/2022", "6/20/2022")
        self.assertFalse(dup_task)
        self.assertRaises(pw.IntegrityError)

    @use_test_database
    def test_update_task(self):
        """
        Tests updating a task
        :return:
        """
        pass

    @use_test_database
    def test_delete_task(self):
        pass

    @use_test_database
    def test_complete_task(self):
        pass


