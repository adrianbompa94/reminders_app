FROM python:3.8-slim-buster

COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install -r requirements.txt

COPY . /code

ENTRYPOINT [ "python" ]

CMD [ "app/app.py" ]
