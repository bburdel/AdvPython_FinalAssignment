"""
Working with Flask, cURL, and JSON
"""
import typer
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
# import peewee as pw

db_connect = create_engine("sqlite:///taskmodel.db")


# TODO what does it make sense to query? -- entire db contents? all task names, some of the lists?
class Tasks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = "select * from Tasks"


class TasksNames(Resource):
    def get(self):
        # open connection to the database
        conn = db_connect.connect()
        query = conn.execute(
            "select * from Tasks")
        # result = {"task name": [row[1] for row in query.cursor.fetchall()]}
        result = {"data": [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        conn.connect()
        return jsonify(result)


def main():
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(TasksNames, "/all")  # Route 1
    typer.echo(f"Route: http://127.0.0.1:5000/all")
    app.run(port=5000)

    db_connect.dispose()


if __name__ == '__main__':
    main()
