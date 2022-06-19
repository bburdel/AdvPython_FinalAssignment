"""
Placeholder file to add py tests for testing the CLI app
"""
import pytest
from typer.testing import CliRunner
import peewee as pw
from todolistapp.task_model import Tasks
import todolistapp.do_or_die as dod
from todolistapp.do_or_die import app

# import pytest

runner = CliRunner()

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


@pytest.fixture
def run_commands():
    return "python3 do_or_die.py "


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 2


# def test_app2(func):
#     result = runner.invoke(app)
#     func()
#     assert result.exit_code == 0
#     return func()


# @test_app2

# @use_test_database
@pytest.fixture
def test_create_task(run_commands):
    result = runner.invoke(app)
    with test_db.bind_ctx(MODEL):
        test_db.create_tables(MODEL)
        try:
            create = dod.create("Test task",
                       "Test description",
                       "06/20/2022",
                       "06/23/2022")
            (run_commands + create)
        finally:
            test_db.drop_tables(MODEL)

    assert "Added, 'Test task,' to the list." in result.stdout

#
# @use_test_database
# def test_complete_task(self):
#     result = runner.invoke(app)
#     dod.complete("Test task")
#     assert "Test task -- LAID TO REST" in result.stdout
