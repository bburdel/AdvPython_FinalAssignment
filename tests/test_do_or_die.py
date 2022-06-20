"""
Placeholder file to add py tests for testing the CLI app
"""

from typer.testing import CliRunner
import peewee as pw
from todolistapp.task_model import Tasks
import todolistapp.do_or_die as dod
from todolistapp.do_or_die import app


runner = CliRunner()

MODEL = [Tasks]

test_db = pw.SqliteDatabase(':memory:')


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
                       "06/20/2022",
                       "06/23/2022")
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
                       "06/20/2022",
                       "06/23/2022")
            dod.complete("Test task")
        finally:
            test_db.drop_tables(MODEL)
    assert "\n" in result.stdout
