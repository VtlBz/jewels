FROM python:3.9-slim

RUN apt-get update && apt-get full-upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /jewels

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir

COPY jewels/ .

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "jewels.wsgi:application", "--bind", "0:8000" ]