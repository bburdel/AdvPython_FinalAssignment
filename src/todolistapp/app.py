"""
Working with Flask, cURL, and JSON
"""

from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
# import peewee as pw

db_connect = create_engine("sqlite:///taskmodel.db")


class TasksNames(Resource):
    def get(self):
        # open connection to the database
        conn = db_connect.connect()
        query = conn.execute(
            "select * from Tasks")
        result = {"task name": [row[1] for row in query.cursor.fetchall()]}
        conn.connect()
        return jsonify(result)


def main():
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(TasksNames, "/tasks")  # Route 1

    app.run(port=5000)

    db_connect.dispose()


if __name__ == '__main__':
    main()
