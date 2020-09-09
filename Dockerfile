FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add jpeg-dev libffi-dev zlib-dev

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./entrypoint.sh  /code/

COPY . /code/

ENTRYPOINT [ "/code/entrypoint.sh" ]
