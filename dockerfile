FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get -y update; apt-get -y install curl

COPY . .

CMD ["python", "main.py"]