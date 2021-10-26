FROM python:3.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install -y postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]


#FROM python:3.9
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /usr/src/dm_rest
#
#COPY ./requirements.txt /usr/src/requirements.txt
#RUN pip install -r /usr/src/requirements.txt
#
#COPY . /usr/src/dm_rest
#
#EXPOSE 8000
