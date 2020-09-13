from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import time

app = Flask(__name__)
api = Api(app)

reminders = []

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
        
        reminders.append(req_data)
        return req_data

class ReminderList(Resource):
    def get(self):
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


