#!/bin/sh

# Wait for DB
python << END
import socket
import time
import os

host = os.environ.get('DB_HOST')
port = int(os.environ.get('DB_PORT'))

print(f"Waiting for database at {host}:{port}...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error:
        time.sleep(1)
END

echo "Database is ready. Running migrations..."
python manage.py migrate

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
