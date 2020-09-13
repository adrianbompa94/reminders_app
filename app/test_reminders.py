from app import app
from flask import json

def test_empty_reminders():
    response = app.test_client().get('/reminders')
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert len(response_data) == 0

def test_add_reminder():
    reminder = {'message': 'adrian', 'time': '20:00'}
    response = app.test_client().post(
        '/reminder', 
        data=json.dumps(reminder), content_type='application/json')
    response_data = json.loads(response.get_data(as_text=True))
    
    assert response.status_code == 200
    assert response_data == reminder

def test_reminder_message_validation():
    reminder = {'time': '20:00'}

    response = app.test_client().post(
        '/reminder', 
        data=json.dumps(reminder), 
        content_type='application/json'
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert response_data == {'message': 'Required parameter missing: message'}

def test_reminder_time_format_validation():
    reminder = {'message':'reminder', 'time':'011:02'}

    response = app.test_client().post(
        '/reminder', 
        data=json.dumps(reminder), 
        content_type='application/json'
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert response_data == {'message': 'Parameter is not in a correct format: time (HH:MM)'}

def test_duplicate_reminder_validation():
    reminder = {'message': 'Reminder 2', 'time': '10:10'}
    duplicate_reminder = {'message': 'Reminder 2', 'time': '10:10'}

    response = app.test_client().post(
        '/reminder', 
        data=json.dumps(reminder), 
        content_type='application/json'
    )
    assert response.status_code == 200

    response = app.test_client().post(
        '/reminder', 
        data=json.dumps(duplicate_reminder), 
        content_type='application/json'
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 409
    assert response_data == {'message': "A reminder with message '{}' already exists.".format(duplicate_reminder['message'])}





