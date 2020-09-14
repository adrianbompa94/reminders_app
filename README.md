# Reminder App

Reminder App is a Flask RESTful API that provides users the option of creating new reminders and query the reminders. 

## Installation

Clone the github repository

```bash
git clone https://github.com/adrianbompa94/reminders_app.git
```

## Usage
A makefile with available commands is added in the project root location, that describes differnet commands that can be runned to build/start the application and run unit tests.

```python
SHELL := /bin/bash

all: docker_image \
	run

docker_image:
	docker build -t reminder_app:latest .

run:
	docker run -d -p 5000:5000 --name reminder_app reminder_app

stop: 
	docker stop $(shell docker container ls -f name=reminder_app -q) &&\
	docker rm $(shell docker container ls -f name=reminder_app -q)

bash:
	docker exec -it $(shell docker container ls -f name=reminder_app -q) /bin/bash

run_tests:
	docker exec -it $(shell docker container ls -f name=reminder_app -q) py.test

```
On the root project location, running command ```make all``` will build an image and run a container based on that image, that will expose the API on 0.0.0.0:5000

Examples:
```
curl -X POST \
  http://0.0.0.0:5000/reminder \
  -H 'Content-Type: application/json' \
  -H 'Host: 0.0.0.0:5000' \
  -H 'User-Agent: PostmanRuntime/7.13.0' \
  -H 'accept-encoding: gzip, deflate' \
  -H 'cache-control: no-cache' \
  -H 'content-length: 48' \
  -d '{
	"message":"hello world",
	"time": "23:19"
}'

curl -X GET \
  http://0.0.0.0:5000/reminders \
  -H 'Content-Type: application/json' \
  -H 'Host: 0.0.0.0:5000' \
  -H 'User-Agent: PostmanRuntime/7.13.0' \
  -H 'accept-encoding: gzip, deflate' \
  -H 'cache-control: no-cache' \
  -H 'content-length: 48'

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
