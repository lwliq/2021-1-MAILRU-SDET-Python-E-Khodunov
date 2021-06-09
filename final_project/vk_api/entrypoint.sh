#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 0.1
done

echo "MySQL started"

python app.py

exec "$@"