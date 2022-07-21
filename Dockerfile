FROM python:3.10.5-slim-buster
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]
