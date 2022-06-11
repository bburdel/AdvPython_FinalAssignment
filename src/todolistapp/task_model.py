'''
the sqlite/peewee model
'''

from pathlib import Path
import peewee as pw
from loguru import logger

file = Path('taskmodel.db')
# if Path.exists(file):
#     Path.unlink(file)
#     logger.info(f"The existing file, {file}, was deleted.")

db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    """
    Created for inheritance of peewee Model properties
    """
    logger.info("Created BaseModel for Model classes to inherit from...inherits from peewee Model")

    class Meta:
        """
        Set up for database inheritance
        """
        database = db


# Create task table
class Tasks(BaseModel):
    """
    This class defines Tasks, which maintains details of a task for ta To Do List platform for which we want to store
    task information.
    """
    # TODO more validation and checks in the parameters
    logger.info("peewee model == 'Tasks' created.")
    task_id = pw.CharField(primary_key=True)
    task_name = pw.CharField(max_length=50, null=False)
    task_details = pw.CharField(max_length=100)
    task_start_date = pw.DateField(formats='%m/%d/%Y')
    task_due_date = pw.DateField(formats='%m/%d/%Y')
    task_complete_date = pw.DateField(formats='%m/%d/%Y', null=True)
    task_priority = pw.CharField()
    task_status = pw.CharField(default='In Progress')  # Maybe?: Not Started, In Progress, Completed, Deleted


# class TasksRemoved(BaseModel):
#     """
#     This class curates Tasks that have been removed from the main list of tasks.
#     """
#     logger.info("peewee model == 'TasksRemoved' created.")
#     task_id = pw.ForeignKeyField(Tasks, to_field='task_id')  # on_delete='CASCADE'
#     task_name = pw.CharField(max_length=50, null=False)
#     task_status = pw.CharField()

def main_task_database():
    """
    Connect to established database
    """

    db.connect()
    # logger.info(f"Connected to the database: {db}")
    db.execute_sql('PRAGMA foreign_keys = ON;')
    # Creates the tables in the database ready for us to use
    # logger.info("Task table generating...")
    db.create_tables([Tasks])
    # # db.create_tables([StatusCollection])
    # logger.info("Task table created.")


if __name__ == '__main__':
    main_task_database()
