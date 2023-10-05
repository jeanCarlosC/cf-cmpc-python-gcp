FROM python:3.9

WORKDIR /app

COPY src/requirements.txt /
COPY src/requirements_dev.txt /

RUN pip install -r /requirements.txt
RUN pip install -r /requirements_dev.txt

EXPOSE 8080