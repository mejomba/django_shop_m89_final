FROM python:3.10-alpine
ENV PYTHONBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /django

COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#EXPOSE 587/udp
#EXPOSE 587/tcp
