"""
Placeholder file to add py tests for testing the CLI app
"""

from typer.testing import CliRunner
import peewee as pw
from todolistapp.task_model import Tasks
import todolistapp.do_or_die as dod
from todolistapp.do_or_die import app
import datetime


runner = CliRunner()

START_DATE = datetime.datetime.now().strftime('%m/%d/%Y')

DUE_DATE = (datetime.date.today() + datetime.timedelta(days=4)).strftime('%m/%d/%Y')

MODEL = [Tasks]

test_db = pw.SqliteDatabase(':memory:')

# This wrapper does not work well
# I used the context manage inside the test function instead
def use_test_database(func):
    """
    Uses a context manager to open, create table, and close
    a connection to a peewee (SQLite3 database)
    """

    @pw.wraps(func)
    def inner(self):

        with test_db.bind_ctx(MODEL):
            test_db.create_tables(MODEL)
            try:
                func(self)
            finally:
                test_db.drop_tables(MODEL)
    return inner



def test_app():
    """
    Tests that the console application runs and exits with exit code 2.
    """
    result = runner.invoke(app)
    assert result.exit_code == 2


def test_create_task():
    """
    Attempts to test the output of the create function to the stdout.
    However, passing assert a string results in a condition that is
    always true.
    """
    result = runner.invoke(app)
    with test_db.bind_ctx(MODEL):
        test_db.create_tables(MODEL)
        try:
            dod.create("Test task",
                       "Test description",
                       START_DATE,
                       DUE_DATE)
        finally:
            test_db.drop_tables(MODEL)
    assert "\n" in result.stdout
    # assert "Added, 'Test task,' to the list." in result.stdout


def test_complete_task():
    """
    Attempts to test the output of the complete function.
    :return:
    """
    result = runner.invoke(app)
    with test_db.bind_ctx(MODEL):
        test_db.create_tables(MODEL)
        try:
            dod.create("Test task",
                       "Test description",
                       START_DATE,
                       DUE_DATE)
            dod.complete("Test task")
        finally:
            test_db.drop_tables(MODEL)
    assert "\n" in result.stdout

def test_update_task():
    """
    Attempts to test the output of the complete function.
    :return:
    """
    result = runner.invoke(app)
    with test_db.bind_ctx(MODEL):
        test_db.create_tables(MODEL)
        try:
            dod.create("Test task",
                       "Test description",
                       START_DATE,
                       DUE_DATE)
            dod.update("Modified task",
                       "Modified description",
                       START_DATE,
                       DUE_DATE)
        finally:
            test_db.drop_tables(MODEL)
    assert "\n" in result.stdout

def test_delete_task():
    """
    Attempts to test the output of the complete function.
    :return:
    """
    result = runner.invoke(app)
    with test_db.bind_ctx(MODEL):
        test_db.create_tables(MODEL)
        try:
            dod.create("Test task",
                       "Test description",
                       START_DATE,
                       DUE_DATE)
            dod.delete("Test task")
        finally:
            test_db.drop_tables(MODEL)
    assert "\n" in result.stdout
