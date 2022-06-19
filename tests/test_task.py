"""
Will contain tests for the tasks.py file
"""
import builtins
import unittest
from unittest import TestCase
from unittest.mock import patch
import peewee as pw
from loguru import logger
# import pysnooper
from todolistapp.task_model import Tasks
import todolistapp.task as t

logger.info("Logging test activities from test_task.py")
logger.add("out_test.log", backtrace=True, diagnose=True)


MODEL = [Tasks]

test_db = pw.SqliteDatabase(':memory:')


def use_test_database(funcn):
    """
    Uses a context manager to open, create table, and close
    a connection to a peewee (SQLite3 database)
    """
    @pw.wraps(funcn)
    def inner(self):

        with test_db.bind_ctx(MODEL):
            test_db.create_tables(MODEL)
            try:
                funcn(self)
            finally:
                test_db.drop_tables(MODEL)

    return inner


class TestTaskModel(TestCase):
    """
    Collection of unit tests for tasks.py
    """

    @use_test_database
    def test_add_task_true(self):
        """
        Tests adding a task
        """
        new_task = t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        self.assertTrue(new_task)
        if new_task:
            logger.info("SUCCESS! Function works as expected.")
        else:
            logger.info("UH OH! Something went wrong with this test.")

    @use_test_database
    def test_add_dup_task(self):
        """
        Tests adding a duplicate task
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        dup_task = t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        self.assertFalse(dup_task)
        self.assertRaises(pw.IntegrityError)
        if not dup_task:
            logger.info("SUCCESS! Function works as expected.")
        else:
            logger.info("UH OH! Something went wrong with this test.")

    @use_test_database
    def test_update_task(self):
        """
        Tests updating a task
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        updated_task = t.Task.update_task("New task", "Updated details",
                                          "6/18/2022", "6/20/2022")

        self.assertTrue(updated_task)
        if updated_task:
            logger.info("SUCCESS! Function works as expected.")
        else:
            logger.info("UH OH! Something went wrong with this test.")

    @use_test_database
    def test_update_unk_task(self):
        """
        Tests updating an unknown (task does not exist) task
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        unknown_task_update = t.Task.update_task("Non-existent task",
                                                 "Test it fails to update",
                                                 "6/18/2022", "6/25/2022")
        self.assertFalse(unknown_task_update)
        self.assertRaises(pw.DoesNotExist)
        if not unknown_task_update:
            logger.info("SUCCESS! Function works as expected.")
        else:
            logger.info("UH OH! Something went wrong with this test.")

    @use_test_database
    def test_delete_task(self):
        """
        Tests deleting a task
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        deleted_task = t.Task.delete_task("New task")
        self.assertTrue(deleted_task)

    @use_test_database
    def test_delete_deleted_task(self):
        """
        Tests deleting a task that does not exist
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        # t.Task.delete_task("New task")
        deleted_test = t.Task.delete_task("Nonexistent task")
        self.assertRaises(pw.DoesNotExist)
        self.assertFalse(deleted_test)

    @use_test_database
    def test_complete_task(self):
        """
        Tests completing a task
        """
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        completed_task =t.Task.complete_task("New task")
        self.assertTrue(completed_task)

    @use_test_database
    def test_complete_unk_task(self):
        t.Task.add_task("New task", "Placeholder", "6/19/2022", "6/20/2022")
        completed_task = t.Task.complete_task("Unknown task")
        self.assertFalse(completed_task)
        self.assertRaises(pw.DoesNotExist)


# class TestTaskLists(TestCase):
#     """
#     Collection of tests for lists of database outputs
#     """
#
#     @use_test_database
#     @patch('builtins.print')
#     def test_print_any_list(self, mock_print):
#         query_result = [{"task_id": "123456789",
#                                            "task_name": "Test task",
#                                            "task_details": "Anything",
#                                            "task_start_date": "6/18/2022",
#                                            "task_due_date": "6/22/2022",
#                                            "task_complete_date": "6/20/2022",
#                                            "task_priority": "Medium",
#                                            "task_status": "Complete",
#                                            }]
#         t.TaskLists.print_any_list_choice(query_result)
#         mock_print.assert_called_with()


# if __name__ == '__main__':
#     unittest.main()
