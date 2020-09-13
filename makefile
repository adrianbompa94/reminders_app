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
