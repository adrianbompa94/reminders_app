from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import os
import psycopg2
import time

app = Flask(__name__)
api = Api(app)

reminders = []

DB_CONFIG = {
    "pg_database": os.environ["PGDATABASE"],
    "pg_host": os.environ["PGHOST"],
    "pg_password": os.environ["PGPASSWORD"],
    "pg_port": os.environ.get("PGPORT", 5432),
    "pg_user": os.environ["PGUSER"],
}

class PgSql(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            user=DB_CONFIG.pg_user,
            password=DB_CONFIG.pg_password,
            host=DB_CONFIG.pg_host,
            port=DB_CONFIG.pg_port,
            database=DB_CONFIG.pg_database,
        )

    def __enter__(self):
        # Make a database connection and return it
        return self.connection

    def __exit__(self, *args):
        self.connection.close()

class Reminder(Resource):
    def post(self):
        req_data = request.get_json()

        if 'message' not in req_data.keys():
            abort(400, 'Required parameter missing: message')
        
        if 'time' not in req_data.keys():
            abort(400, 'Required parameter missing: time')
        
        if not isTimeFormat(req_data['time']):
            abort(400, 'Parameter is not in a correct format: time (HH:MM)')
        
        if next(filter(lambda reminder: reminder['message'] == req_data['message'], reminders), None) is not None:
            abort(409, "A reminder with message '{}' already exists.".format(req_data['message']))
        
        with PgSql() as db:
            cursor = db.cursor()
            insert_message = """INSERT INTO {table} (message, time) VALUES ('{message}', '{tstamp}')""".format(
                message=req_data["message"],
                table="some-table",
                tstamp=req_data["time"],
            )
            cursor.execute(insert_message)
            db.commit()
            cursor.close()
        
        reminders.append(req_data)
        return req_data

class ReminderList(Resource):
    def get(self):
        with PgSql() as db:
            cursor = db.cursor()
            get_message = """SELECT message, time FROM {table}""".format(table="some-table")
            reminders = cursor.fetchall(get_message)
            db.commit()
            cursor.close()
        return reminders

def isTimeFormat(time_string):
    try:
        time.strptime(time_string, '%H:%M')
        return True
    except ValueError:
        return False



api.add_resource(ReminderList, '/reminders')
api.add_resource(Reminder, '/reminder')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')


