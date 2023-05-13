#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
    echo "Trying to connect to postgres..."
    sleep 1
done
echo "PostgreSQL started"

echo "Waiting for elastic..."
while ! nc -z $ES_HOST $ES_PORT; do
    echo "Trying to connect to elastic..."
    sleep 1
done
echo "Elastic started"
