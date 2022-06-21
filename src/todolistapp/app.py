"""
Title: app.py
Description: A basic API script using Flask and sqlalchemy
Author: BBurdelsky
Version: Python 3.10
"""

import typer
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify
from sqlalchemy import create_engine

db_connect = create_engine("sqlite:///taskmodel.db")


class TaskNames(Resource):
    """
    Simple class containing a get function
    """

    def get(self):
        """
        returns all tasks in a database jsonified
        """
        conn = db_connect.connect()
        query = conn.execute(
            "select * from Tasks")
        # result = {"task name": [row[1] for row in query.cursor.fetchall()]}
        result = {"data": [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        conn.connect()
        return jsonify(result)


# class TaskDetails(Resource):
#     """
#     Simple class containing a get function
#     """
#
#     def get(self, task_name: str):
#         """
#         returns the task name and details for all tasks in database
#         """
#         conn = db_connect.connect()
#         query = conn.execute(f"select * from Tasks where task_name =={str(task_name)} ")
#         result = {"data": [dict(zip(tuple(query.keys()), i))
#                            for i in query.cursor]}
#         conn.close()
#         return jsonify(result)


def main():
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(TaskNames, "/all")  # Route 1
    typer.echo("Route (all tasks in db): http://127.0.0.1:5000/all")
    # api.add_resource(TaskDetails, "/details")  # Route 2
    # typer.echo("Route (task details for specific task): http://127.0.0.1:5000/<task_name>")
    app.run(port=5000)

    db_connect.dispose()


if __name__ == '__main__':
    main()
