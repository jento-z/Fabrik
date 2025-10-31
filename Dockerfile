FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]


EXPOSE 8000
# PORT will be set by Render at runtime via environment variable
# Default to 8000 for local development
ENV PORT=8000

# CMD ["gunicorn", "fabrik.wsgi:application", "--bind", "0.0.0.0:8000"]