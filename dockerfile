# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

CMD ["gunicorn", "main:app"]