from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import boto3
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time

AWS_ACCESS_KEY = "AKIAJA5ZLTPDNWYMLKCA"
AWS_SECRET_KEY = "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"
STREAM_NAME = "reminders"

os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_KEY

app = Flask(__name__)
api = Api(app)
kinesis_client = boto3.client("kinesis", region_name="us-east-1")

reminders = []


class PgSql(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postgres",
            host="reminders.chdx1nxslrp2.us-east-1.rds.amazonaws.com",
            password="Vadim2021!",
            port=5432,
            user="postgres",
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
        
        # PostgreSQL write
        with PgSql() as db:
            cursor = db.cursor(cursor_factory=RealDictCursor)
            insert_message = """INSERT INTO {table} (message, time_at) VALUES ('{message}', '{tstamp}')""".format(
                message=req_data["message"],
                table="reminders",
                tstamp=req_data["time"],
            )
            print(f"Writing this to database: {insert_message}")
            cursor.execute(insert_message)
            db.commit()
            cursor.close()

        # Kinesis write
        payload = req_data
        print(f"Writing this to {STREAM_NAME}: {payload}")
        put_response = kinesis_client.put_record(
            Data=json.dumps(payload),
            PartitionKey=str(int(time.time())),
            StreamName=STREAM_NAME,
        )

        reminders.append(req_data)
        return req_data


class ReminderList(Resource):
    def get(self):
        # PostgreSQL read
        with PgSql() as db:
            cursor = db.cursor(cursor_factory=RealDictCursor)
            get_message = """SELECT message, time_at FROM {table}""".format(
                table="reminders"
            )
            reminders = cursor.fetchall(get_message)
            db.commit()
            cursor.close()
        return reminders


def isTimeFormat(time_string):
    try:
        time.strptime(time_string, "%H:%M")
        return True
    except ValueError:
        return False


api.add_resource(ReminderList, "/reminders")
api.add_resource(Reminder, "/reminder")

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
