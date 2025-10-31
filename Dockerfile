FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

# PORT will be set by Render at runtime (defaults to 10000)
# For local development, set PORT=8000 in docker-compose.yml

# CMD ["gunicorn", "fabrik.wsgi:application", "--bind", "0.0.0.0:8000"]