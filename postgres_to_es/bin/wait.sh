#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z $ETL_DB_HOST $ETL_DB_PORT; do
    echo "Trying to connect to postgres..."
    sleep 2
done
echo "PostgreSQL started"


echo "Waiting for elastic..."
while ! nc -z $ETL_ES_HOST $ETL_ES_PORT; do
    echo "Trying to connect to elastic..."
    sleep 2
done
echo "Elastic started"


echo "Waiting for redis..."
while ! nc -z $ETL_REDIS_HOST $ETL_REDIS_PORT; do
    echo "Trying to connect to redis..."
    sleep 2
done
echo "Redis started"
