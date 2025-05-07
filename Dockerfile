FROM python:3.13.3-slim

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --upgrade --root-user-action=ignore pip
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

ENV FLASK_APP=app.py

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]